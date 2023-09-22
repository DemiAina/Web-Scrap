import httpx
from selectolax.parser import HTMLParser

from dataclasses import dataclass, asdict

# id pages
# check if there are any a tags if not just scrap this website

url = 'https://www.rent.ie/houses-to-let/renting_dublin/3_beds/'

@dataclass
class Houses:
    address : str
    money : str
    link : str

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept-Language' : 'en-US,en;q=0.9',
    'Referer' : 'https://google.com',
    'DNT' : '1',
}

def setup(url):
    response = httpx.get(url)
    html = HTMLParser(response.text) 
    return html

def getMax(html):
    num = []
    pages = html.css("a[title]")
    for page in pages: 
        data = page.text()
        num.append(data)
    num.pop()
    return num.pop()

def parse(html):
    houses = html.css("div.search_result")
    print(houses)
    results = []
    for house in houses:
        new_house = Houses(
            house.css_first("a[href]").text(),
            house.css_first("h4").text(),
            house.css_first("a").attributes.get('href'),

        )
        print(new_house)
    # for house in houses:
    #     new_house = Houses(
    #         address=house.css_first("a").text(),      
    #         money=house.css_first("h4").text(),
    #         link=house.css_first("a[href]").text(),      
    #
    #     )


def scrap(newUrl):
    try:
        response = httpx.get(newUrl,follow_redirects=True,headers=headers)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        html = HTMLParser(response.text)
        parse(html)
    except httpx.HTTPError as err:
        # Handle HTTP errors (status codes >= 400)
        print(f"HTTP error occurred: {err}")

def makeUrl(url,max):
    for i in range(1, max + 1):
        newUrl = f"{url}page_{i}"
        scrap(newUrl)

def main():
    html = setup(url)
    max  = int(getMax(html))
    makeUrl(url,max)

if __name__ == '__main__':
    main()

