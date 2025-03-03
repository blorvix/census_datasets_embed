import json

with open('data/census_data.json', 'r') as file:
    census_data = json.load(file)

with open('data/census_examples.json', 'r') as file:
    examples_data = json.load(file)

def get_month(category):
    tags = category.split('/')
    month_short = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    month_long = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    for index, ms in enumerate(month_short):
        if ms in tags:
            return month_long[index]
    return None

result = {}
for dataset in census_data:
    category = dataset['category']
    
    month = get_month(category)
    year = dataset.get('year', None)
    _date = (month or '') + ' ' + (year or '')
    if len(_date) > 1:
        dataset['date'] = _date.strip()
    else:
        if category[-4:].isdigit():
            dataset['date'] = category[-4:]
    
    dataset['example_urls'] = examples_data[category]
    result[category] = dataset
    if len(examples_data[category]) == 0:
        print(category)

with open('data/census_datasets.json', 'w') as file:
    json.dump(result, file, indent=2)