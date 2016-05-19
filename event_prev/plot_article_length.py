
from matplotlib import pyplot as plt
from matplotlib.dates import  date2num
import sqlite3
import datetime as DT

def plotLength():
    connection=sqlite3.connect('../data/news_data.db')
    cursor = connection .cursor()

    data= cursor.execute(''' select date,max(length(news)) as maxlen, min(length(news)) as minlen from News where date>="2016-04-01" group by date''').fetchall()

    data = [i for i in data if i[0] != 'NULL']

    data = [(DT.datetime.strptime(i[0], "%Y-%m-%d"), i[1], i[2]) for i in data]

    x = [date2num(date) for (date, value1, value2) in data]
    y1 = [value1 for (date, value1, value2) in data]
    y2 = [value2 for (date, value1, value2) in data]

    fig = plt.figure()

    graph = fig.add_subplot(111)

    # Plot the data as a red line with round markers
    graph.plot(x, y1,'r-o',x,y2, 'b-o',linewidth=1.5)

    # Set the xtick locations to correspond to just the dates you entered.
    graph.set_xticks(x)
    datacopy = []
    n = len(data)
    for i in range(n):
        if i % 14 == 0:
            datacopy.append(data[i][0].strftime("%Y-%m-%d"))
        elif i == n - 1:
            datacopy.append(data[i][0].strftime("%Y-%m-%d"))
        else:
            datacopy.append(" ")
            # Set the xtick labels to correspond to just the dates you entered.

    # graph.set_xticklabels( [date.strftime("%Y-%m-%d") for (date, value) in data])

    graph.set_xticklabels([date for date in datacopy])

    plt.xlabel('Date')
    plt.ylabel('Article Length')
    plt.title('Graph - Date vs Article-Length')
    plt.grid(True)
    plt.show()

plotLength()

