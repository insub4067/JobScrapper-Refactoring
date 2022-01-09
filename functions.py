import requests
from bs4 import BeautifulSoup
from db import db

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}


# REQUESTS AND GET SOUP
def get_soup(url):
    response = requests.get(url, headers=headers).text
    return BeautifulSoup(response, "html.parser")


# REMOTEOK
def parse_remoteok(soup):
    parsed_jobs = []
    jobs = soup.find_all("tr", {"class": "job"})

    def isPay(input):
        if "$" in input and "k" in input:
            return True
        return False

    for job in jobs:
        link = "https://remoteok.com/" + job["data-url"]
        company = job.find("h3", {"itemprop": "name"}).get_text().strip()
        title = job.find("h2", {"itemprop": "title"}).get_text().strip()
        location = ""
        pay = ""
        div = job.find("div", {"class": "location"}).get_text().strip()

        if isPay(div):
            pay = div
        else:
            location = div

        parsed_jobs.append(
            {
                "title": title,
                "link": link,
                "company": company,
                "location": location,
                "pay": pay,
            }
        )
    return parsed_jobs


def scrap_remoteok(word):
    url = f"https://remoteok.com/remote-{word}-jobs"
    soup = get_soup(url)

    return parse_remoteok(soup)


# REMOTELY
def parse_remotely(soup):
    jobs = soup.find_all("li", {"class": "feature"})
    parsed_jobs = []

    for job in jobs:
        link = "https://weworkremotely.com/" + job.find("a")["href"]
        company = job.find("span", {"class": "company"}).get_text().strip()
        title = job.find("span", {"class": "title"}).get_text().strip()
        location = job.find("span", {"class": "region company"}).get_text().strip()
        pay = ""

        parsed_jobs.append(
            {
                "title": title,
                "link": link,
                "company": company,
                "location": location,
                "pay": pay,
            }
        )

    return parsed_jobs


def scrap_remotely(word):

    url = f"https://weworkremotely.com/remote-jobs/search?term={word}&button=&categories%5B%5D=2&categories%5B%5D=17&categories%5B%5D=18"
    soup = get_soup(url)

    return parse_remotely(soup)


# STACK_OVERFLOW
def parse_stackOverflow(soup):
    jobs = soup.find_all("div", {"class": "-job"})
    parsed_jobs = []

    for job in jobs:
        link = job.find("h2").find("a", href=True)["href"]
        link = f"https://stackoverflow.com{link}"
        title = job.find("h2").get_text().strip()
        company = job.find("h3").find("span").get_text().strip()
        location = (
            job.find("h3").find("span", {"class": "fc-black-500"}).get_text().strip()
        )
        pay = ""

        try:
            pay = job.find("ul").find("li", title=True).get_text().strip()
            if pay is None:
                pay = pay
        except Exception:
            pass

        parsed_jobs.append(
            {
                "title": title,
                "link": link,
                "company": company,
                "location": location,
                "pay": pay,
            }
        )

    return parsed_jobs


def scrap_stackOverflow(word):
    url = f"https://stackoverflow.com/jobs?q={word}&r=true"
    soup = get_soup(url)
    parsed_jobs = []
    try:
        pages = soup.find("div", {"class": "s-pagination"}).find_all("a")[:-1]

        for idx, page in enumerate(pages):
            page = idx + 1

            if page == 1:
                parsed_jobs = parsed_jobs + parse_stackOverflow(soup)

            elif page > 1:
                url = f"https://stackoverflow.com/jobs?q={word}&pg={page}"
                soup = get_soup(url)
                parsed_jobs = parsed_jobs + parse_stackOverflow(soup)
    except AttributeError:
        parsed_jobs = parsed_jobs + parse_stackOverflow(soup)

    return parsed_jobs


# SCRAP SPREADER
def scrap_jobs(word):
    stackOverflow_jobs = scrap_stackOverflow(word)
    remotely_jobs = scrap_remotely(word)
    remoteok_jobs = scrap_remoteok(word)

    jobs = stackOverflow_jobs + remotely_jobs + remoteok_jobs

    db[word] = jobs

    return jobs
