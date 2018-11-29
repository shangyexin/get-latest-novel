import time, json, re
import requests
from bs4 import BeautifulSoup

import config
from config import logger


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
                logger.info('%s 没有更新' % bookName)
            # 有更新
            else:
                with open(recordFile, "w") as f:
                    f.write(onlineChapter)
                # 提交给微信公众号服务器
                postToWechat(bookInfo)
    # 第一次没有最新章节记录时
    except IOError as e:
        logger.error(e)
        with open(recordFile, "w") as f:
            f.write(onlineChapter)


def getFromWebsite(bookName, url):
    bookInfo = {'bookName': '', 'latestChapter': '', 'updateTime': '', 'latestUrl': ''}
    novel = requests.get(url, timeout=60)
    novel.encoding = "gbk"
    soup = BeautifulSoup(novel.text, "html.parser")
    last = soup.find_all(attrs={'class': 'last'})
    # 更新时间在第一个last
    updateInfo = last[0].contents[0]
    updateTime = re.search('\d.*$', updateInfo).group(0)
    # print('updateTime is ' + updateTime)
    # 章节在第二个last
    lastText = last[1].contents[1]
    # 最新章节网址
    latestUrl = lastText.get('href')
    # 完整网址
    completeUrl = config.baseOriginUrl + latestUrl
    # 最新章节名
    latestChapter = lastText.get_text()

    bookInfo['bookName'] = bookName
    bookInfo['latestChapter'] = latestChapter
    bookInfo['updateTime'] = updateTime
    bookInfo['latestUrl'] = completeUrl

    logger.info('bookName is ' + bookInfo['bookName'])
    logger.info('latestChapter is ' + bookInfo['latestChapter'])
    logger.info('updateTime is ' + bookInfo['updateTime'])
    logger.info('latestUrl is ' + bookInfo['latestUrl'])

    return bookInfo


def checkUpdate(bookName, url):
    try:
        bookInfo = getFromWebsite(bookName, url)
        checkIfLatest(bookInfo);

    except Exception as e:
        now = time.strftime("%Y-%m-%d %X", time.localtime())
        logger.error("获取最新章节报错" % (now, bookName))


def postToWechat(bookInfo):
    tryCount = 0
    # 重试3次 每次间隔60s
    while (tryCount < 3):
        try:
            response = requests.post(config.updatePostUrl, data=bookInfo)
            if (response.text == 'success'):
                logger.info('Post to wechat server success!')
                break
            else:
                logger.error('Post to wechat server failed, response text is %s' % response.text)
                tryCount = tryCount + 1
        except Exception as e:
            logger.error(e)
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
    logger.info('Start to monitor novel update.')
    runMoniror()
