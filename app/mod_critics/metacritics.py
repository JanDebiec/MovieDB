from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import time
import collections
import sys
sys.path.extend(['/home/jan/project/movie_db'])

from app.mod_db.models import Movie, Role, People, Director, Rating, Critic
import app.mod_db.controllers as dbc
import app.mod_db.functions as dbf


# from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
McRating = collections.namedtuple("McRating", "source author rating")



def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, headers=headers, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)



def find_by_class(soup, class_, element_type='div'):
    return soup.find(element_type, attrs={'class': class_})

def get_critics_count(soup):
    count_tag = find_by_class(soup, 'based_on', 'span')
    # extract number from elem
    txt = count_tag.getText()
    elems = txt.split()
    for elem in elems:
        try:
            count = int(elem)
            return count
        except:
            pass
    return 0

def get_ratings_list(soup):
    list_ = []
    count = get_critics_count(soup)
    i = 0
    while i < count:
        try:

            for div in soup.find_all('div', 'review'):
                rating = get_detail_rating(div)
                # review = find_by_class(soup, 'review', 'div')
                # rating = get_detail_rating(review)
                if rating != None:
                    list_.append(rating)
                    i = i + 1
        except:
            break
    return i, list_

def get_mc_rating(soup):
    try:
        rating_tag = find_by_class(soup, 'metascore_w', 'span')
        txt = rating_tag.getText()
        score = int(txt)
        return score
    except:
        return 0

def get_detail_rating(review_class):
    try:
        author = find_by_class(review_class, 'author', 'span').getText()
        source = find_by_class(review_class, 'source', 'span').getText()
        rating = find_by_class(review_class, 'metascore_w', 'div').getText()
        return McRating(source, author, rating)
    except:
        return None

def get_response(mc_name):
    '''

    :param mc_name: movie title in MC format
    :return:
    '''
    # url_root is a template string that used to buld a URL.
    url_root = 'http://www.metacritic.com/movie/{}/critic-reviews'
    response = simple_get(url_root.format(mc_name))
    # response = tools.simple_get('http://www.metacritic.com/movie/the-godfather/critic-reviews')
    if response is not None:
        return response
    log_error('No pageviews found for {}'.format(mc_name))
    return None

def convert_name_to_mc(name):
    name_temp = name.replace(' ', '-')
    mc_name = name_temp.lower()
    return mc_name

# def get_ratings_on_title(mc_title):
#     response = get_response(mc_title)
#     if response is not None:
#         html = BeautifulSoup(response, 'html.parser')

def get_movie_html(movie_obj):
    movie_id = movie_obj.id
    movie_title = movie_obj.titleImdb
    title_mc = convert_name_to_mc(movie_title)
    movie_html = get_response(title_mc)
    return movie_html

def insert_rating_for_movie_from_html(movie_id, movie_html):
    movie_soup = BeautifulSoup(movie_html, 'html.parser')
    count, list_ = get_ratings_list(movie_soup)
    if count > 0:
        for item in list_:
            name = '{} {}'.format(item.author, item.source)
            url = 'http://www.metacritic.com/critic/{}?filter=movies'.format(item.author)
            maxVal = 100.0
            crit_obj = Critic(name=name, url=url, maxVal=maxVal)
            crit_id = dbf.add_critic(crit_obj)
            rat = Rating(movie_id, critic_id=crit_id, value=item.rating)
            dbf.add_rating(rat)