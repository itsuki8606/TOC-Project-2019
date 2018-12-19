import re
import time
import urllib
from multiprocessing import Pool
from pyshorteners import Shortener

import requests
from requests_html import HTML

from crawler_utils import pretty_print  # noqa


def fetch(url):
    response = requests.get(url, cookies={'over18': '1'})
    return response

def parse_article_entries(doc):
    html = HTML(html=doc)
    post_entries = html.find('div.b-ent')
    return post_entries


def parse_article_meta(ent):
	
    meta = {
        'name': ent.find('div.board-name', first=True).text,
        'title': ent.find('div.board-title', first=True).text,
    }

    if ent.find('div.board-nuser', first=True).text:
        meta['push'] = ent.find('div.board-nuser', first=True).text
    else:
        meta['push'] = "0"

    return meta

def list_hot_board(url):
    order = 0
    resp = requests.get(url, cookies={'over18': '1'})
    post_entries = parse_article_entries(resp.text)
    #out = '看版人氣'.ljust(6) + '看板名稱'.center(8) + '看板描述'.center(10)+'\n'
    out = ""
    for entry in post_entries:
        meta = parse_article_meta(entry)
        string = meta['push'].center(6) + meta['name'].center(20) + meta['title'].ljust(30)
        out += string + '\n'
        order = order + 1
        if order >= 20:
            break        
    if out:
        return out
    else:
        out = '無相符搜尋結果'
        return out

domain = 'https://www.ptt.cc/'
start_url = 'https://www.ptt.cc/bbs/index.html'


#if __name__ == '__main__':
    #list_hot_board(start_url)
    #search_article(search_url,'[臉書] 林筱淇 12/18')
    #search_author(search_url,'XXXXGAY')
    #search_score(search_url,'100')
