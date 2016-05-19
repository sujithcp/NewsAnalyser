
from matplotlib import pyplot as plt
from matplotlib.dates import  date2num
import sqlite3
import datetime as DT

def plotDB():
    connection=sqlite3.connect('../data/news_data.db')
    cursor = connection .cursor()

    data= cursor.execute('''select date, count(title) as count from News where date>="2016-04-01" group by date''')

    data=[i for i in data if i[0] != 'NULL']

    data = [(DT.datetime.strptime(i[0], "%Y-%m-%d"), i[1]) for i in data]


    x = [date2num(date) for (date, value) in data]
    y = [value for (date, value) in data]

    fig = plt.figure()

    graph = fig.add_subplot(111)

# Plot the data as a red line with round markers
    graph.plot(x, y, 'b-o')

# Set the xtick locations to correspond to just the dates you entered.
    graph.set_xticks(x)
    datacopy=[]
    n=len(data)
    for i in  range(n):
        if i%14==0:
            datacopy .append(data[i][0].strftime("%Y-%m-%d") )
        elif i==n-1:
            datacopy.append(data[i][0].strftime("%Y-%m-%d"))
        else:
            datacopy.append(" ")
# Set the xtick labels to correspond to just the dates you entered.

    #graph.set_xticklabels( [date.strftime("%Y-%m-%d") for (date, value) in data])

    graph.set_xticklabels([date for date in datacopy ])

    plt.show()

plotDB()

