# Databricks notebook source
# MAGIC %md
# MAGIC ## Imports

# COMMAND ----------

import os
import pandas as pd
import re
import openai

# COMMAND ----------

# MAGIC %md
# MAGIC ## Directories

# COMMAND ----------

pdf_dir = 'Data'
exp_dir = '...'
chnk_dir = f'{exp_dir}.churn_chnk'
emb_dir = f'{exp_dir}.churn_oemb'

# COMMAND ----------

chunked_df = spark.table(chnk_dir).toPandas()

# COMMAND ----------

# MAGIC %md
# MAGIC ## OpenAI Embedding

# COMMAND ----------

# This line now securely gets your API key
openai.api_key = dbutils.secrets.get(scope="Zahra-secrets", key="OPENAI_API_KEY")
print("Key length:", len(dbutils.secrets.get(scope="Zahra-secrets", key="OPENAI_API_KEY")))

# COMMAND ----------

# Expected to add a embedding column, which currently is None for lack of credits
def get_embedding(text, model="text-embedding-ada-002"):
    try:
        response = openai.Embedding.create(
            input=text.replace("\n", " "),
            model=model
        )
        return response["data"][0]["embedding"]
    except Exception as e:
        print(f"Error: {e}")
        return None

# Apply embedding to each chunk (example for pandas DataFrame 'chunked_df')
embeddings = []
for idx, row in chunked_df.iterrows():
    emb = get_embedding(row['chunk_text'])
    embeddings.append(emb)

chunked_df["embedding"] = embeddings
chunked_df