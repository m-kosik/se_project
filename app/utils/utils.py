import requests
from bs4 import BeautifulSoup
import urllib.request, json


def get_all_data(username, show_languages):

    limit_reached = False
    try:
        number_of_stars, total_stars = find_repositories_and_stars_from_api(username)
        if show_languages:
            language_dict = list_languages_from_api(username, number_of_stars)  
        else: 
            language_dict = {}

    except GithubLimitReached:
        limit_reached = True
        try:
            number_of_stars, total_stars = find_repositories_and_stars_without_api(username)
            language_dict = list_languages_without_api(username, number_of_stars) if show_languages else {}
        except NoUserError:
            raise NoUserError
    
    return number_of_stars, total_stars, language_dict, limit_reached


def find_repositories_and_stars_from_api(username):

    number_of_stars = {}
    total_stars = 0

    try:
        with urllib.request.urlopen('https://api.github.com/users/' + username + '/repos') as url:
            data = json.loads(url.read().decode())
            for repo in data:
                number_of_stars[repo['name']] = repo['stargazers_count']
            
            page=1
            while data:
                page = page + 1
                with urllib.request.urlopen('https://api.github.com/users/' + username + '/repos?page=' + str(page)) as url:
                    data = json.loads(url.read().decode())
                    for repo in data:
                        number_of_stars[repo['name']] = repo['stargazers_count']

    except urllib.error.HTTPError:
        raise GithubLimitReached

    return number_of_stars, total_stars


def list_languages_from_api(username, number_of_stars):
    
    total_language_use_in_bytes = {}  
    
    for repo in number_of_stars.keys():
        try:
            with urllib.request.urlopen('https://api.github.com/repos/' + username + '/' + repo + '/languages') as url:
                language_use_in_bytes = json.loads(url.read().decode())
                for language, usage in language_use_in_bytes.items():
                    print(language_use_in_bytes)
                    try:
                        total_language_use_in_bytes[language] += usage
                    except KeyError:
                        total_language_use_in_bytes[language] = usage
        except urllib.error.HTTPError:
            raise GithubLimitReached

    return total_language_use_in_bytes


def find_repositories_and_stars_without_api(username):

    repos = requests.get('https://github.com/' + username + '?tab=repositories') 
    if not repos.ok:
        raise NoUserError
    soup = BeautifulSoup(repos.content,'html5lib')

    repository_list = []
    number_of_stars = {}

    for repo in soup.find_all(class_='wb-break-all'):
        repository_list.append(repo.find('a')['href'])
        repo_name = repo.find('a').text.strip(' \n')
        number_of_stars[repo_name] = 0

    total_stars = 0
    for element in soup.find_all('svg', {'aria-label': 'star'}):
        repo_name = element.parent['href'].split('/')[-2]
        stars = int(element.parent.text.strip('\n '))
        number_of_stars[repo_name] = stars
        total_stars += stars

    for k,v in number_of_stars.items():
        print(f'{k} : {v}')

    return number_of_stars, total_stars


def list_languages_without_api(username, number_of_stars):  

    total_language_use_in_bytes = {}

    for repo in number_of_stars.keys():

        temp_repo = requests.get('https://github.com/' + username + '/' + repo) 
        soup = BeautifulSoup(temp_repo.content,'html5lib')

        try:
            languages_in_percent = find_used_languages_by_percent(soup)
            for language, _ in languages_in_percent.items():
                total_language_use_in_bytes[language] = 'N/A (hourly limit reached)'
        except AttributeError:
            print('There are no languages specified for repository ' + repo)

    return total_language_use_in_bytes
    

def find_used_languages_by_percent(soup):
    languages_dict = {}

    header = soup.find(lambda elm: elm.name == "h2" and "Languages" in elm.text)
    child = header.find_next_siblings()[0].find('span')
    for element in child.find_all('span'):
        language = element['aria-label'].rsplit(' ', 1)[0]
        percent_usage = float(element['aria-label'].rsplit(' ', 1)[1])
        languages_dict[language] = percent_usage
    return languages_dict


class NoUserError(Exception):
    pass

class GithubLimitReached(Exception):
    pass