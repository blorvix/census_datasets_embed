import json
import re
from collections import defaultdict

def compare_dataset_titles():
    # Read the JSON file
    with open('data/census_data.json', 'r') as f:
        data = json.load(f)

    # Group datasets by dataset_name
    unique_datasets = defaultdict(list)
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    for dataset in data:
        dataset_name = dataset['dataset_name']
        month_index = None
        for index, month in enumerate(months):
            if dataset_name.endswith(month):
                month_index = index + 1
                dataset_name = dataset_name.replace('/' + month, '')
                break

        # Check for SIPP panel datasets
        # if re.match(r'sipp/(?:topical|core|topicaled|topicaledex|topicalres|topicalex)/\d{4}panel/wave\d', dataset_name):
        #     if not re.match(r'Wave \d+ Survey of Income and Program Participation - \d{4} Panel: ', dataset['title']):
        #         print(f"Found SIPP panel dataset: {dataset_name} {dataset['title']}")
        #     continue

        item = {}
        if dataset['year'] is not None:
            item['year'] = dataset['year']
            dataset_name = dataset_name.replace(dataset['year'], '')
        if month_index is not None:
            item['month'] = month_index

        item['category'] = dataset['category']
        unique_datasets[dataset_name].append(item)

    # Sort the dictionary keys
    unique_datasets = dict(sorted(unique_datasets.items()))
    with open('unique_datasets.json', 'w') as f:
        json.dump(unique_datasets, f, indent=2)
    # print(len(unique_datasets))
    # with open('unique_datasets.txt', 'w') as f:
    #     for dataset_name, dates_list in unique_datasets.items():
    #         f.write(f"{dataset_name}\t\t{', '.join(dates_list)}\n")
    # with open('unique_datasets.json', 'w') as f:
    #     json.dump(unique_datasets, f, indent=2)

    # for dataset in data:
    #     datasets_by_name[dataset['dataset_name']].append(dataset)

    # # Compare titles for each dataset group
    # differences = []
    # for dataset_name, datasets in datasets_by_name.items():
    #     if len(datasets) > 1:  # Only compare if there are multiple datasets
    #         # Get titles without years
    #         titles_without_year = [remove_year_from_title(d['title']) for d in datasets]

    #         # Check if all titles are the same after removing year
    #         if not all(t == titles_without_year[0] for t in titles_without_year):
    #             differences.append({
    #                 'dataset_name': dataset_name,
    #                 'datasets': [
    #                     {
    #                         'year': d['year'],
    #                         'original_title': d['title'],
    #                         'title_without_year': remove_year_from_title(d['title'])
    #                     }
    #                     for d in datasets
    #                 ]
    #             })

    # # Print results
    # if differences:
    #     print("Found differences in titles for the following datasets:")
    #     for diff in differences:
    #         print(f"\nDataset: {diff['dataset_name']}")
    #         for d in diff['datasets']:
    #             print(f"  Year: {d['year']}")
    #             print(f"  Original title: {d['original_title']}")
    #             print(f"  Title without year: {d['title_without_year']}")
    # else:
    #     print("No differences found in titles after removing years.")

if __name__ == "__main__":
    compare_dataset_titles()
