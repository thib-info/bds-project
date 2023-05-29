import json
import os
import random


"""
    Pick 5 random images when the application is started
    The images are picked randomly in each folder of the ./img folder
"""
def get_random_images(nbr: int) -> list:
    folder_path = './staticFiles/img/'
    random_files = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if root != folder_path:
                file_path = "." + os.path.join(root, file)
                random_files.append(file_path)

    random_files = random.sample(random_files, nbr)

    return random_files




def get_transcode(paths: list) -> list:
    ids = []
    for path in paths:
        transcode = path.split("-transcode-")[1].split(".")[0]
        ids.append(transcode)

    return ids


def get_folders_name(paths: list) -> list:
    folders_name = []
    for path in paths:
        folder = path.split('/')[3]
        folder = folder.split('\\')[0]
        folders_name.append(folder)

    return folders_name


def get_img_details(paths: list) -> list:
    codes = get_transcode(paths)
    folders = get_folders_name(paths)

    details = []
    for i in range(len(paths)):
        details.append([folders[i], codes[i]])

    return details


def get_image_file_path(details: list) -> str:
    folder = details[0]
    code = details[1]
    folder_path = './datasets/collections/' + folder

    if folder == 'alijn':
        file_name = "hva--" + code.split("_")[0] + ".json"
    elif folder == 'design':
        file_name = "dmg--" + code.split("$")[0] + ".json"
    elif folder == 'archief':
        file_name = "archiefgent--" + code + ".json"
    elif folder == 'industrie':
        file_name = "industriemuseum--" + code + ".json"
    elif folder == 'stam':
        file_name = "stam--" + code + ".json"
    else:
        return ""

    file_path = folder_path + "/" + file_name

    return file_path


def get_img_name(file_path: str) -> str:
    with open(file_path) as file:
        data = json.load(file)

    name = data["title"][0]["value"]

    return name


def get_img_id(file_path: str) -> str:
    with open(file_path) as file:
        data = json.load(file)

    img_id = data["id"]

    return img_id


"""
    Send back the following information
    [[files_id], [files_name], [files_paths]]
"""
def get_details_imgs(paths: list) -> list:

    details = get_img_details(paths)
    files_path = []

    for detail in details:
        files_path.append(get_image_file_path(detail))

    files_names = []
    files_id = []
    for file_path in files_path:
        files_names.append(get_img_name(file_path))
        files_id.append(get_img_id(file_path))

    return [files_id, files_names, files_path]


def generateCardHtml(card_id, card_name, card_path, card_bck) -> str:
    html_content = f'''
    <div id="{card_id}" class="tphoto card hidden" file_path={card_path} style="background-image: url({card_bck}); background-size: cover; background-position: center;">
        <div class="tname">{card_name}, <span class="age">27</span></div>
        <div class="tinfo"><i class="fa fa-book" aria-hidden="true"> 0</i><i class="fa fa-users" aria-hidden="true"> 0</i></div>
    </div>
    '''

    return html_content
