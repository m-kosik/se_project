from os import stat
import requests
from bs4 import BeautifulSoup
import urllib.request, json

class User():
    def __init__(self, username, show_languages):
        self.username = username
        self.repositories_to_stars = {}
        self.limit_reached = False
        self.total_language_use_in_bytes = {}
        self.get_all_data(show_languages)
            

    def get_all_data(self, show_languages):

        try:
            self.find_repositories_and_stars_from_api()
            if show_languages:
                self.list_languages_from_api()  
            else: 
                self.total_language_use_in_bytes = {}

        except GithubLimitReached:
            self.limit_reached = True
            try:
                self.find_repositories_and_stars_without_api()
                if show_languages:
                    self.list_languages_without_api()  
                else:
                    self.total_language_use_in_bytes = {}
            except NoUserError:
                raise NoUserError


    def find_repositories_and_stars_from_api(self):

        try:
            with urllib.request.urlopen('https://api.github.com/users/' + self.username + '/repos') as url:
                data = json.loads(url.read().decode())
                for repo in data:
                    self.repositories_to_stars[repo['name']] = repo['stargazers_count']
                
                page=1
                while data:
                    page = page + 1
                    with urllib.request.urlopen('https://api.github.com/users/' + self.username + '/repos?page=' + str(page)) as url:
                        data = json.loads(url.read().decode())
                        for repo in data:
                            self.repositories_to_stars[repo['name']] = repo['stargazers_count']

        except urllib.error.HTTPError:
            raise GithubLimitReached


    def list_languages_from_api(self):
        
        for repo in self.repositories_to_stars.keys():
            try:
                with urllib.request.urlopen('https://api.github.com/repos/' + self.username + '/' + repo + '/languages') as url:
                    language_use_in_bytes = json.loads(url.read().decode())
                    for language, usage in language_use_in_bytes.items():
                        try:
                            self.total_language_use_in_bytes[language] += usage
                        except KeyError:
                            self.total_language_use_in_bytes[language] = usage
            except urllib.error.HTTPError:
                raise GithubLimitReached


    def find_repositories_and_stars_without_api(self):

        repos = requests.get('https://github.com/' + self.username + '?tab=repositories') 
        if not repos.ok:
            raise NoUserError
        soup = BeautifulSoup(repos.content,'html5lib')

        repository_list = []
        for repo in soup.find_all(class_='wb-break-all'):
            repository_list.append(repo.find('a')['href'])
            repo_name = repo.find('a').text.strip(' \n')
            self.repositories_to_stars[repo_name] = 0

        for element in soup.find_all('svg', {'aria-label': 'star'}):
            repo_name = element.parent['href'].split('/')[-2]
            stars = int(element.parent.text.strip('\n '))
            self.repositories_to_stars[repo_name] = stars


    def list_languages_without_api(self):  

        for repo in self.repositories_to_stars.keys():

            temp_repo = requests.get('https://github.com/' + self.username + '/' + repo) 
            soup = BeautifulSoup(temp_repo.content,'html5lib')

            try:
                languages_in_percent = self.find_used_languages_by_percent(soup)
                for language, _ in languages_in_percent.items():
                    self.total_language_use_in_bytes[language] = 'N/A (hourly limit reached)'
            except AttributeError:
                print('There are no languages specified for repository ' + repo)

    @staticmethod
    def find_used_languages_by_percent(soup):
        languages = {}
        header = soup.find(lambda elm: elm.name == "h2" and "Languages" in elm.text)
        child = header.find_next_siblings()[0].find('span')
        for element in child.find_all('span'):
            language = element['aria-label'].rsplit(' ', 1)[0]
            percent_usage = float(element['aria-label'].rsplit(' ', 1)[1])
            languages[language] = percent_usage
        return languages


class NoUserError(Exception):
    pass

class GithubLimitReached(Exception):
    pass