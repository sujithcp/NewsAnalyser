import sqlite3

import math

from Tokenize import Tokenize
from fetchData import fetchNewsFromDb


def event_in_week(start_date, end_date) :
    data = fetchNewsFromDb(start_date, end_date)

    connection = sqlite3.connect('./data/news_data.db')
    cursor = connection.cursor()

    dates = set([item[4] for item in data])
    newsSet = {date: [item for item in data if item[4] == date] for date in dates}

    cursor.execute('delete from tfidf')
    connection.commit()
    count = len(data)
    print(count)

    for date in dates:

        connection = sqlite3.connect('./data/news_data.db')
        cursor = connection.cursor()
        global count
        dateData = newsSet[date]
        dateFiles = []
        for item in dateData:
            dateFiles .append(Tokenize(item [2].lower()))

        for file in dateData:
            count -= 1
            print(count, "more/ Analysing  : ", file[2])

            fileWords = Tokenize(file [2].lower())
            fileWordsSet = list(set(fileWords))
            tfidf_list = []
            # print(fileWordsSet)
            for word in fileWordsSet:
                tfidf = (0.5 + 0.5 * fileWords.count(word) / max([fileWords.count(i) for i in fileWords])) * (
                math.log((len(dateData) / (1 + sum([1 for f in dateFiles if word in f])))) / math.log(
                    (len(dateData) / 1))) * 100
                # print(remSet)
                tfidf_list.append({'word': word, 'tfidf': tfidf})
                # print(len(tfidf_list))

            max_tfidf = max(tfidf_list or [{'tfidf': 0}], key=lambda x: x['tfidf'])['tfidf']
            # print(max_tfidf)
            print("max tfidf , ",max_tfidf)
            tfdif_list = [item for item in tfidf_list if item['tfidf'] >= (max_tfidf / 4)]
            for i in tfdif_list:
                cursor.execute("insert or ignore into tfidf(date,word,tfidf) values(?,?,?)",
                               (date, i['word'], i['tfidf'],))

        connection.commit()

    ngrams = cursor.execute('select distinct word from tfidf order by word').fetchall()

    cursor.execute('delete from final_tfidf')
    connection.commit()
    for tuple in ngrams:
        tfidf_sums = cursor.execute(
            'select date, word, sum(tfidf) s from tfidf where word = ? group by date order by s desc', (tuple[0],))

        tfidf_sum = [item[2] for item in tfidf_sums]
        diff = max(tfidf_sum) - min(tfidf_sum)
        if diff <= 0:
            continue
        print(tuple[0], " - ", diff)
        cursor.execute('insert into final_tfidf(word, tfidf) values(?,?)', (tuple[0], diff,))
    connection.commit()




#event_in_week("2016-05-08", "2016-05-10")