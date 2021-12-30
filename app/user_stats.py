from flask import Flask, request, render_template
from utils.utils import *

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():

    username = request.form['username']
    show = request.form['show']

    if show == 'y':
        show_languages = True 
    else:
        show_languages = False
    try:
        stars_in_repos, total_stars, language_dict, limit_reached = get_all_data(username, show_languages)
        final = {}
        final['username'] = username
        final['repositories'] = stars_in_repos
        final['total_stars'] = total_stars
        final['GH_limit_reached'] = limit_reached
        if show_languages:
            final['used_languages'] = language_dict
    except NoUserError:
        return "User not found."
    return final
