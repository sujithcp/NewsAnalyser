import sqlite3

import math
from operator import itemgetter

import nltk

from generals import tokenize

n_samples = 2000
n_features = 1000
n_topics = 10
n_top_words = 20


def tf(word, text, n):
    return text.count(word) / n


def n_containing(term, docs):
    return sum(1 for doc in docs if term in doc['tokens'])


def idf(term, docs):
    n = 0
    for day in docs:
        for news in day['tokens']:
            n += 1
    return math.log(n / (1 + n_containing(term, docs)))


def score(term, n, text, docs):
    return tf(term, text, n) * idf(term, docs)


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()


def fetchNewsFromDb(start_date=None, end_date=None):
    connection = sqlite3.connect('../data/news_data.db')
    cursor = connection.cursor()
    if not start_date or not end_date:
        data = cursor.execute('''select * from News''').fetchall()
    else:
        data = cursor.execute('''select * from News where ? <= date and date <= ?  order by date asc,time asc''',
                              (start_date, end_date,)).fetchall()
    return data


news_data = fetchNewsFromDb(start_date='2016-05-02', end_date='2016-05-06')
dates = set([item[4] for item in news_data])
newsSet = {date: [item for item in news_data if item[4] == date] for date in dates}

freqs = []





