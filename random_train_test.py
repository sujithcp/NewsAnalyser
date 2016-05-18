"""
Suppose you have some texts of news and know their categories.
You want to train a system with this pre-categorized/pre-classified
texts. So, you have better call this data your training set.
"""
import random
import sqlite3
import nltk
from nltk.corpus import stopwords
from generals import tokenize

cats = ['sports', 'health', 'entertainment', 'tech', 'business']
connection = sqlite3.connect('data/news_data.db')
cursor = connection.cursor()

work_data = cursor.execute('''select * from News order by title''').fetchall()
newsSet = []
stopw = set(stopwords.words('english'))
# print(stopw)

for tuple in work_data:
    content = tuple[3]
    print(tuple[2])
    if content.strip() is not '':
        rdata = tokenize(content.strip(),en_stem=True)
        words = rdata.split()
        # print(words)
        string_words = " ".join(words)
        dict = {item: 0 for item in words}
        #print(string_words)
        newsSet.append((dict,tuple[0]))


random.shuffle(newsSet)

train_set = newsSet[:int((len(newsSet)/2))]
test_set = newsSet[int((len(newsSet)/2)):]
cls = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(cls,test_set),len(train_set),len(test_set))
#cls = nltk.NaiveBayesClassifier.train(train_set)


