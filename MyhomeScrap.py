import requests
import json
import pandas as pd

url = 'https://api.myhome.ie/search'  # Replace with the actual API endpoint URL

results = []

def saveJson(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def saveCsv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename)

for i in range(20):
    payload = {
        "ApiKey": "4284149e-13da-4f12-aed7-0d644a0b7adb",
        "CorrelationId": "22fade32-8266-4c26-9ea7-6aa470a30f07",
        "RequestTypeId": 2,
        "RequestVerb": "GET",
        "Endpoint": url,
        "Page": i,
        "PageSize": 20,
        "SortColumn": 2,
        "SortDirection": 2,
        "Url": "https://www.myhome.ie/rentals/ireland/property-to-rent"
    }

    response = requests.get(url, params=payload)
    if response.status_code == 200: 
        data = response.json()  
        print(data)
        saveJson(data, f'results_{i}.json')
        results.append(data)

    else:
        print('Error:', response.status_code)
    
saveCsv(results, 'results.csv')

