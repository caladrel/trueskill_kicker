import urllib
import urllib2
from bs4 import BeautifulSoup
import re

url2 = raw_input("Enter URL:\n")


def open_soup(url, data=None):
    baseurl = 'http://' + url2 + '/kicker/index.php'
    return BeautifulSoup(urllib2.urlopen(baseurl + url, data=data))


def scrape_player_ids():
    soup = open_soup('?p=matches&a=enter')
    options = soup.find_all('select')[2].find_all('option')
    return {o['value']: o.string for o in options}


def scrape_matches(history=False, player=None):
    url = '?p=matches'
    data = None
    if history:
        url += '&a=history'
        if player is not None:
            url += '&s=s'
            data = urllib.urlencode({'player': player})

    soup = open_soup(url, data=data)

    result = []
    for row in soup.find_all('tr'):
        tds = row.find_all('td')
        if len(tds) > 0:
            result.append([td.get_text() for td in tds])

    if history:
        options = {o['value']: o.string for o in soup.find_all('option')}
        return options, result

    return result


def scrape_players():
    soup = open_soup('?p=players')

    result = []
    for row in soup.find_all('tr'):
        tds = row.find_all('td')
        if len(tds) > 0:
            result.append([td.contents[0] if len(td.contents) > 0 else ''
                           for td in tds])
    for row in result:
        link = str(row[2])
        m = re.search(r"id=(\d+)\">(.*)<", link)
        row[2] = (m.group(1), m.group(2))

    return result


def scrape_players_detail(id):
    soup = open_soup('?p=players&a=istats&pid=' + id)
    soup = soup.find(id='content_box')
    return [e.string for e in soup.find_all(['h2', 'li'])]
