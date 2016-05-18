import codecs
import logging
import os
import pickle
import re
import sqlite3

import nltk
from nltk.corpus import stopwords
from stemming.porter2 import stem



def createFile(dir, filename, content,replace = True):
    path = re.sub('[/]+', '/', dir + '/' + filename)
    if not os.path.exists(dir):
        os.makedirs(dir)
    if os.path.isfile(path):
        if not replace:
            print(path," !!!! already exists >>>>> skipping !!!!")
            return True
    try:
        with open(path, 'w') as wfile:
            wfile.write(content)
        return True
    except:
        print("Could not write to file")
        return False


def readFile(path):
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        with codecs.open(path, "r", encoding='utf-8', errors='ignore') as rfile:
            return rfile.read()
    except Exception as e:
        print("Could not read file ",path)
        logging.exception(str(e))
        return None


def tokenize(data,en_stem=True,en_stopword_removal=True):
    word_forms = ['noun', 'verb', 'adjective', 'adverb', 'pronoun', 'preposition', 'conjunction', 'interjection','article']
    stopw =list(set(word_forms+[stem(item) for item in word_forms ])) + stopwords.words('english')

    words = re.findall("[a-zA-Z0-9$][a-zA-Z0-9$]+", data)
    # print(words)
    words = [item.lower() for item in words]
    tmp = words.copy()
    if en_stopword_removal:
        for i in words:
            if (i.lower() in stopw) or (len(i) < 2):
                # print(i)
                tmp.remove(i)
                # print(len(tmp)," ",tmp)
    if en_stem:
        words = [stem(item) for item in tmp]
    else:
        words = tmp.copy()
    return " ".join(words)

def dump(dir,name,obj):
    with open(dir+'/'+name,'w') as wfile:
        pickle.dump(obj,wfile,pickle.HIGHEST_PROTOCOL)
def getDump(dir,name):
    with open(dir + '/' + name, 'r') as rfile:
        return pickle.load(rfile)


def getFileList(dir):
    list = []
    for f in os.listdir(dir):
        if os.path.isfile(dir + f):
            list.append(dir+f)

    return list

def train(cats):
    connection = sqlite3.connect('data/news_data.db')
    cursor = connection.cursor()
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

def fetchNewsFromDb(start_date=None, end_date=None):
    connection = sqlite3.connect('data/news_data.db')
    cursor = connection.cursor()
    if not start_date or not end_date:
        query = '''select * from News'''
    else:
        query = '''select * from News where ? <= date and date <= ? ''', (start_date, end_date,)
    data = cursor.execute(query).fetchall()
    return data

def getClassifier(force_train=False):
    stopw = ['noun', 'verb', 'adjective', 'adverb', 'pronoun', 'preposition', 'conjunction', 'interjection',
             'article'] + stopwords.words('english')
    # Now you have a classifier which can give a try to classifiy text of news whose
    # category is unknown, yet.
    cats = ['sports', 'health', 'entertainment', 'tech', 'business']
    root = './train_data/'
    if not os.path.isfile('train_dump') or force_train:
        classifier = train(cats)
    else:
        with open('train_dump', 'rb') as dump:
            classifier = pickle.load(dump)
    return classifier