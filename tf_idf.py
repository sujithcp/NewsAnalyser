import operator
import os
import math

import sqlite3

from Tokenize import Tokenize
from fetchData import fetchNewsFromDb


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
    newsSet = {date: [item for item in data if item[4] == date] for date in dates}

    docs_in_a_week=[]
    for date in dates  :
        news_in_a_day={'text':[],'tokens':[]}
        for news in newsSet [date] :
            text = (news[2] + news[3]) .lower()
            tokens=Tokenize(text)
            news_in_a_day['text'] .append(text)
            news_in_a_day['tokens'] .append(tokens)
        docs_in_a_week.append(news_in_a_day)


    for day in docs_in_a_week :
        for tokens in day['tokens']:
            day['score']={}
            for token in set(tokens ):
                n=len(tokens)
                score_of_token=score(token, n,day['text'][day['tokens'].index(tokens)].replace("'", ''), docs_in_a_week )
                if token in day['score']:
                    day['score'][token] += score_of_token
                else:
                    day['score'][token] = score_of_token
    sorted_score = []
    for day in docs_in_a_week :
        sorted_score.append(sorted(day['score'].items(), key=operator.itemgetter(1), reverse=True ))
    return sorted_score

#print ( tf_idf( "2016-05-02" , "2016-05-03") )