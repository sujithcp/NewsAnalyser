import logging
import os
import shutil
import feedparser
from stemming.porter2 import stem

from data_fetcher.fetcher import GetTextFromUrl
from generals import readFile, createFile
from news_classifier import getClassifier

classifier = getClassifier()


def cleanDir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def getUrlList(url):
    try:
        lines = [line.strip() for line in readFile(url).strip().split('\n')]
        # print(lines)
    except Exception as e:
        logging.exception(str(e))
        return []
    return lines


def fetchNews():
    cleanDir('./OUTPUT/')
    URL_LIST = (getUrlList('url_list'))
    if not URL_LIST:
        print("No URLs found ")
        return False
    for url in URL_LIST:
        try:
            fp = feedparser.parse(url)
            print("URL: ", url)
            print("No. of articles : ", len(fp['entries']))
            for i in range(0, len(fp['entries']) - 1):
                title = fp['entries'][i]['title']
                link = fp['entries'][i]['link']
                text = title + "\n" + GetTextFromUrl(link).getText()
                text_stem = [stem(item) for item in text.split()]
                dict = {item: 0 for item in text_stem}
                cat = classifier.classify(dict)
                print(title[:50] + " ... ", "  :  ", cat)
                createFile('./OUTPUT/' + cat, title[:30], text)
        except Exception as e:
            logging.exception(str(e))


fetchNews()
