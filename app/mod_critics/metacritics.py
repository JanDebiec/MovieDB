from bs4 import BeautifulSoup
import sys
sys.path.extend(['/home/jan/project/movie_db'])
from app.mod_critics import tools as t


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
        score = float(txt)
        return score
    except:
        return 0


def get_detail_rating(review_class):
    try:
        author = find_by_class(review_class, 'author', 'span').getText()
        source = find_by_class(review_class, 'source', 'span').getText()
        rating = find_by_class(review_class, 'metascore_w', 'div').getText()
        return t.McRating(source, author, rating)
    except:
        return None


def get_response(mc_name):
    '''

    :param mc_name: movie title in MC format
    :return:
    '''
    # url_root is a template string that used to buld a URL.
    url_root = 'http://www.metacritic.com/movie/{}/critic-reviews'
    response = t.simple_get(url_root.format(mc_name))
    # response = tools.simple_get('http://www.metacritic.com/movie/the-godfather/critic-reviews')
    if response is not None:
        return response
    t.log_error('No pageviews found for {}'.format(mc_name))
    return None


def convert_name_to_mc(name):
    # ignore some chars ['.', ''', ...]
    # name.strip('.')
    name.replace('.', '')

    name_temp = name.replace(' ', '-')
    mc_name = name_temp.lower()
    mc_name_no_apo = mc_name.replace("'", '')
    mc_name_no_dot = mc_name_no_apo.replace('.', '')
    return mc_name_no_dot


def get_movie_html(movie_obj):
    movie_id = movie_obj.id
    movie_title = movie_obj.titleImdb
    title_mc = convert_name_to_mc(movie_title)
    movie_html = get_response(title_mc)
    return movie_html


def get_rating_list_for_movie(movie_id, movie_html):
    movie_soup = BeautifulSoup(movie_html, 'html.parser')
    count, list_ = get_ratings_list(movie_soup)
    mc_rating = get_mc_rating(movie_soup)
    return mc_rating, count, list_

