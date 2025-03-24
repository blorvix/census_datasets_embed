import json
import uuid

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# from transformers import AutoTokenizer
# tokenizer = AutoTokenizer.from_pretrained("nomic-ai/nomic-embed-text-v1")

INVALID_FIELDS = ['for', 'in', 'ucgid']

# embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url='https://tableauai1014522.tableauextension.net')
# vector_store = Chroma(
#     collection_name=f"census_choices",
#     embedding_function=embeddings,
#     persist_directory=f"./chroma_census_db/census_choices",
# )

# documents = []
# def add_document(text, category, variable, value):
#     global documents
#     documents.append(Document(
#         page_content=text,
#         metadata={
#             'category': category,
#             'variable': variable,
#             'value': value,
#         },
#         id=str(uuid.uuid4()),
#     ))

#     if len(documents) >= 5000:
#         vector_store.add_documents(documents=documents)
#         documents = []

with open('data/census_data.json', 'r') as file:
    census_data = json.load(file)

total = 0
choices = {}

for i in range(len(census_data)):
    item = census_data[i]
    category = item['category']

    variables_json_path = 'census_variables/' + (category.replace('/', '_')) + '.json'
    with open(variables_json_path, 'r') as file:
        variables = json.load(file)
        variables = variables['variables']
        for name, values in variables.items():
            try:
                items = values['values']['item']
                items_count = len(items)
                if items_count <= 100:
                    continue

                # total += items_count
                if name not in choices:
                    choices[name] = {}

                for key, value in items.items():
                    if key not in choices[name]:
                        choices[name][key] = {
                            'categories': set(),
                            'value': value
                        }
                    choices[name][key]['categories'].add(item['category'])

            except:
                pass
    
for name in choices:
    for key in choices[name]:
        choices[name][key]['categories'] = list(choices[name][key]['categories'])
with open('data/census_choices.json', 'w') as file:
    json.dump(choices, file, indent=2)