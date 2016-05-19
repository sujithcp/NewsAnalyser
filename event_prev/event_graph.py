import datetime
import math
import sqlite3

from matplotlib import pyplot as plt
from matplotlib.dates import date2num

from generals import tokenize


graph1={'mother day':[],'rio olympics':[], 'cannes review' : [],'akshaya tritiya' : []}

x=[]


def fetchNewsFromDb(start_date=None, end_date=None):
    connection = sqlite3.connect('../data/news_data.db')
    cursor = connection.cursor()
    if not start_date or not end_date:
        data = []
    else:
        data = cursor.execute('''select * from News where ? <= date and date <= ?
        union
        select * from General_News where ? <= date and date <= ?
        order by date asc,time asc

        ''',
                              (start_date, end_date,start_date, end_date,)).fetchall()
    return data


def getNgrams(data):
    unigrams = tokenize(data, en_stem=False, en_stopword_removal=True).split()[:25]
    bigrams = zip(unigrams, unigrams[1:])
    trigrams = zip(unigrams, unigrams[1:], unigrams[2:])
    grams = list(bigrams)+list(trigrams)
    return grams


def addEvents(start_date=None, end_date=None):
    NULL = '____-__-__'
    data = fetchNewsFromDb(start_date=start_date, end_date=end_date)

    connection = sqlite3.connect('../data/news_data.db')
    cursor = connection.cursor()

    # dates = set([item[4] for item in data])
    window_data = [item[2] for item in data]
    cursor.execute('''delete from final_tfidf''')
    connection.commit()
    window_data = [getNgrams(item) for item in window_data if item]
    window_data = [item for item in window_data if item]
    l = []
    for item in window_data:
        l.extend(item)
    wordSet = list(set(l))
    count = len(window_data)
    if(count>0):
        print("\n", start_date, " --- ", end_date)
        print("No. of files: ",count,"\t","No of wordgrams: ",len(wordSet),"\n")
    tfidf_list = []

    def getTfidf(word):
        idf = math.log(len(window_data) / (1 + sum([1 for item in window_data if word in item])), 10)
        tf_list = [0.6 + 0.4 * file.count(word) / max([file.count(w) for w in file]) for file in window_data if
                   word in file]
        tf = sum(tf_list)
        tfidf = tf * idf
        return tfidf


    for word in wordSet:
        tfidf = getTfidf(word)
        tfidf_list.append({'word':word,'score':tfidf})
    norm = (sum([item['score']**2 for item in tfidf_list]))**0.5
    tfidf_list = [{'word':item['word'],'score':item['score']*100/norm} for item in tfidf_list]
    tfidf_list = sorted(tfidf_list,key=lambda x:x['score'],reverse=True)

    tfidf_copy = {" ".join( i['word']) : i['score'] for i in tfidf_list }

    for i in graph1:
        if i in tfidf_copy :
            graph1 [i].append(tfidf_copy [i])
        else:
            graph1[i].append(0)

    for i in tfidf_list:
        cursor.execute("insert into final_tfidf(date,word,tfidf) values(?,?,?)",(NULL," ".join(i['word']),i['score'],))

    events = cursor.execute('''
    select new.word,new.tfidf t from final_tfidf as new,tmp_tfidf as old where old.word=new.word and (new.tfidf-old.tfidf)>=(old.tfidf*50/100)
     union
     select word,tfidf t from final_tfidf where word not in (select word from tmp_tfidf) and final_tfidf.tfidf>(select max(tfidf) from final_tfidf)*25/100
     order by t desc
    ''').fetchall()
    for num,i in enumerate(events):
        if num <= 10:
            print(i[0]," : ",i[1])
        cursor.execute("insert or replace into tmp_tfidf(date,word,tfidf) values(?,?,?)",(NULL,i[0],i[1],))
    connection.commit()


def findTrendingEvents(start_date=None, end_date=None, window_size=2):
    window_size-=1
    connection = sqlite3.connect('../data/news_data.db')
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
        x.append(current_date )
        addEvents(current_date.strftime('%Y-%m-%d'), next_date.strftime('%Y-%m-%d'))
        current_date = current_date + datetime.timedelta(days=1)
    connection.commit()


findTrendingEvents('2016-05-01', '2016-05-19',1)



def plotgraph():
    x1 = [date2num(date) for date in x]


    #j=0
    #colour=['b-o', 'r-o', 'g-o', 'c-o', 'm-o']
    for ind in graph1 :
        plt.clf()
        fig = plt.figure()

        graph = fig.add_subplot(111)
        max_value = max( graph1 [ind])
        graph.plot(x1, graph1 [ind], 'b-o',linewidth=1.5,dash_joinstyle='round')

        # Set the xtick locations to correspond to just the dates you entered.
        graph.set_xticks(x)

        datacopy = []
        n = len(x)
        for i in range(n):
            if i % 14 == 0:
                datacopy.append(x[i].strftime("%Y-%m-%d"))
            elif i == n - 1:
                datacopy.append(x[i].strftime("%Y-%m-%d"))
            else:
                datacopy.append(" ")
                # Set the xtick labels to correspond to just the dates you entered.

        # graph.set_xticklabels( [date.strftime("%Y-%m-%d") for (date, value) in data])

        graph.set_xticklabels([date.strftime("%d") for date in x])

        plt.xlabel('Date (Year, Month : 2016, May)')
        plt.ylabel('TF-IDF Weight')
        plt.title('Event - '+ind)
        plt.grid(True)
        limit= max_value + max_value * .3
        plt.ylim((0, limit ))
        plt.savefig(ind+'.png')
        #j+=1

plotgraph()