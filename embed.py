import json
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# from transformers import AutoTokenizer
# tokenizer = AutoTokenizer.from_pretrained("nomic-ai/nomic-embed-text-v1")

# embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url='https://tableauai1014522.tableauextension.net')
# vector_store = Chroma(
#     collection_name="census_datasets_core",
#     embedding_function=embeddings,
#     persist_directory="./chroma_census_db/census_datasets_core",
# )

documents = []

with open('data/census_datasets_grouped.json', 'r') as file:
    census_data_grouped = json.load(file)

with open('data/census_datasets_geographies.json', 'r') as file:
    census_data_geographies = json.load(file)

# def adjust_category(category):
#     tags = category.split('/')
#     month_short = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
#     month_long = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
#     for index, ms in enumerate(month_short):
#         if ms in tags:
#             tags.append(month_long[index])
#             break
#     return ' '.join(tags * 3)

def get_title(title, year):
    if not year:
        return title
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for mon in months:
        title = title.replace(mon + ' ' + str(year) + ' ', '')
    title = title.replace(str(year) + ' ', '')
    title = title.replace(' ' + str(year), '')
    return title

result = {}

index = 0
for core_category, dataset_info in census_data_grouped.items():
    index += 1
    print(index)

    item = census_data_geographies[dataset_info[0]['category']]
    title = get_title(item['title'], item['year'])

    text = 'Title: {title}\nCategory: {category}\nDescription: {description}'.format(
        title=title,
        description=item['description'],
        category=' '.join(core_category.split('/') * 5),
    )

    year_month = []
    for info in dataset_info:
        info_item = {}
        if 'year' in info:
            info_item['year'] = info['year']
        if 'month' in info:
            info_item['month'] = info['month']
        year_month.append(info_item)
    
    result[core_category] = {
        'category': core_category,
        'title': title,
        'description': item['description'],
        'year_month': year_month,
        'variables_embed_part': item['variables_embed_part']
    }

    documents.append(Document(
        page_content=text,
        metadata={
            'core_category': core_category,
            # 'title': title,
            # 'description': item['description'],
            # 'year_month': year_month
        },
        id=index,
    ))
    
    # with open('embed_datasets.txt', 'a') as f:
    #     f.write(text + '\n')
    #     f.write(json.dumps({
    #         'core_category': core_category,
    #         'title': title,
    #         'description': item['description'],
    #         'year_month': year_month
    #     }, indent=2) + '\n\n')

# vector_store.add_documents(documents=documents)

with open('data/census_datasets_core.json', 'w') as file:
    json.dump(result, file, indent=2)