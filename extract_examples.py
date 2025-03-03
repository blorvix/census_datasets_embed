from bs4 import BeautifulSoup
import json
import requests

with open('data/census_data.json', 'r') as file:
    census_data = json.load(file)

result = {}

index = 0
for dataset in census_data:
    index += 1
    print('Checking ', index)

    category = dataset['category']
    examples_url = f'https://api.census.gov/data/{category}/examples.html'
    response = requests.get(examples_url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Locate the table
    table = soup.find('table')

    # Find all <a> tags within the table
    a_tags = table.find_all('a')

    # Extract and print the text of each <a> tag
    examples = []
    for a_tag in a_tags:
        examples.append(a_tag.text.replace('YOUR_KEY_GOES_HERE', ''))

    result[category] = examples

    with open('data/census_examples.json', 'w') as file:
        json.dump(result, file)