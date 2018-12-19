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


def get_metadata_from(url):

    def parse_next_link(doc):
        html = HTML(html=doc)
        controls = html.find('.action-bar a.btn.wide')
        link = controls[1].attrs.get('href')
        return urllib.parse.urljoin(domain, link)

    resp = fetch(url)
    post_entries = parse_article_entries(resp.text)
    next_link = parse_next_link(resp.text)

    metadata = [parse_article_meta(entry) for entry in post_entries]
    return metadata, next_link


def get_paged_meta(url, num_pages):
    collected_meta = []

    for _ in range(num_pages):
        posts, link = get_metadata_from(url)
        collected_meta += posts
        url = urllib.parse.urljoin(domain, link)

    return collected_meta

"""
def partA(key):
    resp = fetch(start_url)
    post_entries = parse_article_entries(resp.text)
    for entry in post_entries:
        meta = parse_article_meta(entry)
        pretty_print(meta['push'], meta['title'], meta['date'], meta['author'])

def partB():
    metadata = get_paged_meta(start_url, num_pages=5)
    for meta in metadata:
        pretty_print(meta['push'], meta['title'], meta['date'], meta['author'])

def partC():

    def get_posts(metadata):
        post_links = [
            urllib.parse.urljoin(domain, meta['link'])
            for meta in metadata if 'link' in meta]

        with Pool(processes=8) as pool:
            contents = pool.map(fetch, post_links)
            return contents

    start = time.time()

    metadata = get_paged_meta(start_url, num_pages=2)
    resps = get_posts(metadata)

    print('花費: %f 秒' % (time.time() - start))

    print('共%d項結果：' % len(resps))
    for post, resps in zip(metadata, resps):
        print('{0:^3} {1} {2: <15} {3}, 網頁內容共 {4} 字'.format(
            post['push'], post['date'], post['author'], post['title'], len(resps.text)))
"""
def list_all(url):
    resp = requests.get(url, cookies={'over18': '1'})
    post_entries = parse_article_entries(resp.text)
    out = ""
    for entry in post_entries:
        meta = parse_article_meta(entry)
        out += pretty_print(meta['push'], meta['title'], meta['date'], meta['author'], meta['link']) + '\n'
    if out:
        return out
    else:
        out = '無相符搜尋結果'
        return out

def search(url,key):
    resp = requests.get(url, params={'q': key}, cookies={'over18': '1'})
    post_entries = parse_article_entries(resp.text)
    out = ""
    for entry in post_entries:
        meta = parse_article_meta(entry)
        out += pretty_print(meta['push'], meta['title'], meta['date'], meta['author'], meta['link']) + '\n'
    if out:
        return out
    else:
        out = '無相符搜尋結果'
        return out

def search_article(url,key):
    resp = requests.get(url, params={'q': 'thread:'+str(key)}, cookies={'over18': '1'})
    post_entries = parse_article_entries(resp.text)
    out = ""
    for entry in post_entries:
        meta = parse_article_meta(entry)
        out += pretty_print(meta['push'], meta['title'], meta['date'], meta['author'], meta['link']) + '\n'
    if out:
        return out
    else:
        out = '無相符搜尋結果'
        return out

def search_author(url,key):
    resp = requests.get(url, params={'q': 'author:'+str(key)}, cookies={'over18': '1'})
    post_entries = parse_article_entries(resp.text)
    out = ""
    for entry in post_entries:
        meta = parse_article_meta(entry)
        out += pretty_print(meta['push'], meta['title'], meta['date'], meta['author'], meta['link']) + '\n'
    if out:
        return out
    else:
        out = '無相符搜尋結果'
        return out

def search_score(url,key):
    resp = requests.get(url, params={'q': 'recommend:'+str(key)}, cookies={'over18': '1'})
    post_entries = parse_article_entries(resp.text)
    out = ""
    for entry in post_entries:
        meta = parse_article_meta(entry)
        out += pretty_print(meta['push'], meta['title'], meta['date'], meta['author'], meta['link']) + '\n'
    if out:
        return out
    else:
        out = '無相符搜尋結果'
        return out

domain = 'https://www.ptt.cc/'
start_url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
search_url = 'https://www.ptt.cc/bbs/Gossiping/search'


#if __name__ == '__main__':
    #search(search_url,'問卦')
    #search_article(search_url,'[臉書] 林筱淇 12/18')
    #search_author(search_url,'XXXXGAY')
    #search_score(search_url,'100')
