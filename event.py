import sqlite3

import math
from _operator import itemgetter

from generals import tokenize


def fetchNewsFromDb(start_date=None, end_date=None):
    connection = sqlite3.connect('./data/news_data.db')
    cursor = connection.cursor()
    if not start_date or not end_date:
        data = cursor.execute('''select * from News''').fetchall()
    else:
        data = cursor.execute('''select * from News where ? <= date and date <= ?  order by date asc,time asc''', (start_date, end_date,)).fetchall()
    return data

data = fetchNewsFromDb(start_date='2016-04-01',end_date='2016-05-05')

dates = set([item[4] for item in data])
newsSet = {date:[item for item in data if item[4]==date] for date in dates}
for date in dates:
    dateData = newsSet[date]
    dayWords = [item[3] for item in dateData]
    tmpWords = ""
    for item in dayWords:
        tmpWords = tmpWords+" "+tokenize(item,en_stem=False)
    dayWords = tmpWords.split()
    dateFiles  =  [tokenize(item[3]).split() for item in dateData]
    for file in dateData:
        fileWords = tokenize(file[3],en_stem=False).split()
        tfidf_list= []
        fileWordsSet = list(set(fileWords))
        for word in fileWordsSet:
            tfidf = (fileWords.count(word)/len(fileWords))*math.log(len(dateData)/(1+sum([1 for f in dateFiles if word in f])))
            tfidf_list.append({'word':word,'tfidf':tfidf})
            print(word," -- ",tfidf)
        print(sorted(tfidf_list,key = itemgetter('tfidf')))
    print(dayWords)
    exit()