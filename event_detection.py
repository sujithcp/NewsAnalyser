import sqlite3

from StoreTermScore import storeTermScore


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
    data1=cursor.execute('select temp.term from TempTermScore as temp, TermScore as ts where temp.term = ts.term and temp.score >= 6*ts.score ').fetchall()
    data2=cursor.execute('select term from TempTermScore where term not in (select term from TermScore) and score > 20').fetchall()
    #data = cursor.execute('''select temp.term from TempTermScore as temp,TermScore as ts where (temp.term=ts.term and temp.score>=(2*ts.score)) or temp.term not in (select distinct term from TermScore)''').fetchall()
    terms=[]
    for term in data1[:5]:
        terms.extend(term)
        #print(term[0])
    for term in data2[:5]:
        terms.extend(term)
        #print(term[0])

    print('<<< New Trending Event >>>')
    for term in terms:
        print(' '+term)


detectEvent("2016-05-05","2016-05-11")