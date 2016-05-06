import re
import nltk
from nltk.corpus import stopwords

with open('stopwords.txt', 'r') as stopwd_ref:
    stopwd = stopwd_ref.read()
stopwd = re.split('\n', stopwd)

def word_grams(tokens):
    word_phrase = []
    n=5
    while n>0:
        for ngram in nltk.ngrams(tokens, n):
            word_phrase .append(' '.join(i for i in ngram))
        n-=1
    return word_phrase


def Tokenize(text):
    '''Opening the file to tokenize the content'''
   # with open(fname,'r', encoding='utf-8', errors='ignore') as file_ref:
    #    text=file_ref .read().lower()
    text=text.replace('\n','')
    text=text.split('.')
    if '' in text:
        text.remove('')
    word_phrase = []
    textcopy=''
    for line in text:
        tokens = re.findall('[a-zA-Z0-9]+', line)
        #Extracting the tokens using regular expression'''
        #    '''stopw = stopwords in nltk '''
        stopw = set(stopwords.words('english'))
        tokenscopy = tokens.copy()
        for token in tokenscopy:
            if token in stopw or token in stopwd or token .isdigit() :
                tokens.remove(token)
        textcopy +=' '.join(tokens)
        word_phrase.extend(word_grams(tokens))

    return (word_phrase,textcopy )