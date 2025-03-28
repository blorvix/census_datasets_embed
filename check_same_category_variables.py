import json

with open('data/census_datasets_core.json', 'r') as f:
    census_datasets_core = json.load(f)

cps_basic_year_month = census_datasets_core['cps/basic']['year_month']

month_names = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

previous_variables = []

for year_month in cps_basic_year_month:
    year = year_month['year']
    month = year_month['month']
    month_name = month_names[month - 1]
    path = f"census_variables/{year}_cps_basic_{month_name}.json"
    with open(path, "r") as f:
        data = json.load(f)

    variables = data["variables"]
    variables = variables.keys()

    if len(previous_variables) > 0:
        new_variables = [v for v in variables if v not in previous_variables]
        removed_variables = [v for v in previous_variables if v not in variables]
        print(year)
        print('new', new_variables)
        print('removed', removed_variables)

    previous_variables = variables
