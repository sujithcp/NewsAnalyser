import sqlite3

from StoreTermScore import storeTermScore


def detectEvent(start_date , end_date):
    connection = sqlite3.connect('data/news_data.db')
    cursor = connection.cursor()

    cursor.execute('''delete from TempTermScore''')
    connection.commit()
    print('------- 1')
    storeTermScore(start_date ,end_date ,"TempTermScore")
    print('------')

    print('------')
    data = cursor.execute('''select temp.term from TempTermScore as temp,TermScore as ts where (temp.term=ts.term and temp.score>=(2*ts.score)) or temp.term not in (select distinct term from TermScore)''').fetchall()

    for term in data:
        print(term)

detectEvent("2016-05-01","2016-05-06")