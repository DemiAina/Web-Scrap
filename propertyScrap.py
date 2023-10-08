import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict



url = 'https://www.property.ie/property-to-let/dublin/price_international_rental-onceoff_standard/beds_3'

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
    response = httpx.get(url, follow_redirects=True)
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
    results = []
    for house in houses:
        new_house = Houses(
            house.css_first("a[href]").text(),
            house.css_first("h4").text(),
            house.css_first("a").attributes.get('href'),

        )
        print(new_house)

def scrap(newUrl):
    try:
        print(newUrl)
        response = httpx.get(newUrl,follow_redirects=True,headers=headers)
        response.raise_for_status()  
        html = HTMLParser(response.text)
        parse(html)
    except httpx.HTTPError as err:
       
        print(f"HTTP error occurred: {err}")

def makeUrl(url,max):
    for i in range(1, max + 1):
        newUrl = f"{url}/p_{i}"
        scrap(newUrl)

def main():
    html = setup(url)
    max  = int(getMax(html))
    makeUrl(url,max)

if __name__ == '__main__':
    main()

