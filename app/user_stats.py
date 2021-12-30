from flask import Flask, request, render_template, jsonify
from utils.utils import User, NoUserError
from waitress import serve
import json

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
        user = User(username, show_languages)
        final = {}
        final['username'] = user.username
        final['repositories'] = user.repositories_to_stars
        total_stars = sum([stars for _, stars in user.repositories_to_stars.items()])
        final['total_stars'] = total_stars
        final['GH_limit_reached'] = user.limit_reached
        if show_languages:
            final['used_languages'] = user.total_language_use_in_bytes
    except NoUserError:
        return "User not found."
    return render_template('result.html', result=json.dumps(final, sort_keys = False, indent = 2))

serve(app, host='0.0.0.0', port=8080)