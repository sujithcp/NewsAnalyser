'''
Train the program with data files

'''
import codecs
import os
import pickle
import re

import nltk
import sqlite3
from stemming.porter2 import stem

from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from nltk.corpus import stopwords

# You need to train the system passing each text one by one to the trainer module.
from generals import tokenize

'''newsSet =[
    {'text': 'not to eat too much is not enough to lose weight', 'category': 'health'},
    {'text': 'Russia is trying to invade Ukraine', 'category': 'politics'},
    {'text': 'do not neglect exercise', 'category': 'health'},
    {'text': 'Syria is the main issue, Obama says', 'category': 'politics'},
    {'text': 'eat to lose weight', 'category': 'health'},
    {'text': 'you should not eat much', 'category': 'health'}
]

for news in newsSet:
    newsTrainer.train(news['text'], news['category'])
'''
connection = sqlite3.connect('data/news_data.db')
cursor = connection.cursor()


def train(cats):
    newsTrainer = Trainer(tokenizer)
    newsSet = []
    stopw = set(stopwords.words('english'))
    # print(stopw)
    for cat in cats:
        data_set = {}
        db_out = cursor.execute('''select * from News where category = ?''',(cat,)).fetchall()
        for item in db_out:
            print(item[2]," ----> ",item[0])
            words = tokenize(item[3],en_stem=True).split()
            data_set = {item: 0 for item in words}
            #print(string_words)
            newsSet.append((data_set, cat))
    classifier = nltk.NaiveBayesClassifier.train(newsSet)
    with open('train_dump', 'wb') as output:
        pickle.dump(classifier, output, pickle.HIGHEST_PROTOCOL)
    #print(classifier.classify({'gain':0,'profit':0,'interest':0}))
    return classifier


# Now you have a classifier which can give a try to classifiy text of news whose
# category is unknown, yet.


#train(['health','sports','tech','entertainment','business'])