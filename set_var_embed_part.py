import json

with open('data/census_datasets.json', 'r') as file:
    census_data = json.load(file)

unique_values = {}
unique_keys = set()

current_part_index = 1
current_part_count = 0

max_count = 0

for category, dataset in census_data.items():
    variables_json_path = 'census_variables/' + (category.replace('/', '_')) + '.json'
    with open(variables_json_path, 'r') as file:
        variables = json.load(file)
        
    var_count = len(variables['variables'])

    if current_part_count + var_count >= 40000 and current_part_count > 0:
        # print(current_part_count)
        current_part_index += 1
        current_part_count = 0

    dataset['variables_embed_part'] = current_part_index

    current_part_count += var_count
    max_count = max(max_count, current_part_count)
    # if current_part_count >= 40000:
    #     current_part_index += 1
    #     current_part_count = 0

print(current_part_index, max_count)

with open('data/census_datasets_parts.json', 'w') as file:
    json.dump(census_data, file, indent=2)