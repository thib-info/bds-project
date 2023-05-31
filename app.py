"""
Usage of Flask to handle multiple pages with better layout than in Dash
"""
import time
import os
from flask import Flask, render_template, request
from src.HomeBackend.card import generateCardHtml, get_random_files, get_image_path, get_file_common_info
from src.HomeBackend.preprocessing import extract_info, find_matches

app = Flask(__name__, template_folder='templatesFiles', static_folder='staticFiles')

data_request = {'request_type': 'None'}
select_card = {}
cards_info = {}
select_card_mapping = {}

correct = False
ind = 0
files_path = []
cards_id = []
cards_name = []
cards_bck = []
while ind < 3:
    try:
        file_path = get_random_files(1)
        [card_id, card_name] = get_file_common_info(file_path)
        card_bck = get_image_path(file_path)

        if not os.path.exists(card_bck[0][1:]):
            continue

        files_path.append(file_path[0])
        cards_id.append(card_id[0])
        cards_name.append(card_name[0])
        cards_bck.append(card_bck[0])

        ind = ind + 1
    except Exception as e:
        print(e)

for file in files_path:
    cards_info[file] = extract_info(file)


@app.route('/api/data')
def get_data():
    return data_request


@app.route('/api/getNewCard')
def get_new_card():
    done = False
    global cards_info
    while done is False:
        try:
            new_card_path = get_random_files(1)
            [new_card_id, new_card_name] = get_file_common_info(new_card_path)
            new_card_bck = get_image_path(new_card_path)
            path_to_check = new_card_bck[0][1:]

            if not os.path.exists(path_to_check):
                continue

            html_content = generateCardHtml(new_card_id[0], new_card_name[0], new_card_path[0], new_card_bck[0])
            data = {
                'request_type': 'newCard',
                'content': html_content
            }

            details = extract_info(new_card_path[0])
            cards_info[new_card_path[0]] = details

            done = True
        except Exception as e:
            print(e)
            done = False

    return data


@app.route('/api/setSuggestions', methods=['POST'])
def getSuggestions():
    global select_card_mapping
    data = request.json

    card_path = data.get('card_path')
    museum = card_path.split('/')[3]
    print(card_path)
    print(museum)
    mappings = find_matches(card_path, museum)
    print(mappings)
    select_card_mapping[card_path] = mappings

    return 'Success'


@app.route('/')
def home():
    data = {
        'title': 'Home Page',
        'message': 'Welcome to the home page!',
        'cards_img': cards_bck,
        'cards_name': cards_name,
        'cards_id': cards_id,
        'files_path': files_path
    }
    return render_template('home.html', data=data)


@app.route('/about')
def about():
    # Inject data into the HTML template
    data = {
        'title': 'About Page',
        'message': 'This is the about page.',
    }
    return render_template('about.html', data=data)


@app.route('/selectedCard')
def selectedCard():
    global select_card

    data = {
        'path': select_card['image_path'],
        'file_path': select_card['path']
    }
    return render_template('selectedCard.html', data=data)


@app.route('/details-card', methods=['POST'])
def process_card():
    global data_request, cards_info, select_card

    data = request.json

    file_path_get = data.get('file_path')
    image_path = data.get('image_path')

    card_info = cards_info[file_path_get]

    data_request = {
        'request_type': 'cardInfo',
        'content': card_info
    }

    select_card['path'] = file_path_get
    select_card['details'] = card_info
    select_card['image_path'] = image_path

    return data_request


if __name__ == '__main__':
    app.run(debug=True)
