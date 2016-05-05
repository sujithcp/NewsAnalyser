"""
Suppose you have some texts of news and know their categories.
You want to train a system with this pre-categorized/pre-classified
texts. So, you have better call this data your training set.
"""
import os
import pickle

import sys
from nltk.corpus import stopwords
from stemming.porter2 import stem

from train import train
import nltk
import re

def getClassifier():
    stopw = ['noun', 'verb', 'adjective', 'adverb', 'pronoun', 'preposition', 'conjunction', 'interjection',
             'article'] + stopwords.words('english')
    # Now you have a classifier which can give a try to classifiy text of news whose
    # category is unknown, yet.
    cats = ['sports', 'health', 'entertainment', 'tech', 'business']
    root = './train_data/'
    if not os.path.isfile('train_dump'):
        classifier = train(cats)
    else:
        with open('train_dump', 'rb') as dump:
            classifier = pickle.load(dump)
    return classifier
'''

stopw = ['noun','verb','adjective','adverb','pronoun','preposition','conjunction','interjection','article']+stopwords.words('english')
# Now you have a classifier which can give a try to classifiy text of news whose
# category is unknown, yet.
cats = ['sports', 'health', 'entertainment', 'tech', 'business']
root = './train_data/'

choice = input("Want to teach [Y/n]\n")
if(choice.lower() == 'y') or (not os.path.isfile('train_dump')):
    classifier = train(root,cats)
else:
    with open('train_dump', 'rb') as dump:
        classifier = pickle.load(dump)

print("Data >>>")
data = sys.stdin.read().lower()
data = re.findall('[a-zA-Z0-9$][a-zA-Z0-9$]+', data)
tmp = data.copy()
for i in data:
    if (i.lower() in stopw) or (len(i) < 2):
        # print(i)
        tmp.remove(i)
        # print(len(tmp)," ",tmp)
data = [stem(item) for item in tmp]
dict = {item: 0 for item in data}
classification = classifier.classify(dict)
# the classification variable holds the possible categories sorted by
# their probablity value
print(classification)

'''