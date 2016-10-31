# -*- coding:utf-8 -*-
import json
from PTTparser import parse_board, parse_article

meta, articles = parse_board('https://www.ptt.cc/bbs/Gossiping/index.html')
print(json.dumps((meta, articles)))

meta, push_msg = parse_article(articles[1]['link'])
print(json.dumps((meta, push_msg)))