from .soup import aysnc_get_soup
import itertools
import asyncio
import time


# STACK_OVERFLOW
async def parse_stackOverflow(**kwargs):

    url = kwargs.get("url")
    soup = kwargs.get("soup")

    if url:
        soup = await aysnc_get_soup(url)

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


async def scrap_stackOverflow(word):
    url = f"https://stackoverflow.com/jobs?q={word}&r=true"
    soup = await aysnc_get_soup(url)
    parsed_jobs = []
    try:
        pages = soup.find("div", {"class": "s-pagination"}).find_all("a")[:-1]

        urlList = [
            "https://stackoverflow.com/jobs?q={word}&pg={index}".format(
                index=page.text.strip(), word=word
            )
            for page in pages
        ]

        tasks = [asyncio.ensure_future(parse_stackOverflow(url=url)) for url in urlList]
        parsed_jobs = await asyncio.gather(*tasks)
        parsed_jobs = list(itertools.chain(*parsed_jobs))

    except AttributeError:
        parsed_jobs = parsed_jobs + await parse_stackOverflow(soup=soup)

    return parsed_jobs
