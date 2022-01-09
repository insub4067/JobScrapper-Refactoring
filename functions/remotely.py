from .soup import aysnc_get_soup

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


async def scrap_remotely(word):

    url = f"https://weworkremotely.com/remote-jobs/search?term={word}&button=&categories%5B%5D=2&categories%5B%5D=17&categories%5B%5D=18"
    soup = await aysnc_get_soup(url)

    return parse_remotely(soup)
