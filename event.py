import datetime
import math
import sqlite3

from nltk.corpus import stopwords
from generals import tokenize


def fetchNewsFromDb(start_date=None, end_date=None):
    connection = sqlite3.connect('./data/news_data.db')
    cursor = connection.cursor()
    if not start_date or not end_date:
        data = cursor.execute('''select * from News''').fetchall()
    else:
        data = cursor.execute('''select * from News where ? <= date and date <= ?  order by date asc,time asc''',
                              (start_date, end_date,)).fetchall()
    return data


def getNgrams(data):
    unigrams = tokenize(data, en_stem=False, en_stopword_removal=True).split()[:25]
    bigrams = zip(unigrams, unigrams[1:])
    trigrams = zip(unigrams, unigrams[1:], unigrams[2:])
    grams = list(bigrams)+list(trigrams)
    return grams


def addEvents(start_date=None, end_date=None):
    data = fetchNewsFromDb(start_date=start_date, end_date=end_date)

    connection = sqlite3.connect('./data/news_data.db')
    cursor = connection.cursor()

    # dates = set([item[4] for item in data])
    window_data = [item[2] for item in data]
    stopw = stopwords.words('english')

    cursor.execute('''delete from final_tfidf''')
    connection.commit()
    window_data = [getNgrams(item) for item in window_data if item]
    window_data = [item for item in window_data if item]
    l = []
    for item in window_data:
        l.extend(item)
    wordSet = list(set(l))
    count = len(window_data)
    if(count<1):
        return
    print("\n", start_date, " --- ", end_date)
    print("No of files:\t",count,"No of wordgrams:\t",len(wordSet),"\n")
    tfidf_list = []

    def getTfidf(word):
        idf = math.log(len(window_data) / (1 + sum([1 for item in window_data if word in item])), 2)
        tf_list = [0.5 + 0.5 * file.count(word) / max([file.count(w) for w in file]) for file in window_data if
                   word in file]
        tf = sum(tf_list)
        '''
        Normalize to 100 file equivalent.
        '''
        tfidf = tf * idf * 100 / len(window_data)
        return tfidf


    for word in wordSet:
        tfidf = getTfidf(word)
        tfidf_list.append({'word':word,'score':tfidf})
    tfidf_list = sorted(tfidf_list,key=lambda x:x['score'],reverse=True)
    for i in tfidf_list[:20]:
        cursor.execute("insert into final_tfidf(word,tfidf) values(?,?)",(" ".join(i['word']),i['score'],))
    connection.commit()

    events = cursor.execute('''
    select new.word,new.tfidf t from final_tfidf as new,tmp_tfidf as old where old.word=new.word and (new.tfidf-old.tfidf)>=(old.tfidf*50/100)
     union
     select word,tfidf t from final_tfidf where word not in (select word from tmp_tfidf) and t>=5
     order by t desc
    ''').fetchall()
    for i in events[:10]:
        print(i[0],i[1])
        cursor.execute("insert or replace into tmp_tfidf(word,tfidf) values(?,?)",(i[0],i[1],))
    connection.commit()


def findTrendingEvents(start_date=None, end_date=None, window_size=2):
    connection = sqlite3.connect('./data/news_data.db')
    cursor = connection.cursor()
    if not start_date or not end_date:
        return None
    cursor.execute("delete from tmp_tfidf")
    cursor.execute("delete from final_tfidf")
    connection.commit()
    current_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    final_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    while current_date <= final_date:
        next_date = (current_date + datetime.timedelta(days=window_size))
        addEvents(current_date.strftime('%Y-%m-%d'), next_date.strftime('%Y-%m-%d'))
        current_date = next_date + datetime.timedelta(days=1)
    connection.commit()


findTrendingEvents('2010-05-01', '2016-05-12', 2)
