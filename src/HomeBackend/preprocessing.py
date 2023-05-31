import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace
from pyspark.sql.types import StringType, StructField, StructType

''' Initiate Spark session '''
spark = SparkSession.builder.getOrCreate()


''' Define the schema for the JSON data '''
# schema = StructType([
#     StructField("id", StringType(), nullable=True),

#     StructField("relations", ArrayType(
#         StructType([
#             StructField("label", StringType(), nullable=True),
#             StructField("value", StringType(), nullable=True),
#         ])
#     ), nullable=True),
# ])

''' Function to add value to dictionary given key if it exists, else it create an entry '''


def add_to_dic(dic, label, value):

    if label in dic:
        if value not in dic[label]:
            dic[label] += [value]

    else:
        dic[label] = [value]

    return dic


''' Send relevant information about item '''


def extract_info(file_path):
    ''' Read json file of an item '''
    df = spark.read.json(file_path)

    ''' Title and description columns need extraction and formatting '''
    df = df.withColumn('title', regexp_replace(
        col('title').cast('string'), r'[\[\]\{\}]', ''))
    df = df.withColumn('description', regexp_replace(
        col('description').cast('string'), r'[\[\]\{\}]', ''))

    ''' Collect all values to dictionary, iterate over them to send relevant information to frontend '''
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

            ''' Some items have metadata like H x W x B that needs further extraction'''
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

                ''' Carefully selected columns '''
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


''' Loop over list, check matches and increment'''


def get_similarity(keys, keys_to_match):

    found = 0

    for key in keys:
        if key in keys_to_match:
            found += 1

    return found


''' Find top 5 items similar to the item specififed in the file_path '''


def find_matches(file_path, museum):
    ''' Read item file and convert to dictionary '''
    df = spark.read.json(file_path)
    row = df.collect()[0].asDict()

    ''' Extract relations row and store the keys of each relation'''
    relations = row['relations']
    keys = []

    for relation in relations:
        keys += [relation[1]]

    ''' Read the dataset of the museum coresponding to the item '''
    # Define the folder path
    folder_path = os.path.join('datasets', 'collections', museum)

    # Replace backslashes with forward slashes if running on non-Windows systems
    if not os.name == 'nt':
        folder_path = folder_path.replace('\\', '/')
    df = spark.read.json(folder_path)

    museum_relations = df.select(['relations', 'object_id']).na.drop()
    museum_relations = museum_relations.collect()

    scores = {}

    ''' Loop over each item in the museum's relations  '''
    for i in range(len(museum_relations)):

        keys_to_match = []

        ''' Get the keys of the relations for each item '''
        for relation in museum_relations[i][0]:
            keys_to_match += [relation[1]]

        ''' Compare with keys of original item and get similarity'''
        similarity = get_similarity(keys, keys_to_match)
        
        ''' Store object_id and similarity pair '''
        scores[museum_relations[i][1]] = similarity

    ''' Sort dictionary based on values and get the 5 object's ids with the highest similarity (other than the actual object) '''
    matches = sorted(scores, key=scores.get, reverse=True)[1:6]

    paths = []

    ''' Get full file paths by looping over the list and matching the id to the path '''
    for match in matches:

        id = match.split(":")[1]

        dir = os.listdir(folder_path)

        for file in dir:
            print(file)
            print(folder_path)
            if id in file:
                path = folder_path + '/' + file
                paths.append(path)

    return paths
