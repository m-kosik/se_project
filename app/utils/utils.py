
import requests
from bs4 import BeautifulSoup
import html5lib
import urllib.request, json

def get_all_data(username):
    repos = requests.get('https://github.com/' + username + '?tab=repositories') 
    if not repos.ok:
        raise NoUserError
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

class NoUserError(Exception):
    pass