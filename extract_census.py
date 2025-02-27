from bs4 import BeautifulSoup
import json
import os
import requests

CENSUS_HTML_PATH = 'data/Census Data API_ _data.html'
CENSUS_RAW_JSON_FILE_PATH = 'data/census_raw_data.json'
CENSUS_JSON_FILE_PATH = 'data/census_data.json'
CENSUS_VARIABLES_DIR_PATH = 'census_variables'
INVALID_CATEGORIES = ['2022/cps/unempins/may', '2022/ecnbridge1', '2022/ecnbridge2', '2022/ecncomp']


def parse_html_to_json(html_path):
    """Parse the HTML table content to JSON"""
    # Parse HTML content
    with open(html_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the table
    table = soup.find('table')
    
    # Get column headers
    headers = []
    for th in table.find('thead').find_all('th'):
        headers.append(th.text.strip())
    
    # Get table data
    table_data = []
    for row in table.find('tbody').find_all('tr'):
        row_data = {}
        for index, cell in enumerate(row.find_all('td')):
            # Handle links in cells
            if cell.find('a'):
                row_data[headers[index]] = {
                    'text': cell.text.strip(),
                    'href': cell.find('a')['href']
                }
            else:
                row_data[headers[index]] = cell.text.strip()
        table_data.append(row_data)
    
    return table_data


def extract_dataset_info(item):
    extracted_info = {
        'title': item['Title'],
        'description': item['Description'],
        'year': item['Vintage'] if item['Vintage'] != 'N/A' else None,
        'dataset_name': item['Dataset Name'].replace('› ', '/'),
        'variables_json_url': item['Variable List']['href'][:-4] + 'json',
        'data_api_url': item['API Base URL']['href']
    }

    extracted_info['category'] = (extracted_info['year'] + '/' if extracted_info['year'] != None else '') + extracted_info['dataset_name']
    
    return extracted_info


def download_variables_json(url, category):
    filepath = CENSUS_VARIABLES_DIR_PATH + '/' + category.replace('/', '_') + '.json'

    if os.path.exists(filepath):
        return

    response = requests.get(url)
    try:
        data = response.json()
    except:
        print(f"Error: {url}")
        print(response.text)
        return
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def main():
    datasets_raw_list = parse_html_to_json(CENSUS_HTML_PATH)
    with open(CENSUS_RAW_JSON_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(datasets_raw_list, file, indent=2)

    datasets_list = []
    for item in datasets_raw_list:
        extracted_item = extract_dataset_info(item)
        if extracted_item['category'] in INVALID_CATEGORIES:
            continue
        download_variables_json(extracted_item['variables_json_url'], extracted_item['category'])
        datasets_list.append(extracted_item)

    with open(CENSUS_JSON_FILE_PATH, 'w') as file:
        json.dump(datasets_list, file, indent=2)

if __name__ == "__main__":
    main()
