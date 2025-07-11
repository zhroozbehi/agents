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

# MAGIC %md
# MAGIC ## Read Embeded Data

# COMMAND ----------

df = spark.table(emb_dir).toPandas()
print(f"Embeding length: {len(df['embedding'].iloc[0])}")
df.head(3)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Vector Index

# COMMAND ----------

vsc = VectorSearchClient()
vector_search_endpoint_name = "vector-search-churn-endpoint"

# COMMAND ----------

vsc.create_endpoint(
    name=vector_search_endpoint_name,
    endpoint_type="STANDARD" # or "STORAGE_OPTIMIZED"
)

# COMMAND ----------

endpoint = vsc.get_endpoint(
  name=vector_search_endpoint_name)
endpoint

# COMMAND ----------

# Vector index

embedding_model_endpoint = "databricks-gte-large-en"

# COMMAND ----------

index = vsc.create_delta_sync_index(
  endpoint_name=vector_search_endpoint_name,
  index_name=vs_index_fullname,
  primary_key="chunk_text",
  source_table_name=emb_dir,
  pipeline_type='TRIGGERED',
  embedding_dimension=len(df['embedding'].iloc[0]),
  embedding_vector_column="embedding", # If  embeded
  embedding_source_column=None, # If not embeded
  embedding_model_endpoint_name=embedding_model_endpoint, 
  sync_computed_embeddings=False, 
  columns_to_sync=None
)
index.describe()

# COMMAND ----------

index = vsc.get_index(endpoint_name=vector_search_endpoint_name, index_name=vs_index_fullname)

index.describe()

# COMMAND ----------

# Wait for index to come online. Expect this command to take several minutes.
import time
while not index.describe().get('status').get('detailed_state').startswith('ONLINE'):

 print("Waiting for index to be ONLINE...")
 time.sleep(5)
print("Index is ONLINE")
index.describe()