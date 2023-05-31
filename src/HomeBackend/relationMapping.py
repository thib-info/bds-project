import os
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()


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
            if id in file:
                paths += [(folder_path + file)[6:]]

    return paths