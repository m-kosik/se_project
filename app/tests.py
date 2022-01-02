from bs4 import BeautifulSoup
import pytest
import requests

from utils.utils import User, NoUserError, count_total_stars

def test_real_user_intialization():
    my_user = User('m-kosik')
    assert my_user.username == 'm-kosik'
    assert my_user.limit_reached == False

def test_no_user_exception():
    with pytest.raises(NoUserError):   
        my_user = User('very_weird_name_qwertyuiop')
        my_user.get_all_data(show_languages='n')


def test_repo_retrieval():
    my_user = User('m-kosik')
    my_user.get_all_data(show_languages='n')
    empty_user = User('AlinaBaranowska')
    empty_user.get_all_data(show_languages='n')
    assert my_user.repositories_to_stars
    assert not empty_user.repositories_to_stars

def test_loading_many_pages():
    my_user = User('kfinc')
    my_user.get_all_data(show_languages='n')
    if not my_user.limit_reached:
        assert len(my_user.repositories_to_stars) > 30


def test_total_star_count():
    star_dictionary = {'repo1': 2, 'repo2': 3, 'repo3': 5}
    assert count_total_stars(star_dictionary) == 10
    assert count_total_stars({}) == 0


def test_language_retrieval():
    my_user = User('m-kosik')
    my_user.get_all_data(show_languages='y')
    assert 'Python' in my_user.total_language_use_in_bytes.keys()
    assert 'Jupyter Notebook' in my_user.total_language_use_in_bytes.keys()
    
def test_languages_from_empty_repo():
    empty_repo = requests.get('https://github.com/alina-baranowska/Wine_quality_kaggle_challenge') 
    soup = BeautifulSoup(empty_repo.content,'html5lib')
    languages = User.find_used_languages_by_percent(soup)
    assert not languages
