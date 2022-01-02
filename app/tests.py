import pytest

from utils.utils import User, NoUserError, count_total_stars
from user_stats import app

def test_real_user_intialization():
    my_user = User('m-kosik')
    assert my_user.username == 'm-kosik'
    assert my_user.limit_reached == False

def test_nouser_exception():
    with pytest.raises(NoUserError):   
        my_user = User('very_weird_name_qwertyuiop')
        my_user.get_all_data()

def test_repo_retrieval():
    my_user = User('m-kosik')
    my_user.get_all_data(show_languages='n')
    assert my_user.repositories_to_stars

def test_language_retrieval():
    my_user = User('m-kosik')
    my_user.get_all_data(show_languages='y')
    assert 'Python' in my_user.total_language_use_in_bytes.keys()
    assert 'Jupyter Notebook' in my_user.total_language_use_in_bytes.keys()
    
def test_total_star_count():
    star_dictionary = {'repo1': 2, 'repo2': 3, 'repo3': 5}
    assert count_total_stars(star_dictionary) == 10
    assert count_total_stars({}) == 0

