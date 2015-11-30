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

### parse_board(url)
example:

        meta, posts = ptt.get_post_list("https://www.ptt.cc/bbs/Gossiping/index.html")
    
meta:

    {
        "prev":"上頁的連結",
        "next":"下頁的連結"
    }
![XXX](http://phate334.github.io/webPTTparser/board-meta.PNG "meta")

posts:[dict(),...]每個元素代表一篇文章，包含如下內容

    {  
        "nrec":"推文數",  
        "mark":"標記",  
        "title":"文張標題",  
        "url":"文張連結，不可用時為None",  
        "date":"日期",  
        "author":"作者"  
    }

### parse_article(url)
原始資料中某些作者會已修改內文的方式來回應其他人，目前還沒有有效的方法表達這些資料，故內文的資料並沒放在回傳的meta中。
example:

        meta, push_info = ptt.parse_article("https://www.ptt.cc/bbs/Gossiping/M.1448856523.A.FB1.html")
meta:

    {
        "author":"ID",
        "name":"括號內的暱稱".
        "board_name":"看板名稱",
        "title":"文章標題",
        "date":"發文時間",
        "ip":[index0為發文時的ip，後面的都是編輯時的ip]
    }
push_info:[dict(),...]  每個元素都是一條回覆訊息

    {
        "tag":"→、推、噓",
        "userid":"ID",
        "content":"回覆內容",
        "time":"回覆時間"
    }
