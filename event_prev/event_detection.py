import datetime

import sqlite3

from store_tfidf import storeTermScore

connection = sqlite3.connect('./data/news_data.db')
cursor = connection.cursor()

'''Compare with prev term scores and detect events in given window'''

def detectEvent(start_date , end_date):
    cursor.execute('''delete from TempTermScore''')
    connection.commit()
    print('------- ')
    storeTermScore(start_date ,end_date ,"TempTermScore")
    print('------')
    print('------')
    print('------')
    data1=cursor.execute('select temp.term, temp.score from TempTermScore as temp, TermScore as ts where temp.term = ts.term and temp.score >= 6*ts.score').fetchall()
    data2=cursor.execute('select term,score from TempTermScore where term not in (select term from TermScore) and score > 20').fetchall()

    event=data1[:5]
    event.extend( data2[:5])

    print(data1)
    print('----------x----------')

    return [start_date, end_date ,event]


def final(start_date, end_date,window_size):
    window_size-=1

    current_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    final_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    events=[]
    while current_date <= final_date:
        next_date = (current_date + datetime.timedelta(days=window_size))

        events.append(detectEvent(current_date.strftime('%Y-%m-%d'), next_date.strftime('%Y-%m-%d')))

        current_date = current_date  + datetime.timedelta(days=1)

    for window in events:
        print('\n\n<<< Trending Events :', window[0], '-', window [1],'>>>')
        if window [2] ==[]:
            print('  No new trending events in news')
        else:
            for i in window [2]:
                print(' ',i[0],'-',i[1])

final("2016-05-07", "2016-05-17", 3)