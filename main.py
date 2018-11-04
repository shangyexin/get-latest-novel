import logging, time, json, re
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='get-latest-novel.log',
                    filemode='w'
                    )

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.23 Safari/537.36"
}

baseOriginUrl = 'https://www.biqiuge.com'

updatePostUrl = 'http://35.234.33.9/api/novelupdate'


def parseConfig():
    with open("novel.json", "r", encoding='utf-8') as f:
        novelList = json.loads(f.read())

    return novelList


def checkIfLatest(bookInfo):
    onlineChapter = bookInfo['latestChapter']
    bookName = bookInfo['bookName']

    recordFile = './temp/' + bookName + '.txt'
    try:
        with open(recordFile, "r") as f:
            localChapter = f.read()
            # print(localChapter)
            # 没有更新
            if (localChapter == onlineChapter):
                logging.info('%s 没有更新' % bookName)
            # 有更新
            else:
                with open(recordFile, "w") as f:
                    f.write(onlineChapter)
                # 提交给微信公众号服务器
                postToWechat(bookInfo)
    # 第一次没有最新章节记录时
    except IOError as e:
        logging.error(e)
        with open(recordFile, "w") as f:
            f.write(onlineChapter)


def getFromWebsite(bookName, url):
    bookInfo = {'bookName': '', 'latestChapter': '', 'updateTime': '', 'latestUrl':''}
    novel = requests.get(url, timeout=60)
    novel.encoding = "gbk"
    soup = BeautifulSoup(novel.text, "html.parser")
    last = soup.find_all(attrs={'class': 'last'})
    # 更新时间在第一个last
    updateInfo = last[0].contents[0]
    updateTime = re.search('\d.*$',updateInfo).group(0)
    # print('updateTime is ' + updateTime)
    # 章节在第二个last
    lastText = last[1].contents[1]
    # 最新章节网址
    latestUrl = lastText.get('href')
    # 完整网址
    completeUrl = baseOriginUrl + latestUrl
    # 最新章节名
    latestChapter = lastText.get_text()

    bookInfo['bookName'] = bookName
    bookInfo['latestChapter'] = latestChapter
    bookInfo['updateTime'] = updateTime
    bookInfo['latestUrl'] = completeUrl

    logging.info('bookName is ' + bookInfo['bookName'])
    logging.info('latestChapter is ' + bookInfo['latestChapter'])
    logging.info('updateTime is ' + bookInfo['updateTime'])
    logging.info('latestUrl is ' + bookInfo['latestUrl'])

    return bookInfo


def checkUpdate(bookName, url):
    try:
        bookInfo = getFromWebsite(bookName, url)
        checkIfLatest(bookInfo);

    except Exception as e:
        now = time.strftime("%Y-%m-%d %X", time.localtime())
        logging.error("%s  获取 %s 最新章节报错" % now, bookName)


def postToWechat(bookInfo):
    tryCount = 0
    # 重试3次 每次间隔60s
    while (tryCount < 3):
        try:
            response = requests.post(updatePostUrl, data=bookInfo)
            if(response.text == 'success'):
                logging.info('Post to wechat server success!')
                break
            else:
                logging.error('Post to wechat server failed, response text is %s' % response.text)
                tryCount= tryCount + 1
        except Exception as e:
            logging.error(e)
            tryCount = tryCount + 1
        time.sleep(60)


def runMoniror():
    # 获取小说列表
    novelList = parseConfig()

    while (True):
        for book in novelList:
            bookName = (novelList[book]['chineseName'])
            bookUrl = (novelList[book]['bookUrl'])
            checkUpdate(bookName, bookUrl)
            time.sleep(1)
        # 每5分钟查询一次
        time.sleep(360)


if __name__ == '__main__':
    logging.info('Start to monitor novel update.')
    runMoniror()
