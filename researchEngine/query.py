import pymilvus
from pymilvus import (
    connections,
    Collection
)
from sentence_transformers import SentenceTransformer
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings)
import time


connection = connections.connect(host="127.0.0.1", port=19530)
# mc = MilvusClient(connections=connection)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
# model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")

collection = Collection(name="acts_db")

QUESTION = "Give me some cases related to suicide?"
QUERY = [QUESTION]

# Before conducting a search, load the data into memory.
collection.load()

# Embed the question using the same encode
embedded_question = model.encode(QUERY)

# Return top k results with AUTOINDEX.
TOP_K = 2

# Run semantic vector search using your query and the vector database.
start_time = time.time()
results = collection.search(
    data=embedded_question, 
    anns_field="embedding", 
    # No params for AUTOINDEX
    param={},
    # Boolean expression if any
    expr="",
    #output_fields=[ "document", "metadata"],
    output_fields=[ "metadata"],  
    limit=TOP_K,
    consistency_level="Eventually")

elapsed_time = time.time() - start_time
print(f"Milvus search time: {elapsed_time} sec")


#for n, hits in enumerate(results):
#    for hit in hits:
#       print("--------------------------------")
#       print(hit)

import re

# Define regex patterns
patterns = {
    'Name of statute': r"Name of statute: (.+?)\s+Section Number:",
    'Section Number': r"Section Number: (.+?)\s+Section Title:",
    'Section Title': r"Section Title: (.+?)\s+Section Text:",
    'Section Text': r"Section Text: (.+?)(?=\s*$)",
}

# Initialize the dictionary to store all extracted information
all_extracted_info = {key: [] for key in patterns.keys()}

# Function to extract information from a single hit
def extract_info(hit):
    extracted_info = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, hit, re.DOTALL)
        if match:
            extracted_info[key] = match.group(1).strip()
        else:
            extracted_info[key] = None
    return extracted_info

# Process all hits
for hits in results:
    for hit in hits:
        hit = str(hit)
        info = extract_info(hit)
        #print(info)
        for key, value in info.items():
            all_extracted_info[key].append(value)

print("Extracted information \n")
print(all_extracted_info)



