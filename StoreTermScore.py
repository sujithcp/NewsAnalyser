import sqlite3

from tf_idf import tf_idf


def storeTermScore(start_date, end_date , tablename):
    term_Score_list = tf_idf (start_date , end_date )

    connection = sqlite3.connect('data/news_data.db')
    cursor = connection.cursor()
    cursor.execute('''delete from {tn}'''.format(tn=tablename ))
    #print(len(term_dict ))
    for term in term_Score_list  :
        cursor.execute('INSERT OR IGNORE INTO {tn}(term,score) VALUES(?,?)'.format(tn=tablename),term  )
    connection.commit()
