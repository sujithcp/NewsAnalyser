'''
Classify a paragraph of text
Read the text from stdin
Press ctrl+D to end reading

'''



import sys

from stemming.porter2 import stem

from news_classifier import getClassifier

choice = input("Want to teach [Y/n]\n")

if choice.lower() == 'y':
    classifier = getClassifier(force_train=True)
else:
    classifier = getClassifier()

print("Data >>>")
text = sys.stdin.read().lower()
text = [stem(item) for item in text.split()]
dict = {item: 0 for item in text}
print(classifier.classify(dict))
