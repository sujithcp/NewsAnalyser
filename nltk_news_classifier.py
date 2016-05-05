import codecs
import os
from nltk.corpus import stopwords
import re
import nltk
from stemming.porter2 import stem

cats = ['sports', 'health', 'entertainment', 'tech', 'business']
root = './test_data/'
newsSet = []
stopw = set(stopwords.words('english'))
# print(stopw)
for cat in cats:
    dict = {}
    for f in os.listdir(root + cat + '/'):
        if os.path.isfile(root + cat + '/' + f):
            print(cat+'/'+f)
            with codecs.open(root + cat + '/' + f, "r", encoding='utf-8', errors='ignore') as rfile:
                rdata = rfile.read().lower()
            words = re.findall("[a-zA-Z0-9$]+", rdata)
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
            with open(root+cat+'/'+f, 'w') as wfile:
                wfile.write(string_words)
            #print(string_words)
            newsSet.append((dict,cat))

cls = nltk.NaiveBayesClassifier.train(newsSet)
print(cls.most_informative_features(10))
text = 'Saina Nehwal and PV Sindhu both defeated their respective Indonesian opponents to start the Asian Badminton Championship on a winning note on Wednesday'
text = [stem(item) for item in text.split()]
dict = {item: 0 for item in text}
print(cls.classify(dict))