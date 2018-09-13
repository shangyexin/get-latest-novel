import logging, time

import requests
from requests.exceptions import ReadTimeout,ConnectionError,RequestException
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                # filename='shengxu.log',
                # filemode='w')
                    )

book_url = "http://www.biqiuge.com/book/4772/"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.23 Safari/537.36"
}


def monitor(html):
    soup = BeautifulSoup(html, 'lxml')
    # print(soup.prettify())
    # with open('index.html', 'w', encoding='utf-8') as f:
    #     f.write(soup.prettify())
    print(soup.title.string)
    last = soup.find_all(attrs={'class': 'last'})
    # print(last)
    last_text = (last[1].contents[1])
    last_url = last_text.get('href')
    title = last_text.get_text()
    logging.info('Last url is ' + last_url)
    logging.info('Last title is ' + title)

    return

if __name__ == '__main__':
    logging.info('Start to get book html.')
    # 每过一分钟刷新一次网页
    while(True):
        try:
            response = requests.get(book_url, headers=headers, timeout=1)
            if (response.status_code == 200):
                logging.info('Get html success.')
                # with open('./original.html', 'w') as f:
                #     f.write(response.text)
                monitor(response.text)
            else:
                logging.warning('Get book html failed, status code is ' + response.status_code)
            # print(response.text)
        except ReadTimeout:
            logging.error("timeout")
        except ConnectionError:
            logging.error("connection Error")
        except RequestException:
            logging.error("error")
        # time.sleep(60)
        break