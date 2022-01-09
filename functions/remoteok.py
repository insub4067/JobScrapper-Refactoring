from .soup import aysnc_get_soup

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


async def scrap_remoteok(word):
    url = f"https://remoteok.com/remote-{word}-jobs"
    soup = await aysnc_get_soup(url)

    return parse_remoteok(soup)
