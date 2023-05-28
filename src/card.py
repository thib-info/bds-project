import os
import random


def get_random_images():
    folder_path = './staticFiles/img/design'

    file_list = os.listdir(folder_path)
    random_files = random.sample(file_list, 5)

    for i, file in enumerate(random_files):
        random_files[i] = '../staticFiles/img/design/' + file

    return random_files
