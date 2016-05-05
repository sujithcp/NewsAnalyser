import operator
import os
import shutil
from collections import Counter

import sqlite3
from nltk.probability import FreqDist

from generals import *
from news_classifier import getClassifier


def cleanDir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


connection = sqlite3.connect('data/news_data.db')
cursor = connection.cursor()

work_data = cursor.execute('''select * from News''').fetchall()

RESULT_ROOT = 'result_data/'
cleanDir(RESULT_ROOT)

newsClassifier = getClassifier()

for tuple in work_data:
    content = tuple[3]
    print(tuple[2])
    if content.strip() is not '':
        tokenized_content = tokenize(content, en_stem=True)
        # print(tokenized_content)
        data = tokenized_content.split()
        dict = {item: 0 for item in data}
        res = newsClassifier.classify(dict)
        fdist = FreqDist(tokenize(content, en_stem=False).split())
        fdist = sorted(fdist.items(), key=operator.itemgetter(1), reverse=True)
        # print(fdist)
        createFile(RESULT_ROOT + res + '/', fdist[0][0], content)
