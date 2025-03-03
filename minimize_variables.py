import json

INVALID_FIELDS = ['for', 'in', 'ucgid']

with open('data/census_variables.json', 'r') as file:
    census_variables = json.load(file)

for category, variables in census_variables.items():
    minimized_path = 'census_variables_minimized/' + (category.replace('/', '_')) + '.json'
    with open(minimized_path, 'w') as file:
        json.dump(variables, file, separators=(',', ':'))
