from bs4 import BeautifulSoup
import json

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

def main():
    json_data = parse_html_to_json('Census Data API_ _data.html')
    with open('census_table_data.json', 'w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
