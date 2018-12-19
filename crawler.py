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
    post_entries = html.find('div.r-ent')
    return post_entries


def parse_article_meta(ent):
	
    meta = {
        'title': ent.find('div.title', first=True).text,
        'date': ent.find('div.date', first=True).text,
    }

    if ent.find('div.nrec', first=True).text:
        meta['push'] = ent.find('div.nrec', first=True).text
    else:
        meta['push'] = "0"

    try:
        meta['author'] = ent.find('div.author', first=True).text
        meta['link'] = ent.find('div.title > a', first=True).attrs['href']
    except AttributeError:
        if '(本文已被刪除)' in meta['title']:
            match_author = re.search('\[(\w*)\]', meta['title'])
            if match_author:
                meta['author'] = match_author.group(1)
        elif re.search('已被\w*刪除', meta['title']):
            match_author = re.search('\<(\w*)\>', meta['title'])
            if match_author:
                meta['author'] = match_author.group(1)
    return meta

def list_all(url):
    order = 0
    resp = requests.get(url, cookies={'over18': '1'})
    post_entries = parse_article_entries(resp.text)
    out = ""
    for entry in post_entries:
        meta = parse_article_meta(entry)
        out += pretty_print(meta['push'], meta['title'], meta['date'], meta['author'], meta['link']) + '\n'
        order = order + 1
        if order >= 20:
            break
    if out:
        return out
    else:
        out = '無相符搜尋結果'
        return out

def search(url,key):
    order = 0
    resp = requests.get(url, params={'q': key}, cookies={'over18': '1'})
    post_entries = parse_article_entries(resp.text)
    out = ""
    for entry in post_entries:
        meta = parse_article_meta(entry)
        out += pretty_print(meta['push'], meta['title'], meta['date'], meta['author'], meta['link']) + '\n'
        order = order + 1
        if order >= 20:
            break
    if out:
        return out
    else:
        out = '無相符搜尋結果'
        return out

def search_article(url,key):
    order = 0
    resp = requests.get(url, params={'q': 'thread:'+str(key)}, cookies={'over18': '1'})
    post_entries = parse_article_entries(resp.text)
    out = ""
    for entry in post_entries:
        meta = parse_article_meta(entry)
        out += pretty_print(meta['push'], meta['title'], meta['date'], meta['author'], meta['link']) + '\n'
        order = order + 1
        if order >= 20:
            break
    if out:
        return out
    else:
        out = '無相符搜尋結果'
        return out

def search_author(url,key):
    order = 0
    resp = requests.get(url, params={'q': 'author:'+str(key)}, cookies={'over18': '1'})
    post_entries = parse_article_entries(resp.text)
    out = ""
    for entry in post_entries:
        meta = parse_article_meta(entry)
        out += pretty_print(meta['push'], meta['title'], meta['date'], meta['author'], meta['link']) + '\n'
        order = order + 1
        if order >= 20:
            break
    if out:
        return out
    else:
        out = '無相符搜尋結果'
        return out

def search_score(url,key):
    order = 0
    resp = requests.get(url, params={'q': 'recommend:'+str(key)}, cookies={'over18': '1'})
    post_entries = parse_article_entries(resp.text)
    out = ""
    for entry in post_entries:
        meta = parse_article_meta(entry)
        out += pretty_print(meta['push'], meta['title'], meta['date'], meta['author'], meta['link']) + '\n'
        order = order + 1
        if order >= 20:
            break
    if out:
        return out
    else:
        out = '無相符搜尋結果'
        return out



