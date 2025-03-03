import json
import plotly.express as px
import pandas as pd

# Load the JSON data
with open('data/census_variables.json', 'r') as file:
    data = json.load(file)

# Count the number of items per category
counter = {}
for category, items in data.items():
    items_count = len(items)
    if items_count in counter:
        counter[items_count] += 1
    else:
        counter[items_count] = 1

x_values = []
y_values = []
max_x = max(counter.keys())
count = 0
for x in range(1, max_x + 1):
    if x in counter:
        count += counter[x]
        x_values.append(x)
        y_values.append(count * 100 / len(data))
# sorted_keys = sorted(counter.keys())
# for key in sorted_keys:
#     x_values.append(str(key))
#     y_values.append(counter[key])

# Convert to a DataFrame for easier plotting
df = pd.DataFrame({
    'x': x_values,
    'y': y_values
})

# Create the bar plot using Plotly
# fig = px.bar(df, x='Variables', y='Categories',)  # Add text labels to bars
fig = px.line(df, x='x', y='y', title='Line Chart Example')

# Show the plot
fig.show()