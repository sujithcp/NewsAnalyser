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
from matplotlib import pyplot as plt

'''
cats = ['sports', 'health', 'entertainment', 'tech', 'business']
connection = sqlite3.connect('../data/news_data.db')
cursor = connection.cursor()

total = 1000
accuracy=[]

work_data = cursor.execute("select * from News order by title ").fetchall()

stopw = set(stopwords.words('english'))
# print(stopw)
test_set =[]

for tuple in work_data:
    content = tuple[3]
    print(tuple[2])
    if content.strip() is not '':
        rdata = tokenize(content.strip(), en_stem=True)
        words = rdata.split()
        # print(words)
        string_words = " ".join(words)
        dict = {item: 0 for item in words}
        # print(string_words)
        test_set.append((dict, tuple[0]))


while total < 9000 :
    n= total//5
    train_set = []
    for cls in cats:

        work_data = cursor.execute("select * from News where category = ? limit ? ",(cls,n,)).fetchall()

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
                train_set .append((dict,tuple[0]))


    cls = nltk.NaiveBayesClassifier.train(train_set)
    accuracy .append(nltk.classify.accuracy(cls,test_set))

    print('\n----------------')
    print(total)
    print('----------------\n')
    #cls = nltk.NaiveBayesClassifier.train(train_set)

    total+=500

print (accuracy  )
'''

accuracy =[0.8897025687246507, 0.9072780531771069, 0.9289094186570527, 0.9425416854438936, 0.9486255069851285, 0.9530193780982424, 0.9568499324019829, 0.9558359621451105, 0.9598918431726002, 0.9577512392969806, 0.9591031996394772, 0.9582018927444795, 0.9573005858494817, 0.9579765660207301, 0.9587652095538531, 0.9591031996394772]
def plot_accuracy():
    x=[i for i in range(1000,9000,500)]
    y=[float(acc*100) for acc in accuracy ]
    print(x)
    print(y)
    fig = plt.figure()
    graph = fig.add_subplot(111)
    graph.plot(x, y, 'b-', linewidth=1.5)
    graph.set_xticks(x)
    plt.xlabel('Total no. of articles')
    plt.ylabel('Accuracy')
    plt.title('Graph - Article count vs Accuracy')
    plt.grid(True)
    plt.ylim(0, 110)
    plt.savefig('Accuracy2.png')
    plt.show()

plot_accuracy()


