# Databricks notebook source
# MAGIC %md
# MAGIC ## Imports

# COMMAND ----------

# %pip install --upgrade --force-reinstall databricks-vectorsearch
# dbutils.library.restartPython()

# COMMAND ----------

import os
import pandas as pd
import re
from databricks.vector_search.client import VectorSearchClient
from sentence_transformers import SentenceTransformer

# COMMAND ----------

# MAGIC %md
# MAGIC ## Directories

# COMMAND ----------

pdf_dir = 'Data'
exp_dir = '...'
emb_dir = f'{exp_dir}.churn_emb'

vs_index = "churn_index"
vs_index_fullname = f"{exp_dir}.{vs_index}"

# COMMAND ----------

# Initialize client
client = VectorSearchClient()

# The name of your index (from your output above)
index_name = "....churn_index"
endpoint_name = "vector-search-churn-endpoint"
embedding_model_endpoint = "databricks-gte-large-en"
vector_search_endpoint_name = "vector-search-churn-endpoint"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Read Vector Index

# COMMAND ----------

index = client.get_index(endpoint_name=vector_search_endpoint_name, index_name=vs_index_fullname)
index.describe()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Read Embedding Model

# COMMAND ----------

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# COMMAND ----------

# MAGIC %md
# MAGIC ## Embed Query

# COMMAND ----------

query = "What are the health risks for garment workers?"
query_vector = model.encode(query).tolist()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Find Similarity

# COMMAND ----------

all_columns = spark.table(emb_dir).columns

# # Dict type dict_keys(['manifest', 'result', 'debug_info']), all keys dict
results = index.similarity_search(
    query_vector=query_vector,
    columns=all_columns,     
    num_results=5
)


matches = results['result']['data_array']

for row in matches:
    filename = row[0]
    chunk_id = row[1]      # or whatever it represents
    chunk_text = row[2]
    # row[3] is the embedding vector, row[4] is probably score
    print(f"{filename} (chunk_id: {chunk_id})\n{chunk_text[:300]}\n{'-'*40}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Find Similarity Score

# COMMAND ----------

score = row[4]
print(f"{filename} (chunk_id: {chunk_id}) [score: {score}]\n{chunk_text[:300]}\n{'-'*40}")