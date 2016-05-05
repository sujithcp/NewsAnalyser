from datetime import datetime

import re

import sqlite3

date_object = datetime.strptime('Thu, 05 May 2016 17:14:47 +0530', '%a, %d %b %Y %X %z')
print(date_object.date(), date_object.time())

datetime_var = re.sub('[ ][0-9A-Z+-]+$', '', 'Thu, 05 May 2016 17:14:47 +0530', 1)
print(datetime_var)

con = sqlite3.connect('../data/news_data.db')
cur = con.cursor()

data = cur.execute('''select * from News where date not like "%-%-%" ''').fetchall()

for t in data:
    old_date = t[4]
    print(old_date)
    new_date = datetime.strptime(old_date,'%d %b %Y').date()
    print(new_date)
    cur.execute('''update News set date = ? where title = ? and id = ?''',(new_date,t[2],t[1],))
con.commit()
