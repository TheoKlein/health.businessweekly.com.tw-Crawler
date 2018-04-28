import requests
from bs4 import BeautifulSoup
import datetime
import time
import csv
import random

FILE_NAME = "良醫健康網_藥局"
LAST_PAGE = 399

url = "https://health.businessweekly.com.tw/GSearchDoc.aspx"
headers = {'Cache-Control': "no-cache"}
doctors = []

def logging(msg):
    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    print("[{}] {}".format(now, msg))


def sleeping(maxSec=5):
    '''
        隨機暫停 1 ~ maxSec 秒，避免短時間內大量請求。
        Arg:
        - maxSec: 預設值 10 秒
    '''
    sec = random.randrange(1, maxSec + 1)
    # logging('暫停 {} 秒鐘'.format(sec))
    time.sleep(sec)


def getDoctor(page):
    querystring = {"t":"4" ,"p": page}
    res = requests.request("GET", url, headers=headers, params=querystring)
    soup = BeautifulSoup(res.text, "html5lib")

    for result in soup.findAll("article", {"class":"searchresults"}):
        title = result.find("a", {"class":"title"}).em.string
        left_info = result.findAll("ol")[0]
        right_info = result.findAll("ol")[1]

        tel = left_info.findAll("li")[0].text.replace("電話：", "")
        address = left_info.findAll("li")[1].text.replace("地址：", "")

        recommend = int(right_info.findAll("li")[0].span.text)
        share = int(right_info.findAll("li")[1].text.replace("分享文：", "").replace("篇", ""))
        score = right_info.findAll("li")[2].find("div", {"class": "rating"})['title']
        info = {
            "title": title,
            "tel": tel,
            "address": address,
            "recommend": recommend,
            "share": share,
            "score": score
        }
        doctors.append(info)
    logging("Page {} 已完成".format(page))
    # sleeping()


logging("=== 良醫健康網 - 藥局 ===")
for page in range(1, LAST_PAGE + 1):
    getDoctor(page)


keys = doctors[0].keys()
with open('%s.csv' % FILE_NAME, 'w', encoding="utf8") as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(doctors)
logging("資料已輸出至：{}.csv".format(FILE_NAME))