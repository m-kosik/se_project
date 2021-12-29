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
        stars_in_repos, total_stars = get_all_data(text)
        final = {}
        final['username'] = text
        final['repositories'] = stars_in_repos
        final['total_stars'] = total_stars
        final['used_languages'] = 'lang'
    except NoUserError:
        return "User not found."
    return final
