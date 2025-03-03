import json

INVALID_FIELDS = ['for', 'in', 'ucgid']

with open('data/census_data.json', 'r') as file:
    census_data = json.load(file)

result = {}

for i in range(len(census_data)):
    print(i)

    item = census_data[i]
    category = item['category']

    variables_json_path = 'census_variables/' + (category.replace('/', '_')) + '.json'
    with open(variables_json_path, 'r') as file:
        variables_data = json.load(file)

        result[category] = [
            {
                'name': name,
                'label': value['label'],
                'predicateType': value.get('predicateType', None)
            }
            for name, value in variables_data['variables'].items()
            if name not in INVALID_FIELDS
        ]

with open('data/census_variables.json', 'w') as file:
    json.dump(result, file, indent=2)