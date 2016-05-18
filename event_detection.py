import datetime

import sqlite3

import math

from general_functions import fetchNewsFromDb, Tokenize
from store_tfidf import storeTermScore

connection = sqlite3.connect('./data/news_data.db')
cursor = connection.cursor()

def detectEvent(start_date , end_date):
    cursor.execute('''delete from TempTermScore''')
    connection.commit()
    print('------- ')
    storeTermScore(start_date ,end_date ,"TempTermScore")
    print('------')
    print('------')
    print('------')
    data1=cursor.execute('select temp.term from TempTermScore as temp, TermScore as ts where temp.term = ts.term and temp.score >= 4*ts.score').fetchall()
    data2=cursor.execute('select term from TempTermScore where term not in (select term from TermScore) and score > 20').fetchall()
    #data = cursor.execute('''select temp.term from TempTermScore as temp,TermScore as ts where (temp.term=ts.term and temp.score>=(2*ts.score)) or temp.term not in (select distinct term from TermScore)''').fetchall()

    data1=data1[:10]
    data1.extend( data2[:10])
    data1 = [i[0] for i in data1]

    event_in_week(start_date , end_date )

    data2 = cursor.execute('select word from final_tfidf order by tfidf desc limit 20').fetchall()
    data2 = [i[0] for i in data2]
    print(data1)
    print('----------x----------')
    print(data2)
    print('----------x----------')
    event = [term for term in data1 if term in data2 ]

    return [start_date, end_date ,event]


def event_in_week(start_date, end_date) :
    data = fetchNewsFromDb(start_date, end_date)

    dates = set([item[4] for item in data])
    newsSet = {date: [item for item in data if item[4] == date] for date in dates}

    cursor.execute('delete from tfidf')
    connection.commit()
    count = len(data)
    print(count)

    for date in dates:

        global count
        dateData = newsSet[date]
        dateFiles = []
        for item in dateData:
            dateFiles .append(Tokenize(item [2].lower()))

        for file in dateData:
            count -= 1
            print(count, "more/ Analysing  : ", file[2])

            fileWords = Tokenize(file [2].lower())
            fileWordsSet = list(set(fileWords))
            tfidf_list = []
            # print(fileWordsSet)
            for word in fileWordsSet:
                tfidf = (0.5 + 0.5 * fileWords.count(word) / max([fileWords.count(i) for i in fileWords])) * (
                math.log((len(dateData) / (1 + sum([1 for f in dateFiles if word in f])))) /1+ math.log(
                    (len(dateData) / 1))) * 100
                # print(remSet)
                tfidf_list.append({'word': word, 'tfidf': tfidf})
                # print(len(tfidf_list))

            max_tfidf = max(tfidf_list or [{'tfidf': 0}], key=lambda x: x['tfidf'])['tfidf']
            # print(max_tfidf)
            print("max tfidf , ",max_tfidf)
            tfdif_list = [item for item in tfidf_list if item['tfidf'] >= (max_tfidf / 4)]
            for i in tfdif_list:
                cursor.execute("insert or ignore into tfidf(date,word,tfidf) values(?,?,?)",
                               (date, i['word'], i['tfidf'],))

        connection.commit()

    ngrams = cursor.execute('select distinct word from tfidf order by word').fetchall()

    cursor.execute('delete from final_tfidf')
    connection.commit()
    for tuple in ngrams:
        tfidf_sums = cursor.execute(
            'select date, word, sum(tfidf) s from tfidf where word = ? group by date order by s desc', (tuple[0],))

        tfidf_sum = [item[2] for item in tfidf_sums]
        diff = max(tfidf_sum) - min(tfidf_sum)
        if diff <= 0:
            continue
        print(tuple[0], " - ", diff)
        cursor.execute('insert into final_tfidf(word, tfidf) values(?,?)', (tuple[0], diff,))
    connection.commit()


def final(start_date, end_date,window_size):
    window_size-=1

    current_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    final_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    events=[]
    while current_date <= final_date:
        next_date = (current_date + datetime.timedelta(days=window_size))

        events.append(detectEvent(current_date.strftime('%Y-%m-%d'), next_date.strftime('%Y-%m-%d')))

        current_date = next_date + datetime.timedelta(days=1)

    for window in events:
        print('\n\n<<< Trending Events :', window[0], '-', window [1],'>>>')
        if window [2] ==[]:
            print('  No new trending events in news')
        else:
            for i in window [2]:
                print(' ',i)

final("2016-05-08", "2016-05-17", 3)