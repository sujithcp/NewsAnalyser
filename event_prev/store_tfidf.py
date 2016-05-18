import math
import operator

import sqlite3

from general_functions import fetchNewsFromDb, Tokenize

connection = sqlite3.connect('data/news_data.db')
cursor = connection.cursor()

def tf(word, text,n):
    return text.count(word)/n


def n_containing(term, docs):
    return sum(1 for doc in docs if term in doc['tokens'] )


def idf(term , docs):
    n=0
    for day in docs:
        for news in day['tokens']:
            n+=1
    return math.log ( n / ( 1 + n_containing(term, docs) ) )


def score(term, n,text, docs):
    return tf(term, text,n) * idf(term,docs)


def tf_idf ( start_date, end_date ):
    data=fetchNewsFromDb(start_date ,end_date )
    dates = set([item[4] for item in data])
    print(dates)
    newsSet = {date: [item for item in data if item[4] == date] for date in dates}

    docs_in_a_week=[]
    for date in dates  :
        news_in_a_day={'text':[],'tokens':[]}
        for news in newsSet [date] :
            text = (news[2]) .lower()
            tokens=Tokenize(text)
            news_in_a_day['text'] .append(text)
            news_in_a_day['tokens'] .append(tokens)
        docs_in_a_week.append(news_in_a_day)

    token_score = {}


    for day in docs_in_a_week :
        for tokens in day['tokens']:

            n = len(tokens)
            for token in set(tokens ):
                score_of_token=score(token, n,day['text'][day['tokens'].index(tokens)].replace("'", ''), docs_in_a_week )

                if score_of_token > 0 :
                    if token in token_score :
                        token_score [token] += score_of_token
                    else:
                        token_score [token] = score_of_token
                    print("Token : ",token," \t, Score : ",score_of_token )

    sorted_score=sorted(token_score.items(), key=operator.itemgetter(1), reverse=True )

    return sorted_score


def storeTermScore(start_date, end_date , tablename):
    term_Score_list = tf_idf (start_date , end_date )

    if tablename =='TermScore':
        for term in term_Score_list :
            cursor.execute('INSERT OR IGNORE INTO TermScore(term,score) VALUES(?,?)',term  )
        connection.commit()
    else:
        cursor.execute('delete from {tn}'.format(tn=tablename))
        for term in term_Score_list:
            cursor.execute('INSERT OR IGNORE INTO TempTermScore(term,score) VALUES(?,?)',term)
        connection.commit()


def createTermScoreDB():
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


#createTermScoreDB()