# -*- coding:utf-8 -*-
"""this parser can capture board and article data from web ptt.
"""
import re
import urllib
import urllib2

from bs4 import BeautifulSoup

class PTT():
    """
    API for parser web PTT, in BeautifulSoup4-based.
    """
    def __init__(self):
        ###create over 18 opener###
        cookies = urllib2.HTTPCookieProcessor()
        data_encoded = urllib.urlencode({"yes":"yes"})
        self.opener = urllib2.build_opener(cookies)
        self.opener.open("https://www.ptt.cc/ask/over18", data_encoded)
        ###default value###
        self.ptt_host = "https://www.ptt.cc"
        self.re_obj = re.compile(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b")

    def get_soup(self, url, ttl=4):
        """
        when opener time out, default ttl is 4.
        """
        for i in range(ttl):
            try:
                html = self.opener.open(url)
                break
            except urllib2.URLError:
                html = None
        try:
            return BeautifulSoup(html, "lxml")
        except TypeError:
            return None
        
    def parse_board(self, url):
        """url: get article information from this board url.
        return: dict, list
                page_meta:{"prev":"previous page url","next":"next page url"}
                result:[{"":""},...]
        """
        result = []
        soup = self.get_soup(url)
        if not soup:
            return (None, None)
        ### article list parser ###
        list_div = soup.find_all(class_="r-ent")
        for article in list_div:
            temp = {}
            temp["nrec"] = article.find(class_="nrec").get_text()  # 推文數
            temp["mark"] = article.find(class_="mark").get_text()  # 標記
            temp["title"] = article.find(class_="title").get_text()  # 標題
            temp["url"] = self.ptt_host + article.find("a")["href"] if article.find("a") else None  # 文章網址
            temp["date"] = article.find(class_="date").get_text()  # 日期
            temp["author"] = article.find(class_="author").get_text()  # 作者
            result.append(temp)
        ### Previous & Next page url###
        page_meta = {}
        page_meta["prev"] = soup.find(text=u"‹ 上頁").parent.get("href")
        page_meta["prev"] = self.ptt_host + page_meta["prev"] if page_meta["prev"] else None
        page_meta["next"] = soup.find(text=u"下頁 ›").parent.get("href")
        page_meta["next"] = self.ptt_host + page_meta["next"] if page_meta["next"] else None
        return (page_meta, result)

    def parse_article(self, url):
        meta = {}
        push_info = []
        soup = self.get_soup(url)
        if not soup:
            return None
        article_div = soup.find(id="main-container")
        ### Information about this article like content,author,IP...etc  ###
        for node in article_div.find_all(class_=["article-metaline","article-metaline-right"])[:3]:
            tag, value = node.stripped_strings
            tag = "author" if tag==u"作者" else tag
            tag = "board_name" if tag==u"看板" else tag
            tag = "title" if tag==u"標題" else tag
            tag = "date" if tag==u"時間" else tag
            meta[tag] = value
        user_id, name = meta["author"].split(" ")
        meta["author"] = user_id
        meta["name"] = name
        # find editor IP address
        meta["ip"] = []
        for sys_log in article_div.find_all(class_="f2"):
            ip = self.re_obj.findall(sys_log.get_text())
            meta["ip"] += ip
        ### push information include tag,userid,content,time ###
        for node in article_div.find_all(class_="push"):
            temp = {}
            temp["tag"] = node.find(class_="push-tag").get_text().strip()
            temp["userid"] = node.find(class_="push-userid").get_text()
            temp["content"] = node.find(class_="push-content").get_text()
            temp["time"] = node.find(class_="push-ipdatetime").get_text()
            push_info.append(temp)
        return (meta, push_info)

if __name__ == "__main__":
    ptt = PTT()
    # meta, articles = ptt.parse_board("https://www.ptt.cc/bbs/Gossiping/index.html")
    # meta, push_info = ptt.parse_article("https://www.ptt.cc/bbs/Gossiping/M.1448856523.A.FB1.html")