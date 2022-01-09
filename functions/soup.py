from bs4 import BeautifulSoup
import aiohttp

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}

# REQUESTS AND GET SOUP
async def aysnc_get_soup(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, ssl=False) as response:
            response = await response.text()
            return BeautifulSoup(response, "html.parser")
