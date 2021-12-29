from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import html5lib
import urllib.request, json

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    repository_list, number_of_stars, total_stars = get_all_data(text)
    return str(total_stars)

def get_all_data(username):
    repos = requests.get('https://github.com/' + username + '?tab=repositories') 
    soup = BeautifulSoup(repos.content,'html5lib')
    repository_list, number_of_stars, total_stars = find_repositories_and_stars(soup)
    return repository_list, number_of_stars, total_stars

def find_repositories_and_stars(soup):
    repository_list = []
    number_of_stars = {}

    for repo in soup.find_all(class_='wb-break-all'):
        repository_list.append(repo.find('a')['href'])
        repo_name = repo.find('a').text.strip(' \n')
        number_of_stars[repo_name] = None

    total_stars = 0
    for element in soup.find_all('svg', {'aria-label': 'star'}):
        repo_name = element.parent['href'].split('/')[-2]
        stars = int(element.parent.text.strip('\n '))
        number_of_stars[repo_name] = stars
        total_stars += stars

    for k,v in number_of_stars.items():
        print(f'{k} : {v}')

    return repository_list, number_of_stars, total_stars