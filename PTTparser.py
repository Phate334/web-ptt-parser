# -*- coding:utf-8 -*-
import re
from bs4 import BeautifulSoup
import requests

ptt_host = 'https://www.ptt.cc'
ptt_get = lambda url:requests.get(url, cookies={'over18': '1'})

def get_soup(src):
    # TODO: check src's location is on web or file 
    res = ptt_get(src)
    # TODO: TTL
    return BeautifulSoup(res.text, 'html.parser')

def parse_board(url):
    page = get_soup(url)
    page_content = page.find(class_='r-list-container')
    article_list = []
    for article_dom in page_content.find_all(class_=['r-ent', 'r-list-sep']):
        if 'r-list-sep' in article_dom['class']:  # split line
            continue
        if not article_dom.find('a'):  # removed article
            continue
        article = {}
        article['nrec'] = article_dom.find(class_='nrec').text
        article['mark'] = article_dom.find(class_='mark').text
        article['title'] = article_dom.find(class_='title').text.strip()
        article['link'] = ptt_host + article_dom.find('a').get('href')
        article['date'] = article_dom.find(class_='date').text
        article['author'] = article_dom.find(class_='author').text
        article_list.append(article)
    meta = {}
    page_links = page.find(class_='btn-group-paging').find_all('a')
    meta['prev'] = (ptt_host + page_links[1]['href']) if page_links[1].get('href') else None
    meta['next'] = (ptt_host + page_links[2]['href']) if page_links[2].get('href') else None

    return (meta, article_list)

def parse_article(src):
    soup = get_soup(src)
    article_content = soup.find(id='main-container')

    meta_map = {
        u"作者":"author_name",
        u"看板":"board_name",
        u"標題":"title",
        u"時間":"datetime"
    }
    meta = {}
    for node in article_content.find_all(class_=['article-metaline','article-metaline-right']):
        tag, value = node.stripped_strings
        meta[meta_map[tag]] = value
    user_id, name = meta["author_name"].split(" (")
    meta["author_id"] = user_id
    meta["author_name"] = name[:-1]
    push_info = []
    for push in article_content.find_all(class_="push"):
        temp = {}
        temp["tag"] = push.find(class_="push-tag").text.strip()
        temp["userid"] = push.find(class_="push-userid").text
        temp["content"] = push.find(class_="push-content").text
        temp["time"] = push.find(class_="push-ipdatetime").text
        push_info.append(temp)
    return (meta, push_info)
    