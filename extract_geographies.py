from bs4 import BeautifulSoup
import json
import requests

with open('data/census_datasets_parts.json', 'r') as file:
    census_data = json.load(file)

result = {}

index = 0
for category, dataset in census_data.items():
    index += 1
    print('Checking ', index)

    category = dataset['category']
    examples_url = f'https://api.census.gov/data/{category}/geography.json'
    response = requests.get(examples_url)

    result = response.json()

    dataset['geography'] = result['fips'] if 'fips' in result else []

    with open('data/census_datasets_geographies.json', 'w') as file:
        json.dump(census_data, file, indent=2)