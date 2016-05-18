
from matplotlib import pyplot as plt
from matplotlib.dates import  date2num
import sqlite3
import datetime

def plotDB():
    connection=sqlite3.connect('../data/news_data.db')
    cursor = connection .cursor()

    data= cursor.execute('''select date, count(title) as count from News where date>='2016-04-01' group by date''')

    data=[i for i in data if i[0] != 'NULL']

    date=[]
    for i in data:
        date.append(datetime.datetime.strptime(i[0], '%Y-%m-%d'))

    date= [date2num(i)  for i in date ]
    count=[i[1] for i in data]

    plt.plot(date, count, 'b')
    plt.axis()
    plt.show()

plotDB()

