
import os
import time
from pinecone import (Pinecone, ServerlessSpec,CloudProvider,AwsRegion,VectorType)
from dotenv import load_dotenv
import torch
from prepare_data import prepare_data
from utils.embedding import query
load_dotenv()

#Vector db pinecone setup
pc = Pinecone(os.environ.get("PINECONE_API_KEY"))
index_name = "ragproj-v1"
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud= CloudProvider.AWS,
            region=AwsRegion.US_EAST_1
        ), 
        vector_type=VectorType.DENSE
    )
#connect to the index
index = pc.Index(index_name)
time.sleep(1)
index.describe_index_stats()
prepare_data(index)

input = input("Please Enter your query\n")
query(input, index)
# Base LM ? 
# Hugging face token
# break document into chunks/convert into embeddings and store in a vector db. 
#ReAct framework : Reason/ Action - what about COT, lets keep it too. 
#Scale of context/data for RAG? 

# pinecone
# langchain
# huggingface
# v2: fastapi if complete fullstack app
# Dockerrise. 




