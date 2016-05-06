import sqlite3

from NewsPro.tf_idf import tf_idf


def storeTermScore(start_date, end_date , tablename):
    term_Score_list = tf_idf (start_date , end_date )
    term_dict={}
    for eachday in term_Score_list:
        for term in eachday :
            if term[0] in term_dict :
                term_dict [term[0]] += term[1]
            else:
                term_dict[term[0]] = term[1]

    connection = sqlite3.connect('data/news_data.db')
    cursor = connection.cursor()

    for term in term_dict :
        cursor.execute('INSERT INTO ? VALUES(?,?)',tablename , term ,term_dict [term ])

storeTermScore("20018-07-02" , "2016-05-06" , "TermScore")