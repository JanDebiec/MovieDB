from bs4 import BeautifulSoup
import time
import collections
import sys
sys.path.extend(['/home/jan/project/movie_db'])
import app.mod_critics.tools as t

McRating = collections.namedtuple("McRating", "source author rating")


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
    response = tools.simple_get(url_root.format(mc_name))
    # response = tools.simple_get('http://www.metacritic.com/movie/the-godfather/critic-reviews')
    if response is not None:
        return response
    tools.log_error('No pageviews found for {}'.format(mc_name))
    return None

def convert_name_to_mc(name):
    name_temp = name.replace(' ', '-')
    mc_name = name_temp.lower()
    return mc_name

def get_ratings_on_title(mc_title):
    response = get_response(mc_title)
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')