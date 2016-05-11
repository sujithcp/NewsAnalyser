import re
import sqlite3
from _operator import itemgetter

from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from stemming.porter2 import stem
import datetime
connection = sqlite3.connect('../data/news_data.db')
cursor = connection.cursor()

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

def fetchNewsFromDb(start_date=None, end_date=None):
    connection = sqlite3.connect('../data/news_data.db')
    cursor = connection.cursor()
    if not start_date or not end_date:
        data = cursor.execute('''select * from News''').fetchall()
    else:
        data = cursor.execute('''select * from News where ? <= date and date <= ?  order by date asc,time asc''', (start_date, end_date,)).fetchall()
    return data

def addEvents(start_date = None,end_date=None):
    data = fetchNewsFromDb(start_date=start_date, end_date=end_date)
    if not data:
        return
    print("\n",start_date," --- ",end_date)
    stopw = stopwords.words('english')

    newsSet = [item[2] for item in data]
    tfidf_vectorizer = TfidfVectorizer(max_df=10, max_features=200000,
                                       min_df=0.002, stop_words=stopw,
                                       use_idf=True, tokenizer=tokenize, ngram_range=(2, 3))
    tfidf_matrix = tfidf_vectorizer.fit_transform(newsSet)
    terms = tfidf_vectorizer.get_feature_names()
    # print(terms)
    idf = tfidf_vectorizer.idf_
    # print(idf)
    dist = 1 - cosine_similarity(tfidf_matrix)
    # print(dist)
    tfidf_list = zip(terms, idf)
    tfidf_list = [{'term': i[0], 'idf': i[1]} for i in tfidf_list]
    tfidf_list = sorted(tfidf_list, key=lambda x: x['idf'])
    cursor.execute("delete from New_Events")
    for i in tfidf_list[:50]:
        #print(i)
        cursor.execute("insert or replace into New_Events(term,score) values(?,?)", (i['term'], i['idf'],))
    events = cursor.execute('''
    select Events.term t,New_events.score s2 from Events,New_Events where Events.term=New_events.term and  (Events.score-s2)>=1
union
select term t,score s2 from New_Events where t not in (select term  from Events) and s2<7
    ''')
    print("\nEvents ------------- \n")
    events = sorted(events,key=itemgetter(1))
    for i in events[:15]:
        print(i[0],i[1])
    cursor.execute("insert or replace into Events select * from New_Events")
    connection.commit()
    return None


def findTrendingEvents(start_date = None,end_date=None,window_size=2):

    if not start_date or not end_date:
        return None
    cursor.execute("delete from Events")
    connection.commit()
    current_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')
    final_date = datetime.datetime.strptime(end_date,'%Y-%m-%d')
    print(current_date.strftime('%Y-%m-%d')," ",final_date.strftime('%Y-%m-%d'),"\n\n\n")
    while current_date<=final_date:
        next_date = (current_date+datetime.timedelta(days=window_size))
        addEvents(current_date.strftime('%Y-%m-%d'),next_date.strftime('%Y-%m-%d'))
        current_date = next_date+datetime.timedelta(days=1)
    connection.commit()


findTrendingEvents(start_date='2010-05-01',end_date='2016-05-11',window_size=5)