# webPTTparser
用 BeautifulSoup4 解析 web PTT 的頁面，包含看板的文章列表及文章的內容等。

## Update
- 2016.11.1

 1. 目前正在重構中，這版改用 requests 取得頁面內容。程式碼裡還有一些待辦還沒寫完。 

 2. 爬取文章後的欄位修改。

## Getting started
    import PTTparser

## API
### parse_board(url)
example:

        meta, articles = ptt.parse_board("https://www.ptt.cc/bbs/Gossiping/index.html")

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

### parse_article(src)
原始資料中某些作者會已修改內文的方式來回應其他人，目前還沒有有效的方法表達這些資料，故內文的資料並沒放在回傳的 meta 中。
example:

        meta, push_info = ptt.parse_article("https://www.ptt.cc/bbs/Gossiping/M.1448856523.A.FB1.html")
meta:

    {
        "author_id":"ID",
        "author_name":"括號內的暱稱".
        "board_name":"看板名稱",
        "title":"文章標題",
        "datetime":"發文時間",
        "ip":[ index 0 為發文時的 ip ，後面的都是編輯時的 ip ]
    }
push_info:[dict(),...]  每個元素都是一條回覆訊息

    {
        "tag":"→、推、噓",
        "userid":"ID",
        "content":"回覆內容",
        "time":"回覆時間"
    }
