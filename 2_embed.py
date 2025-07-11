# Databricks notebook source
# MAGIC %md
# MAGIC ## Imports

# COMMAND ----------

import os
import pandas as pd
import re
from sentence_transformers import SentenceTransformer

# COMMAND ----------

# MAGIC %md
# MAGIC ## Directories

# COMMAND ----------

pdf_dir = 'Data'
exp_dir = '...'
chnk_dir = f'{exp_dir}.churn_chnk'
emb_dir = f'{exp_dir}.churn_emb'

# COMMAND ----------

chunked_df = spark.table(chnk_dir).toPandas()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Sentence Transformer Embedding

# COMMAND ----------

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# COMMAND ----------

def get_embedding(text, model=model):
    try:
        this_emb = model.encode(text.replace("\n", " "))
        return this_emb 
    except Exception as e:
        print(f"Error: {e}")
        return None

# # Apply embedding to each chunk (example for pandas DataFrame 'chunked_df')
embeddings = []
for idx, row in chunked_df.iterrows():
    emb = get_embedding(row['chunk_text'])
    embeddings.append(emb)

chunked_df["embedding"] = embeddings
display(chunked_df)

# COMMAND ----------

spark_df = spark.createDataFrame(chunked_df)
spark_df.write.mode("overwrite").option("delta.enableChangeDataFeed", "true").saveAsTable(emb_dir)