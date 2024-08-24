# import re
# from .models import LegalDocument, CaseOutcome

# def process_document(document):
#     # Implement document processing logic here
#     title = "Sample Title"
#     content = document.read().decode('utf-8')
#     court = "Sample Court"
#     case_number = "Sample Case Number"
#     date = "2023-08-22"
#     return title, content, court, case_number, date

# def predict_outcome(content):
#     # Implement predictive analytics logic here
#     predicted_outcome = "Plaintiff wins"
#     actual_outcome = "Defendant wins"
#     return predicted_outcome, actual_outcome

import pymilvus
from pymilvus import (
    connections,
    Collection
)
from sentence_transformers import SentenceTransformer
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings)
import time
import re
from .models import LegalDocument, CaseOutcome


from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
#from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from groq import Groq
import os
#os.environ.get("GROQ_API_KEY")

# Define regex patterns
patterns = {
    'Name of statute': r"Name of statute: (.+?)\s+Section Number:",
    'Section Number': r"Section Number: (.+?)\s+Section Title:",
    'Section Title': r"Section Title: (.+?)\s+Section Text:",
    'Section Text': r"Section Text: (.+?)(?=\s*$)",
}

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

def sentence_transformer_model(model):
    # initialize the text to encoding model
    sent_model = SentenceTransformer(model)
    return sent_model



def extract_text_from_pdf(path):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
    # Load all PDFs from a directory
    loader = DirectoryLoader(path, glob="**/*.pdf", loader_cls=PyPDFLoader)
    doc = loader.load()
    return doc


def summarize_pdf(doc,path):
    doc =extract_text_from_pdf(path)
    pdf_text = ""
    for data in doc:
        text = data.page_content
        pdf_text +=text
    client = Groq(
        api_key="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",
    )
    prompt = "Summarize the following text without losing any essential info related to the case:\n" + text

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens = 4098
    )

    return chat_completion.choices[0].message.content



def query(text): #text-> normal chat prompt from chat bar in website
    connection = connections.connect(host="127.0.0.1", port=19530)
    # mc = MilvusClient(connections=connection)

    #model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    # model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")
    model = sentence_transformer_model('sentence-transformers/all-MiniLM-L6-v2')

    collection = Collection(name="acts_db")

    QUESTION = text
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
        output_fields=["metadata"], 
        limit=TOP_K,
        consistency_level="Eventually")
    

    elapsed_time = time.time() - start_time
    print(f"Milvus search time: {elapsed_time} sec")
    #results = str(results)
    # Initialize the dictionary to store all extracted information
    all_extracted_info = {key: [] for key in patterns.keys()}

    # Process all hits
    for hits in results:
        for hit in hits:
            hit = str(hit)
            print(hit)
            info = extract_info(hit)
            #print(info)
            for key, value in info.items():
                all_extracted_info[key].append(value)

    #print("Extracted information \n")
    #print(all_extracted_info)
    return all_extracted_info




# class ResearchEngine:
#     def __init__(self):
#         self.data_sources = ['case_laws', 'statutory_provisions', 'court_rules']

#     def aggregate_and_process_data(self):
#         """
#         Aggregate and process data from various legal data sources.
#         """
#         for source in self.data_sources:
#             # Implement logic to fetch and process data from each source
#             pass

#     def extract_information(self, content):
#         """
#         Extract relevant information, legal principles, and precedents from the given content.
#         """
#         # Implement logic to extract relevant information
#         key_principles = ['Principle A', 'Principle B']
#         precedents = ['Precedent 1', 'Precedent 2']
#         return key_principles, precedents

#     def predict_case_outcome(self, content):
#         """
#         Predict the case outcome based on historical trends and patterns.
#         """
#         # Implement predictive analytics logic
#         predicted_outcome = "Plaintiff wins"
#         return predicted_outcome
    

#     def query(text): #text-> normal chat prompt from chat bar in website
#         connection = connections.connect(host="127.0.0.1", port=19530)
#         # mc = MilvusClient(connections=connection)

#         model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
#         # model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")

#         collection = Collection(name="acts_db")

#         QUESTION = "Give me some cases related to suicide?"
#         QUERY = [QUESTION]

#         # Before conducting a search, load the data into memory.
#         collection.load()

#         # Embed the question using the same encode
#         embedded_question = model.encode(QUERY)

#         # Return top k results with AUTOINDEX.
#         TOP_K = 1

#         # Run semantic vector search using your query and the vector database.
#         start_time = time.time()
#         results = collection.search(
#             data=embedded_question, 
#             anns_field="embedding", 
#             # No params for AUTOINDEX
#             param={},
#             # Boolean expression if any
#             expr="",
#             output_fields=["document"], 
#             limit=TOP_K,
#             consistency_level="Eventually")

#         elapsed_time = time.time() - start_time
#         print(f"Milvus search time: {elapsed_time} sec")
#         results = str(results)
#         return results

#         # for n, hits in enumerate(results):
#         #     for hit in hits:
#         #         print(hit)
#         #pprint.pprint(results)

# def create_summary_from_retrieved_text(results)
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
#from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf_and_encode(path):
    embeddings = []
    batch_size = 100
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
    # Load all PDFs from a directory
    loader = DirectoryLoader(path, glob="**/*.pdf", loader_cls=PyPDFLoader)
    doc = loader.load()
    # return documents
    # loader = PyPDFLoader(
    # "data\1_Harry Potter and The Philosophers Stone.pdf",)

    # doc =loader.load()
    text_chunks = text_splitter.split_documents(doc)

    list_of_strings = [doc.page_content for doc in text_chunks if hasattr(doc, 'page_content')]

    model = sentence_transformer_model('sentence-transformers/all-MiniLM-L6-v2')

    for i in range(0, len(list_of_strings), batch_size):
        # Get a batch of chunks
        batch = list_of_strings[i:i+batch_size]
        
        # Encode the batch
        start_time = time.time()
        batch_embeddings = model.encode(batch, device='cuda:0')
        end_time = time.time()
        
        # Extend the list of embeddings with the embeddings of this batch
        embeddings.extend(batch_embeddings)
    return embeddings
    



# def encode_query(retrieved_text):
#     EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

#     embd = HuggingFaceEmbeddings(
#     model_name=EMBEDDING_MODEL_NAME,
#     multi_process=True,
#     model_kwargs={"device": "cpu"},
#     encode_kwargs={"normalize_embeddings": True},  # set True for cosine similarity
#     )


#     return embd.embed_query(retrieved_text)
