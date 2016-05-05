'''

Fetch data from the rss feeds and add it to the news corpus
This program is to be executed periodically.
main summery extracted using sumy library

'''
import hashlib
import re
import sqlite3
import threading

import feedparser

from data_fetcher.fetcher import GetTextFromUrl
from generals import readFile

'''
get list of [url,category] from the file urls
If category is specified returns all such lists,

'''

newCount = 0
def getUrlList(category=None):
    lines = [line.strip() for line in readFile('./urls').strip().split('\n')]
    #print(lines)
    if not category:
        return [[i for i in line.split()] for line in lines]
    else:
        line = [[i for i in line.split()] for line in lines]
        line = [i for i in line if i[1] == category]
        print(line)
        return line

'''
get text from the rss links and store it in corresponding folder
file name is derived from the title of the rss feed
skip file write if file already exists
'''


def fetchRss(category=None,name = ""):
    global newCount
    connection = sqlite3.connect('../data/news_data.db')
    cursor = connection.cursor()
    URL_LIST = getUrlList(category)
    if not URL_LIST:
        print("No URLs found ")
        return False
    for url in URL_LIST:
        try:
            fp = feedparser.parse(url[0])
            print("URL: ", url[0])
            print("No. of articles : ", len(fp['entries']))
            for i in range(0, len(fp['entries']) - 1):
                title = fp['entries'][i]['title']
                link = fp['entries'][i]['link']
                datetime = fp['entries'][i]['published'] or ""
                date = re.findall('[0-9]+[ ][A-Za-z]+[ ][0-9]+', datetime)[0] or ""
                time = re.findall('[0-9]+:[0-9]+:[0-9]+', datetime)[0] or ""
                print(name, " --> ", title,link,date,time)
                cursor.execute("select count(*) from News where title = ?", (title,))
                count = int(cursor.fetchone()[0])
                if count != 0:
                    print("Skipping >>> ")
                    continue

                print("Adding to database ",title)
                text = GetTextFromUrl(link).getText()
                #print(text)
                id = hashlib.md5(text.encode('utf-8')).hexdigest()
                print(id)
                cursor.execute("insert into News(id,title,news,category,date,time,link) values(?,?,?,?,?,?,?)", (id, title, text, category, date, time,link,))
                connection.commit()

                newCount += 1
            print(name, " - Done")
        except Exception as e:
            print("Exception occured for ",name)
            print(str(e))
    print("Finished....","New Documents = ",newCount)


'''



for url in URL_LIST:
    try:
        fp = feedparser.parse(url[0])
        for i in range(0, len(fp['entries']) - 1):
            title = fp['entries'][i]['title']
            text = GetTextFromUrl(fp['entries'][i]['link']).getText()
            print(title)
            createFile('../event_data/'+url[1],'/'+title[:15],text+title,replace=False)
            print("Done")
    except:
        print("Exception occured for ")

'''

tsports = threading.Thread(target=fetchRss, args=("sports","t_sports"))
thealth = threading.Thread(target=fetchRss,args=("health","t_health"))
tentertainment = threading.Thread(target=fetchRss,args=("entertainment","t_entertainment"))
ttech = threading.Thread(target=fetchRss,args=("tech","t_tech"))
tbusiness = threading.Thread(target=fetchRss,args=("business","t_business"))


tsports.daemon = True
thealth.daemon = True
tentertainment.daemon = True
ttech.daemon = True
tbusiness.daemon = True

tsports.start()
thealth.start()
tentertainment.start()
ttech.start()
tbusiness.start()

tsports.join()
thealth.join()
tentertainment.join()
ttech.join()
tbusiness.join()