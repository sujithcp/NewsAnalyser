import logging
import os
import shutil
import feedparser
import re
import time
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from stemming.porter2 import stem

from data_fetcher.fetcher import GetTextFromUrl
from generals import readFile, createFile
from news_classifier import getClassifier

classifier = getClassifier()
def cleanDir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def getUrlList(url):
    try:
        lines = [line.strip() for line in readFile(url).strip().split('\n')]
        #print(lines)
    except Exception as e:
        logging.exception(str(e))
        return []
    return lines

def tokenize(data,en_stem=False,en_stopword_removal=True):
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
    return words


def fetchNews():
    news_set = []
    cleanDir('./OUTPUT/')
    URL_LIST = (getUrlList('url_list'))
    if not URL_LIST:
        print("No URLs found ")
        return False
    for url in URL_LIST:
        try:
            fp = feedparser.parse(url)
            print("URL: ", url)
            print("No. of articles : ", len(fp['entries']))
            for i in range(0, len(fp['entries']) - 1):
                title = fp['entries'][i]['title']
                link = fp['entries'][i]['link']
                text = title + "\n" + GetTextFromUrl(link).getText()[:200]
                news_set.append(text)

        except Exception as e:
            logging.exception(str(e))

    return  news_set

news_set = fetchNews()
for i in news_set:
    print("*****\t",i)
tfidf_vectorizer = TfidfVectorizer(max_df=10, max_features=200000,
                                   min_df=0.002,
                                   use_idf=True, tokenizer=tokenize, ngram_range=(2, 3))
tfidf_matrix = tfidf_vectorizer.fit_transform(news_set)
terms = tfidf_vectorizer.get_feature_names()
num_clusters = 10
km = KMeans(n_clusters=num_clusters,n_jobs=4)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()

for num,item in enumerate(clusters):
    createFile('OUTPUT/'+str(item),news_set[num][:10],news_set[num])
print(clusters)
