import sqlite3

connection = sqlite3.connect('../data/news_data.db')
cursor = connection.cursor()


data = cursor.execute('''select title,count(title) c from News group by title having c>1''').fetchall()


for t in data:
    titles = t[0].split('\n')
    for i in titles:
        print(i)
        data_set = cursor.execute('''select * from News where title = ? limit 1''',(i,))
        cursor.execute('''delete from News where title = ?''',(i,))
        for j in data_set:
            print(j[0],j[1],j[2],j[4],j[5])
            cursor.execute("insert or ignore into News(id,title,news,category,date,time,link) values(?,?,?,?,?,?,?)",
             (j[1], j[2], j[3], j[0], j[4], j[5], j[6],))
connection.commit()
    #for item in tuple:
        #cursor.execute('''delete from News where title = ?''',(item[2],))
        #print(item)
        #cursor.execute("insert or ignore into News(id,title,news,category,date,time,link) values(?,?,?,?,?,?,?)",
                       #(item[1], item[2], item[3], item[0], item[4], item[5], item[6],))
        #connection.commit()
