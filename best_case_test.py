"""
Delete the train_dump file and run
Exact same dataset is used for training and testing

"""
import codecs
import os
import pickle
import re

import sqlite3
from nltk.corpus import stopwords
from stemming.porter2 import stem

from generals import tokenize
from news_classifier import getClassifier

stopw = ['noun','verb','adjective','adverb','pronoun','preposition','conjunction','interjection','article']+stopwords.words('english')
# Now you have a classifier which can give a try to classifiy text of news whose
# category is unknown, yet.
if (not os.path.isfile('train_dump')):
    print("Train train_data not found !\nPlease try training.")
    classifier = getClassifier()
else:
    with open('train_dump', 'rb') as dump:
        classifier = pickle.load(dump)

resSet = []
cats = ['sports', 'health', 'entertainment', 'tech', 'business']
root = './test_data/'
newsSet = []

connection = sqlite3.connect('data/news_data.db')
cursor = connection.cursor()


for cat in cats:
    dict = {}
    db_out = cursor.execute('''select * from News where category = ? order by title''',(cat,)).fetchall()
    for tuple in db_out:
        print("Testing : ",tuple[2]," --- ",tuple[0])
        data = tokenize(tuple[3],en_stem=True)
        words = re.findall("[a-zA-Z0-9$]+", data)
        # print(words)
        tmp = words.copy()
        for i in words:
            if (i.lower() in stopw) or (len(i) < 2):
                # print(i)
                tmp.remove(i)
                # print(len(tmp)," ",tmp)
        words = [stem(item) for item in tmp]
        string_words = " ".join(words)
        dict = {item: 0 for item in words}
        #print(string_words)
        newsSet.append((dict,cat))
        # Test if category equal to that obtained by the classifier
        res = classifier.classify(dict)
        #print(res)
        if res == cat:
            resSet.append([cat,tuple[2][:15],True])
            #print('---> TRUE')
        else:
            resSet.append([cat,tuple[2],False])
            print("xxxx>>> FALSE ",tuple[2][:15]," : ",cat," - is classified as - ", res)

print(100*len([item for item in resSet if item[2]])/len([item for item in resSet]),' %')

for cat in cats:
    nErr = len([item for item in resSet if(cat==item[0] and not item[2])])
    print('Error in ',cat,' : ',nErr)


if input('want to delete wrong data from db ? [yes i am sure/NO] \n>>> ')=='yes i am sure':
    falseSet = [i for i in resSet if not i[2]]
    connection = sqlite3.connect('data/news_data.db')
    cursor = connection.cursor()
    print(len(falseSet))
    for wrongItem in falseSet:
        print('deleting : ', wrongItem[1])
        try:
            cursor.execute('''delete from News where title = ?''', (wrongItem[1],))
        except Exception as e:
            print("Exception : ", str(e))

    connection.commit()

