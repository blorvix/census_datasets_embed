import json

# Read the JSON file
with open('data/census_data.json', 'r') as file:
    data = json.load(file)

# Sort the data based on dataset_name
sorted_data = sorted(data, key=lambda x: x['dataset_name'])

# Write the sorted data back to a new file with proper indentation
with open('data/census_data_sorted.json', 'w') as file:
    json.dump(sorted_data, file, indent=2)

print("Data has been sorted and saved to data/census_data_sorted.json")
