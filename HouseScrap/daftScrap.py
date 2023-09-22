import requests
import chompjs
import json
from selectolax.parser import HTMLParser
import pandas as pd

url = 'https://www.daft.ie/property-for-rent/dublin/houses?numBeds_to=3&numBeds_from=3&pageSize=20&from=0'  # Replace with the actual API endpoint URL

results = []

def saveJson(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def saveCsv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename)

def Setup(url):
    response = requests.get(url)
    html = HTMLParser(response.text)
    return html

def HowManyResults(html):
    data = html.css("script[type='application/json']")
    for i in data: 
        new = chompjs.parse_js_object(i.text())
        total = new['props']['pageProps']['paging']['totalResults']
        print(total)
        return total

def getData(url,filename):
    print(f"On url -> {url}")
    response = requests.get(url)
    html = HTMLParser(response.text)
    data = html.css("script[type='application/json']")
    for i in data: 
        new = chompjs.parse_js_object(i.text())
        total = new['props']['pageProps'] 
        saveJson(total,filename)

def ConstructUrl(total):
    sub = total % 10
    even = total - sub + 20
    x = 20
    while x < even:
        url = f"https://www.daft.ie/property-for-rent/dublin/houses?numBeds_to=3&numBeds_from=3&pageSize=20&from={x}"
        filename = f'results_draft_{x}.json'
        getData(url,filename)
        x = x  + 20 
    print(total)

if __name__ == "__main__":
    html = Setup(url)
    total = HowManyResults(html)
    ConstructUrl(total)
