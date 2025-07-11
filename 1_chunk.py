# Databricks notebook source
# MAGIC %md
# MAGIC ## Imports

# COMMAND ----------

import os
import pandas as pd
import re

# COMMAND ----------

# MAGIC %md
# MAGIC ## Directories

# COMMAND ----------

pdf_dir = 'Data'
exp_dir = '......'
data_dir = f'{exp_dir}.churn_pdfs'
chnk_dir = f'{exp_dir}.churn_chnk'

# COMMAND ----------

# MAGIC %md
# MAGIC ## Read Data

# COMMAND ----------

df = spark.table(data_dir).toPandas()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Chunking

# COMMAND ----------

def chunk_text(text, chunk_size=300, overlap=0):
    """Split text into chunks of `chunk_size` words, with optional overlap."""
    words = re.split(r'\s+', text)
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap  # move by chunk_size, or less if overlapping
    return chunks

# Apply chunking to your extracted DataFrame
chunk_size = 300  # adjust as needed
overlap = 50      # (optional) overlap for more context

chunked_rows = []
for idx, row in df.iterrows():
    filename = row['filename']
    text = row['content']
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    for i, chunk in enumerate(chunks):
        chunked_rows.append({'filename': filename, 'chunk_id': i, 'chunk_text': chunk})

chunked_df = pd.DataFrame(chunked_rows)
chunked_df.head()

# COMMAND ----------

spark_df = spark.createDataFrame(chunked_df)
spark_df.write.mode("overwrite").option("delta.enableChangeDataFeed", "true").saveAsTable(chnk_dir)