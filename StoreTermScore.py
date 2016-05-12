import sqlite3

from tf_idf import tf_idf


def storeTermScore(start_date, end_date , tablename):
    term_Score_list,max_score,avg_score = tf_idf (start_date , end_date )

    connection = sqlite3.connect('data/news_data.db')
    cursor = connection.cursor()
    #cursor.execute('delete from {tn}'.format(tn=tablename ))
    #print(len(term_dict ))
    if tablename =='TermScore':
        for term in term_Score_list :
            cursor.execute('INSERT OR IGNORE INTO TermScore(term,score) VALUES(?,?)',term  )
        connection.commit()
    else:
        cursor.execute('delete from {tn}'.format(tn=tablename))
        for term in term_Score_list:
            values=[term[0], term[1], max_score [term[0]] - avg_score [term [0]]]
            print( values)
            cursor.execute('INSERT OR IGNORE INTO TempTermScore(term,score,diff) VALUES(?,?,?)',values)
        connection.commit()

#storeTermScore("2016-05-05","2016-05-10",'TempTermScore')