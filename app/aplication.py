from flask import Flask, request, render_template
from utils.utils import *

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    try:
        repository_list, number_of_stars, total_stars = get_all_data(text)
    except NoUserError:
        return "User not found."
    return str(total_stars)
