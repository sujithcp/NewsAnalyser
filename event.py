import sqlite3

import math
from _operator import itemgetter

import nltk

from generals import tokenize


def fetchNewsFromDb(start_date=None, end_date=None):
    connection = sqlite3.connect('./data/news_data.db')
    cursor = connection.cursor()
    if not start_date or not end_date:
        data = cursor.execute('''select * from News''').fetchall()
    else:
        data = cursor.execute('''select * from News where ? <= date and date <= ?  order by date asc,time asc''', (start_date, end_date,)).fetchall()
    return data

data = fetchNewsFromDb(start_date='2016-05-04',end_date='2016-05-09')

connection = sqlite3.connect('./data/news_data.db')
cursor = connection.cursor()


dates = set([item[4] for item in data])
newsSet = {date:[item for item in data if item[4]==date] for date in dates}

'''
for date in dates:
    dateData = newsSet[date]
    dayWords = [item[2] for item in dateData]
    tmpWords = ""
    for item in dayWords:
        tmpWords = tmpWords+" "+tokenize(item,en_stem=False)
    dayWords = tmpWords.split()
    dateFiles  =  [list(nltk.bigrams(tokenize(item[2],en_stem=False).split()))+list(nltk.trigrams(tokenize(item[2],en_stem=False).split())) for item in dateData]
    for file in dateData:
        fileWords = list(nltk.bigrams(tokenize(file[2],en_stem=False).split()))+list(nltk.trigrams(tokenize(file[2],en_stem=False).split()))
        tfidf_list= []
        fileWordsSet = list(set(fileWords))
        for word in fileWordsSet:
            tfidf = (0.5+0.5*fileWords.count(word)/max([fileWords.count(i) for i in fileWords]))*math.log(len(dateData)/(1+sum([1 for f in dateFiles if word in f])),2)
            tfidf_list.append({'word':word,'tfidf':tfidf})
            #print(word," -- ",tfidf)
        tdif_list = sorted(tfidf_list,key = itemgetter('tfidf'),reverse=True)
        tdif_list = [item for item in tdif_list if item['tfidf']>=(tdif_list[0]['tfidf']/2)]
        for i in tdif_list:
            cursor.execute("insert or ignore into tfidf(date,word,tfidf) values(?,?,?)",(date," ".join(i['word']),i['tfidf'],))
        print(tdif_list)
        connection.commit()


'''
ngrams = cursor.execute('''select distinct word from tfidf order by word''').fetchall()

for tuple in ngrams:
    tfidf_sums = cursor.execute('''select date, word, sum(tfidf) s from tfidf where word = ? group by date order by s desc''', (tuple[0],))
    tfidf_sums = [item[2] for item in tfidf_sums]
    diff = max(tfidf_sums)-min(tfidf_sums)
    print(tuple[0]," - ",diff)
    if diff<=0:
        continue
    cursor.execute('''insert into final_tfidf(word, tfidf) values(?,?)''',(tuple[0],diff,))
connection.commit()
