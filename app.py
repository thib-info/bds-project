"""
Usage of Flask to handle multiple pages with better layout than in Dash
"""

from flask import Flask, render_template

from src.card import get_random_images

app = Flask(__name__, template_folder='templatesFiles', static_folder='staticFiles')


card_bck = get_random_images()

@app.route('/')
def home():
    # Inject data into the HTML template
    data = {
        'title': 'Home Page',
        'message': 'Welcome to the home page!',
        'cards_img': card_bck
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


if __name__ == '__main__':
    app.run(debug=True)
