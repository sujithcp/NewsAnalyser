import sqlite3


def fetchNewsFromDb(start_date=None, end_date=None):
    connection = sqlite3.connect('data/news_data.db')
    cursor = connection.cursor()
    if not start_date or not end_date:
        data = cursor.execute('''select * from News''').fetchall()
    else:
        data = cursor.execute('''select * from News where ? <= date and date <= ?  order by date asc,time asc''', (start_date, end_date,)).fetchall()
    return data

data = fetchNewsFromDb(start_date='2016-04-01',end_date='2016-05-05')

dates = set([item[4] for item in data])
newsSet = {date:[item for item in data if item[4]==date] for date in dates}
print(len(newsSet['2016-05-05']))