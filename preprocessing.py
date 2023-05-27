''' SPARK 1 '''
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, MapType
from pyspark.sql.functions import col, regexp_replace

spark = SparkSession.builder.getOrCreate()

# Path to folder of json files
folder_path = 'datasets\\collections\\alijn'

# Define the schema for the JSON data
schema = StructType([
    StructField("id", StringType(), nullable=True),
    
    StructField("object_id", StringType(), nullable=True),
    
    StructField("title", ArrayType(
        StructType([
            StructField("value", StringType(), nullable=True),
        ])
    ), nullable=True),
    
    StructField("description", ArrayType(
        StructType([
            StructField("value", StringType(), nullable=True),
        ])
    ), nullable=True),
])

# For modifying schema per metadata
# new_schema = StructType(schema.fields + [
#     StructField("metadata.value", StringType(), nullable=True), 
# ])


df = spark.read.schema(schema).json(folder_path)
df.printSchema()

df = df.withColumn('title', regexp_replace(col('title').cast('string'), r'[\[\]\{\}]', ''))
df = df.withColumn('description', regexp_replace(col('description').cast('string'), r'[\[\]\{\}]', ''))
# df.show(n=40, truncate=True)



# df.write.csv('filename.csv', header=True, mode='overwrite')


''' PANDAS 1 '''
import os
import pandas as pd
import json

# Path to folder
# folder_path = 'datasets\\collections\\design'

# dfs = pd.DataFrame()

# # Paths to nested json object
# object_paths = [['title', 'value'], ['description', 'value']]
# column_names = ['title', 'description']

# for filename in os.listdir(folder_path):
#     if filename.endswith('.json'):
#         file_path = os.path.join(folder_path, filename)
#         with open(file_path, 'r') as file:
#             data = json.load(file)

#         # Define a custom function to extract the specific objects
#         def extract_objects(obj):
#             if isinstance(obj, list):
#                 results = {}
#                 for item in obj:
#                     if item['key'] in column_names:
#                         results[item['key']] = item['value']
#                 return results
#             return None

#         # Extract each object path separately
#         dfs_path = []
#         for path in object_paths:
#             df = pd.json_normalize(data, record_path=path, meta=['id', 'object_id', 'type'], meta_prefix='meta')
#             df[column_names] = df['meta'].apply(extract_objects).apply(pd.Series)
#             dfs_path.append(df)

#         # Concatenate the DataFrames for each path
#         df_combined = pd.concat(dfs_path, ignore_index=True)
#         dfs.append(df_combined)

# combined_df = pd.concat(dfs, ignore_index=True)

# combined_df.to_csv('filename.csv', index=False)

# print(df["metadataCollection"][0])