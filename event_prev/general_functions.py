import re
import nltk
import sqlite3


with open('stopwords.txt', 'r') as stopwd_ref:
    stopwd = stopwd_ref.read()
stopwd = re.split('\n', stopwd)



def fetchNewsFromDb(start_date=None, end_date=None):
    connection = sqlite3.connect('data/news_data.db')
    cursor = connection.cursor()
    if not start_date or not end_date:
        data = cursor.execute('''select * from News''').fetchall()
    else:
        data = cursor.execute('''select * from News where ? <= date and date <= ?  order by date asc,time asc''', (start_date, end_date,)).fetchall()
    return data



def word_grams(tokens):
    word_phrase = []
    n=3
    while n>1:
        for ngram in nltk.ngrams(tokens, n):
            word_phrase .append(' '.join(i for i in ngram))
        n-=1

        word_phrase_copy = word_phrase .copy()
        for ngram in word_phrase_copy :
            word=ngram.strip().split(' ')
            i=0
            correct=0
            digit=0
            for i in range(len(word)):
                if word [i].isdigit():
                    digit+=1
                elif word[i] not in stopwd :
                    correct+=1
            if correct+digit<2 or word[0] in stopwd or word [-1] in stopwd or correct<digit:
                word_phrase .remove(ngram )
    return word_phrase



def Tokenize(text):
    text=text.replace('\n','')
    text=text.split('.')
    if '' in text:
        text.remove('')
    word_phrase = []
    #textcopy=''
    for line in text:
        tokens = re.findall("[a-zA-Z0-9]+|[a-zA-Z0-9]+['.,-][a-zA-Z0-9]+", line.replace("'",''))
        word_phrase.extend(word_grams(tokens))
    return (word_phrase)