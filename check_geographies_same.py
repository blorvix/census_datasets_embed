import json

with open('data/census_datasets_core.json') as f:
    census_datasets_core = json.load(f)

with open('data/census_datasets_geographies.json') as f:
    census_datasets_geographies = json.load(f)

month_short = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

for core_category, info in census_datasets_core.items():
    geography = None
    last_category = None
    for year_month in info['year_month']:
        category = core_category
        if 'year' in year_month:
            category = year_month['year'] + '/' + category
        if 'month' in year_month:
            category = category + '/' + month_short[year_month['month'] - 1]

        dataset = census_datasets_geographies.get(category, None)
        if dataset is None:
            continue
        # if not dataset or 'geography' not in dataset:
        #     continue
        # if geography is not None and geography != dataset['geography']:
        #     print(last_category, '!=', category)
        # last_category = category
        # geography = dataset['geography']






