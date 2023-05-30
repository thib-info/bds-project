import os
import glob
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace, lit
from pyspark.sql.types import StringType, StructField, StructType


spark = SparkSession.builder.getOrCreate()

folder_path = 'datasets\\collections\\'

# Define the schema for the JSON data
schema = StructType([
    StructField("id", StringType(), nullable=True),
    
    StructField("object_id", StringType(), nullable=True),

    # StructField("object_id", StringType(), nullable=True),

    # StructField("title", ArrayType(
    #     StructType([
    #         StructField("value", StringType(), nullable=True),
    #     ])
    # ), nullable=True),

    # StructField("description", ArrayType(
    #     StructType([
    #         StructField("value", StringType(), nullable=True),
    #     ])
    # ), nullable=True),

    # StructField("relations", ArrayType(
    #     StructType([
    #         StructField("label", StringType(), nullable=True),
    #         StructField("value", StringType(), nullable=True),
    #     ])
    # ), nullable=True),
])


# For modifying schema per metadata
# new_schema = StructType(schema.fields + [
#     StructField("metadata.value", StringType(), nullable=True),
# ])



def add_to_dic(dic, label, value):

    if label in dic:
        if value not in dic[label]:
            dic[label] += [value]

    else:
        dic[label] = [value]

    return dic


def extract_info(file_path):

    df = spark.read.json(file_path)
    df = df.withColumn('title', regexp_replace(
        col('title').cast('string'), r'[\[\]\{\}]', ''))
    df = df.withColumn('description', regexp_replace(
        col('description').cast('string'), r'[\[\]\{\}]', ''))

    row = df.collect()[0].asDict()
    dic = {}

    for key in row:

        if key == 'title':
            dic = add_to_dic(dic, 'Titel', row[key][17:])

        elif key == 'object_id':
            dic = add_to_dic(dic, 'Object ID', row[key])

        elif key == 'description':
            dic = add_to_dic(dic, 'Beschrijving', row[key][23:])

        elif key == 'metadataCollection':

            for metadata in row[key]:

                label = metadata[2]
                value = metadata[1][0][4]

                if label == 'hoogte':
                    dic = add_to_dic(dic, 'Hoogte', value)

                elif label == 'breedte':
                    dic = add_to_dic(dic, 'Breedte', value)

                elif label == 'diepte':
                    dic = add_to_dic(dic, 'Diepte', value)

        elif key == 'relations':

            for relation in row[key]:

                label = relation[2]
                value = relation[4]

                if label == 'MaterieelDing.beheerder':
                    dic = add_to_dic(dic, 'Museumnaam', value)

                elif (label == 'vervaardiger' and value != 'onbekend') or 'associatie.persoon' in label:
                    dic = add_to_dic(dic, 'Gemaakt door', value)

                elif label == 'objectnaam':
                    dic = add_to_dic(dic, 'Objectnaam', value)

                elif 'toegekendType' in label:
                    dic = add_to_dic(dic, 'Toegekend type', value)

                elif label == 'materiaal':
                    dic = add_to_dic(dic, 'Materialen', value)

                elif label == 'techniek':
                    dic = add_to_dic(dic, 'Techniek', value)

                elif 'onderwerp' in label:
                    dic = add_to_dic(dic, 'Onderwerp', value)

                elif 'periode' in label:
                    dic = add_to_dic(dic, 'Periode', value)

    return dic


print('\n\n\n---------------------------------------------------')
print('-----------------BEGIN DEBUGGING-------------------')
print('---------------------------------------------------\n\n\n')



def find_matches(file_path, museum):
    
    df = spark.read.json(file_path)
    row = df.collect()[0].asDict()    
    
    relations = row['relations']
    keys = []

    for relation in relations:
        keys += [relation[1]]
    
    
    folder_path = 'datasets\\collections\\' + museum
    
    df = spark.read.json(folder_path)

    museum_relations = df.select(['relations', 'object_id']).na.drop()
    museum_relations = museum_relations.collect()

    scores = {}

    for i in range(len(museum_relations)):
        
        keys_to_match = []
        
        for relation in museum_relations[i][0]:
            keys_to_match += [relation[1]]
                
        similarity = get_similarity(keys, keys_to_match)
        
        if similarity > 0:
            scores[museum_relations[i][1]] = get_similarity(keys, keys_to_match)
        

    matches = sorted(scores, key=scores.get, reverse=True)[1:6]

    print(matches)
    return matches


def get_similarity(keys, keys_to_match):
    
    found = 0
    
    for key in keys:
        if key in keys_to_match:
            found += 1
    
    return found
    

find_matches('datasets\collections\stam\stam--S.0180.json', 'stam')