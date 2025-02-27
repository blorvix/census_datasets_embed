import json
import re
import requests
import os

invalid_categories = ['2022/cps/unempins/may', '2022/ecnbridge1', '2022/ecnbridge2', '2022/ecncomp']

def extract_first_two_sentences(text):
    # Split by period followed by space to get sentences
    sentences = text.split('. ')
    # Take first two sentences and rejoin with period and space
    return '. '.join(sentences[:1]) + '.'

def extract_census_info(json_data):
    # Extract required fields
    title = json_data['Title']
    description = json_data['Description']
    vintage = json_data['Vintage']
    dataset_name = json_data['Dataset Name']
    variable_list_link = json_data['Variable List']['href'][:-4] + 'json'
    api_base_url = json_data['API Base URL']['href']
    
    # Create dictionary with extracted information
    extracted_info = {
        'Title': title,
        'Description': description,
        'Year': vintage,
        'Dataset Name': dataset_name.replace('› ', '/'),
        'Variables': variable_list_link,
        'API Base URL': api_base_url
    }

    extracted_info['Category'] = (extracted_info['Year'] + '/' if extracted_info['Year'] != 'N/A' else '') + extracted_info['Dataset Name']
    
    return extracted_info

def get_variable_list(variable_list_link, category):
    filepath = 'census_variables/' + category.replace('/', '_') + '.json'

    if os.path.exists(filepath):
        return
    else:
        response = requests.get(variable_list_link)
        try:
            data = response.json()
        except:
            print(f"Error: {variable_list_link}")
            print(response.text)
            return
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    # invalid_keys = ['for', 'in']
    # items = [(key, value['label']) for key, value in data['variables'].items() if key not in invalid_keys]

def main():
    # Read the JSON file
    with open('census_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    # Extract information for each item
    extracted_items = []
    for item in data:
        extracted_data = extract_census_info(item)
        extracted_items.append(extracted_data)
    
    total_content = ''
    for item in extracted_items:
        content = 'Title: ' + item['Title'] + '\n'
        # content += 'Category: ' + (item['Year'] + '/' if item['Year'] != 'N/A' else '') + item['Dataset Name'] + '\n'
        content += 'Description: ' + item['Description'] + '\n1'
        total_content += content + '\n\n'

        variable_list = get_variable_list(item['Variables'], item['Category'])
        # total_content += 'Fields:' + '\n'
        # for key, value in variable_list:
        #     total_content += key + ': ' + value + '\n'
        # total_content += '\n'

    with open('total_content.txt', 'w', encoding='utf-8') as f:
        f.write(total_content)
    
    # # Save the extracted data to a new JSON file
    # output_file = 'extracted_census_data.json'
    # with open(output_file, 'w', encoding='utf-8') as f:
    #     json.dump(extracted_items, f, indent=2)

    # content = ''
    # for item in extracted_items:
    #     content += f"{item['Title']}, {item['Description']}\n"

    # print(len(re.split('[, ]+', content)))

    # with open('extracted_census_data.txt', 'w', encoding='utf-8') as f:
    #     f.write(content)

if __name__ == "__main__":
    main()
