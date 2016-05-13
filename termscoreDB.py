import sqlite3

from StoreTermScore import storeTermScore

def createTermScoreDB():


    connection = sqlite3.connect('data/news_data.db')
    cursor = connection.cursor()
    cursor.execute('drop table TermScore')
    cursor.execute('drop table TempTermScore')
    cursor.execute('drop table tfidf')
    cursor.execute('drop table final_tfidf')
    cursor .execute('''create table TermScore ('term' TEXT, 'score' REAL)''')
    cursor.execute('''create table TempTermScore ('term' TEXT, 'score' REAL )''')
    cursor.execute('''create table tfidf ('date' TEXT,'word' TEXT, 'tfidf' REAL)''')
    cursor.execute('''create table final_tfidf ('date' TEXT,'word' TEXT, 'tfidf' REAL)''')
    connection.commit()


    storeTermScore("2008-01-01","2016-05-05" , "TermScore")

createTermScoreDB()