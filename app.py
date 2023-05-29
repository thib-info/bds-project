"""
Usage of Flask to handle multiple pages with better layout than in Dash
"""
import time

from flask import Flask, render_template, request
from src.HomeBackend.card import get_random_images, get_details_imgs, generateCardHtml
from src.HomeBackend.getCardInfo import getCardInfo

app = Flask(__name__, template_folder='templatesFiles', static_folder='staticFiles')

data_request = {'request_type': 'None'}

cards_bck = get_random_images(3)
[cards_id, cards_name, files_path] = get_details_imgs(cards_bck)


@app.route('/api/data')
def get_data():
    data_request["time"] = time.localtime()
    return data_request


@app.route('/api/getNewCard')
def get_new_card():
    new_card_bck = get_random_images(1)
    [new_card_id, new_card_name, new_card_path] = get_details_imgs(new_card_bck)

    html_content = generateCardHtml(new_card_id[0], new_card_name[0], new_card_path[0], new_card_bck[0])

    data = {
        'request_type': 'newCard',
        'content': html_content
    }

    return data


@app.route('/')
def home():
    # Inject data into the HTML template
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


@app.route('/details-card', methods=['POST'])
def process_card():
    global data_request
    data = request.json

    card_id = data.get('card_id')
    accepted = data.get('accepted')
    file_path = data.get('file_path')

    if accepted:
        print(f"Card {card_id} has been accepted. With the path to the file: {file_path}")
    else:
        print(f"Card {card_id} has been rejected.")

    """
    card_info = getCardInfo(file_path)
    data_request = {
        'request_type': 'cardInfo',
        'content': card_info
    }
    """

    return 'Success'


if __name__ == '__main__':
    app.run(debug=True)
