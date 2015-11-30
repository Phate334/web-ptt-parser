# -*- coding:utf-8 -*-
"""this parser can capture board and post data from web ptt.
"""
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
        
    def get_post_list(self, url):
        """url: get post information from this board url.
        return: dict, list
                page_meta:{"prev":"previous page url","next":"next page url"}
                result:[{"":""},...]
        """
        result = []
        soup = self.get_soup(url)
        if not soup:
            return (None, None)
        ### post list parser ###
        post_div = soup.find_all(class_="r-ent")
        for post in post_div:
            temp = {}
            temp["nrec"] = post.find(class_="nrec").get_text()  # 推文數
            temp["mark"] = post.find(class_="mark").get_text()  # 標記
            temp["title"] = post.find(class_="title").get_text()  # 標題
            temp["url"] = self.ptt_host + post.find("a")["href"] if post.find("a") else None  # 文章網址
            temp["date"] = post.find(class_="date").get_text()  # 日期
            temp["author"] = post.find(class_="author").get_text()  # 作者
            result.append(temp)
        ### Previous & Next page url###
        page_meta = {}
        page_meta["prev"] = soup.find(text=u"‹ 上頁").parent.get("href")
        page_meta["prev"] = self.ptt_host + page_meta["prev"] if page_meta["prev"] else None
        page_meta["next"] = soup.find(text=u"下頁 ›").parent.get("href")
        page_meta["next"] = self.ptt_host + page_meta["next"] if page_meta["next"] else None
        return (page_meta, result)

if __name__ == "__main__":
    ptt = PTT()
    meta, posts = ptt.get_post_list("https://www.ptt.cc/bbs/Gossiping/index.html")