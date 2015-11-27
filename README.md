# webPTTparser
用BeautifulSoup4解析web PTT的頁面，包含看板的文章列表及文章的內容等。

## Getting started
    ptt = PTT()
Instance中包含一個urllib2的opener，以免遇到18禁的看板。

## API
### get_soup(url, ttl=4)
用來取得BeautifulSoup的instance。

url: 目標網址。  
ttl: 回應失敗時重覆嘗試的次數，預設4次。  
return: BeautifulSoup無法解析回應時回傳None。  

### get_post_list(url)
return: (dict, list)  
    meta, posts = PTT.get_post_list("https://www.ptt.cc/bbs/Gossiping/index.html")
    
meta:{"prev":"上頁的連結","next":"下頁的連結"}  
posts:[{""},...]每個元素代表一篇文章，包含如下內容  
    {  
    "nrec":"推文數",  
    "mark":"標記",  
    "title":"文張標題",  
    "url":"文張連結，不可用時為None",  
    "date":"日期",  
    "author":"作者"  
    }
