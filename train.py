'''
Train the program with data files

'''
import pickle
import sqlite3
import nltk
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
    newsSet = []
    for cat in cats:
        db_out = cursor.execute('''select * from News where category = ?''',(cat,)).fetchall()
        for item in db_out:
            print(item[2]," ----> ",item[0])
            words = tokenize(item[3],en_stem=True).split()
            data_set = {item: 0 for item in words}
            newsSet.append((data_set, cat))
    classifier = nltk.NaiveBayesClassifier.train(newsSet)
    with open('train_dump', 'wb') as output:
        pickle.dump(classifier, output, pickle.HIGHEST_PROTOCOL)
    #print(classifier.classify({'gain':0,'profit':0,'interest':0}))
    return classifier


#train(['health','sports','tech','entertainment','business'])