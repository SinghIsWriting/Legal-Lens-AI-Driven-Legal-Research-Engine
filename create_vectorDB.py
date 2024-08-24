import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings)
from langchain_community.vectorstores import milvus
import _csv
from tqdm import tqdm
from langchain_community.vectorstores import Milvus
import pymilvus
from pymilvus import (
    MilvusClient, utility, connections,
    FieldSchema, CollectionSchema, DataType, IndexType,
    Collection, AnnSearchRequest, RRFRanker, WeightedRanker, db
)
import time


connection = connections.connect(host="127.0.0.1", port=19530)
mc = MilvusClient(connections=connection)

# model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1", device='cuda:0') 


def create_milvus_collection(collection_name, dim):
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)
    
    fields = [
    FieldSchema(name='id', dtype=DataType.VARCHAR, description='ids', max_length=100, is_primary=True, auto_id=False),
    FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, description='embedding vectors', dim=dim),
    FieldSchema(name="document", dtype=DataType.VARCHAR, max_length=60000),
    FieldSchema(name="metadata", dtype=DataType.VARCHAR, max_length=20000),
    ]
    schema = CollectionSchema(fields=fields)
    collection = Collection(name=collection_name, schema=schema)

    # create IVF_FLAT index for collection.
    index_params = {
        'metric_type':'L2',
        'index_type':"IVF_FLAT",
        'params':{"nlist":2048}
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    print(f"Successfully created collection: `{collection_name}`")
    return collection

collection = create_milvus_collection('judgement_db', 1024)

_csv.field_size_limit(100000000)
chunksize=20000
chunk_check=0
text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
ids_arr = []
count = 1
refer = 1
length = 0




for new_csv in tqdm(pd.read_csv("judge_database_master_20-23.csv",chunksize=chunksize,encoding="utf-8")):
    counter = 0
    embed_chunks=[]
    chunk_id_reference = []
    reference = "date of judgement: "+new_csv["date of judgment"]+ " " +"case_title: "+new_csv["case title"]
    new_csv=new_csv['all_text']
    print('created references')
    new_csv.to_csv('temp.csv')
    print('temp csv created')
    loader = CSVLoader(file_path="temp.csv", encoding="utf-8", csv_args={'delimiter': ','})
    data = loader.load()
    print('loading done')

    text_chunks = text_splitter.split_documents(data)

    print('split documents')
        #1 generating chunk_id (add MP)
    
    for value in text_chunks:
        value.metadata['row'] += length

    for i, value in enumerate(text_chunks):
        if i < len(text_chunks)-1:
            current_doc_id = value.metadata['row']+chunk_check
            next_doc_id = text_chunks[i+1].metadata['row']+chunk_check
            chunk_id_reference.append(f"{current_doc_id}.{counter}")

            if current_doc_id == next_doc_id:
                counter = counter + 1
                counterif = counter
            else:
                counter = 0
        else:
            if text_chunks[i-1].metadata['row'] == value.metadata['row']:
                current_doc_id = value.metadata['row']+chunk_check
                chunk_id_reference.append(f"{current_doc_id}.{counterif}")
            else:
                current_doc_id = value.metadata['row']+chunk_check
                chunk_id_reference.append(f"{current_doc_id}.{0}")

    print('create chunk IDs')
    for i in range(0,len(chunk_id_reference)):
        text_chunks[i].metadata['chunk_id'] = chunk_id_reference[i]


    for chunks in text_chunks:
        for i in range(0,len(reference)):
            if chunks.metadata["row"] == i + length:
                chunks.metadata["reference"] = reference.iloc[i]
                embed_chunks.append(chunks)
    print('create References')
    
    count += len(ids_arr)
    ids_arr = []
    for i in range(count, count + len(embed_chunks)+1):
        id = 'id'+""+str(i)
        print(id)
        ids_arr.append(id)
    print(f"{refer} ...........")

    length = text_chunks[-1].metadata['row'] + 1
    
    # Define the batch size
    batch_size = 1000

    # List to store embeddings
    embeddings = []

    list_of_strings = [doc.page_content for doc in embed_chunks if hasattr(doc, 'page_content')]

    print('Creating embeddings........................')
    # Iterate over chunks in batches
    for i in tqdm(range(0, len(list_of_strings), batch_size)):
        # Get a batch of chunks
        batch = list_of_strings[i:i+batch_size]
        
        # Encode the batch
        start_time = time.time()
        batch_embeddings = model.encode(batch, device='cuda:0')
        end_time = time.time()
        
        # Extend the list of embeddings with the embeddings of this batch
        embeddings.extend(batch_embeddings)

    print(f"Total embeddings generated: {len(embeddings)}")

    
    # INSERT CHUNK LIST INTO MILVUS

    # Create chunk_list and dict_list in a single loop
    dict_list = []
    for chunk, vector, ids in zip(embed_chunks, embeddings, ids_arr):
        # Assemble embedding vector, original text chunk, metadata.
        chunk_dict = {
            'id': ids,
            'embedding': vector,
            'document': chunk.page_content,
            'metadata': str(chunk.metadata)
        }
        dict_list.append(chunk_dict)


    # batch wise db insertion

    batch_size = 2500

    print('TQDM is initialised')
    print('Inserting in vector database...........................')
    # Create batches
    for i in tqdm(range(0, len(dict_list)-1, batch_size)):
        batch = dict_list[i:i + batch_size]
        collection.insert(batch)
    collection.flush()
    refer += 1
