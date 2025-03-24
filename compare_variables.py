import json
import os

# Step 1: Read the JSON file
with open('data/census_data.json', 'r') as file:
    census_data = json.load(file)

# Step 2: Group items by dataset_name
dataset_groups = {}
for item in census_data:
    dataset_name = item['dataset_name']
    if dataset_name not in dataset_groups:
        dataset_groups[dataset_name] = []
    dataset_groups[dataset_name].append(item)

# Step 3: Compare variables file sizes for items with the same dataset_name
with open('compare.txt', 'w') as output_file:
    for dataset_name, items in dataset_groups.items():
        if len(items) > 1:  # Only compare if there are multiple items with the same dataset_name
            file_sizes = {}
            variables_data = {}
            for item in items:
                # Construct the variables file path
                variables_file_path = f"census_variables/{item['category'].replace('/', '_')}.json"
                # Get the file size
                if os.path.exists(variables_file_path):
                    file_size = os.path.getsize(variables_file_path)
                    file_sizes[item['category']] = file_size
                    with open(variables_file_path, 'r') as f:
                        data = json.load(f)
                        variables_data[item['category']] = data
                else:
                    output_file.write(f"File not found: {variables_file_path}\n")

            # Check if file sizes are different
            unique_sizes = set(file_sizes.values())
            if len(unique_sizes) > 1:
                output_file.write(f"Dataset Name: {dataset_name}\n")
                for category, size in file_sizes.items():
                    output_file.write(f"  Category: {category}, File Size: {size} bytes, variables length: {len(variables_data[category]['variables'])}\n")
