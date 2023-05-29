import json


def getFile(file_path: str) -> dict:
    try:
        with open(file_path) as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print('JSON file not found')
        return {}
    except Exception as e:
        print(f'Error reading JSON file: {str(e)}')
        return {}


def organizeInfo(content: dict) -> dict:
    details = {}

    # Add the title
    details['title'] = content['title'][0]['value']

    # Add the description
    details['description'] = content['description'][0]['value']

    # Add the height
    print(content['metadataCollection'][1])
    print(content['metadataCollection'][1]['data'])
    details['height'] = content['metadataCollection'][1]['data'][0]['value']

    # Add the width
    details['width'] = content['metadataCollection'][2]['data'][0]['value']

    # Add the depth
    details['depth'] = content['metadataCollection'][3]['data'][0]['value']

    return details


def getCardInfo(file_path: str) -> dict:
    file_content = getFile(file_path)

    # file_info = organizeInfo(file_content)

    file_info = {
        "name": "Thibault",
        "description": "Yes that's me",
        "Museum": "test",
    }

    return file_info
