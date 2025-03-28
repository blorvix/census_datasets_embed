import json

years = [2015, 2016, 2017, 2018, 2019, 2021]

previous_variables = []

for year in years:
    path = f"census_variables/{year}_pep_population.json"
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
