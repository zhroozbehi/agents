# Databricks notebook source
# MAGIC %md
# MAGIC ## Imports

# COMMAND ----------

!pip install PyPDF2

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

import os
import PyPDF2
import pandas as pd
import re

# COMMAND ----------

# MAGIC %md
# MAGIC ## Directories

# COMMAND ----------

pdf_dir = 'Data'
exp_dir = '.....'
data_dir = f'{exp_dir}.churn_pdfs'

# COMMAND ----------

# MAGIC %md
# MAGIC ### One time run: Read from current dir

# COMMAND ----------

print(os.listdir('Data'))

# COMMAND ----------

# Read PDF files from Data folder in a df
results = []

for filename in os.listdir('Data'):
    if filename.endswith('.pdf'):
        path = os.path.join('Data', filename)
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        results.append({'filename': filename, 'content': text})

# Create DataFrame
df = pd.DataFrame(results)
df.head()

# COMMAND ----------

spark_df = spark.createDataFrame(df)
spark_df.write.mode("overwrite").saveAsTable(data_dir)