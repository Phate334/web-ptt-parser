# -*- coding:utf-8 -*-
from PTTparser import parse_board, parse_article

meta, articles = parse_board('https://www.ptt.cc/bbs/Gossiping/index.html')
print(meta, articles)

meta, push_msg = parse_article(articles[1]['link'])
print(meta, push_msg)