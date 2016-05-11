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
    print(dates)
    newsSet = {date: [item for item in data if item[4] == date] for date in dates}

    docs_in_a_week=[]
    for date in dates  :
        news_in_a_day={'text':[],'tokens':[]}
        for news in newsSet [date] :
            text = (news[2]) .lower()
            tokens=Tokenize(text)
            #print (tokens)
            news_in_a_day['text'] .append(text)
            news_in_a_day['tokens'] .append(tokens)
        docs_in_a_week.append(news_in_a_day)

    token_score={}

    for day in docs_in_a_week :
        #day['score'] = {}
        for tokens in day['tokens']:

            n = len(tokens)
            for token in set(tokens ):
                score_of_token=score(token, n,day['text'][day['tokens'].index(tokens)].replace("'", ''), docs_in_a_week )
                '''
                if score_of_token > 0 :
                    if token in token_score :
                        token_score [token] += score_of_token
                        if score_of_token >max_score [token ]:
                            max_score [token ]= score_of_token
                        if score_of_token <min_score [token ] :
                            min_score [token ] =score_of_token
                    else:
                        token_score [token] = score_of_token
                        max_score [token ] = score_of_token
                        min_score [token ] = score_of_token

                    print("Token : ",token," \t, Score : ",score_of_token )
                '''

                if score_of_token > 0:
                    if token in token_score:
                        token_score[token] .append (score_of_token)

                    else:
                        token_score[token] = [score_of_token ]
                print("Token : ", token, " \t, Score : ", score_of_token)

    max_score = {}
    avg_score = {}

    for token in token_score :
        max_score [token ] =max( token_score [token ])
        n=sum(1 for i in token_score[token ] )
        token_score [token ] = sum(i for i in token_score [token ])
        avg_score [token ] = token_score [token ] /n

    sorted_score=sorted(token_score.items(), key=operator.itemgetter(1), reverse=True )

    return sorted_score , max_score , avg_score

#tf_idf( "2016-05-05" , "2016-05-06" )