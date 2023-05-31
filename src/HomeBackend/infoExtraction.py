from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace

spark = SparkSession.builder.getOrCreate()


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