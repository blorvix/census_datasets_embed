import json
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# from transformers import AutoTokenizer
# tokenizer = AutoTokenizer.from_pretrained("nomic-ai/nomic-embed-text-v1")

embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url='https://tableauai1014522.tableauextension.net')
vector_store = Chroma(
    collection_name="census_datasets",
    embedding_function=embeddings,
    persist_directory="./chroma_census_db/census_datasets",
)

documents = []

with open('data/census_data.json', 'r') as file:
    census_data = json.load(file)

def adjust_category(category):
    tags = category.split('/')
    month_short = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    month_long = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    for index, ms in enumerate(month_short):
        if ms in tags:
            tags.append(month_long[index])
            break
    return ' '.join(tags * 3)

for i in range(len(census_data)):
    index = i + 1
    print(index)
    
    item = census_data[i]
    if item['year'] is None:
        del item['year']

    text = 'Title: {title}\nCategory/Date: {category}\nDescription: {description}'.format(
        title=item['title'],
        description=item['description'],
        category=adjust_category(item['category'] + '/mar'),
    )
    if text is not None:
        documents.append(Document(
            page_content=text,
            metadata=item,
            id=index,
        ))

vector_store.add_documents(documents=documents)