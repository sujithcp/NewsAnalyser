import sqlite3

from StoreTermScore import storeTermScore
from event_in_week import event_in_week


def detectEvent(start_date , end_date):
    connection = sqlite3.connect('data/news_data.db')
    cursor = connection.cursor()

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

    print('<<< New Trending Event >>>')
    for term in event:
        print(' '+term)


detectEvent("2016-05-05","2016-05-10")