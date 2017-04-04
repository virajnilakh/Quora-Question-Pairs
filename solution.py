import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
train = pd.read_csv("./train.csv")[:40000]
#test = pd.read_csv("../input/test.csv")[:100]
def getWords(text):
    unFilteredList = re.compile('[a-zA-Z]+').findall(text)
    filteredList=[]
    for w in unFilteredList:
        w = w.lower()
        if w in stop_words:
            continue
        filteredList.append(w)
    return filteredList
i=0
for l in train.question1:
    train.question1[i]=getWords(train.question1[i])
    train.question2[i]=getWords(train.question2[i])
    i+=1
#print train
i=0
duplicateWordsList=[]
nonDuplicateWordsList=[]
def getDiff(l1,l2):
    diff=[]
    i=0
    for w in l1:
        if w not in l2:
            diff.append(w)
        else:
            l2.remove(w)
    for w in l2:
        diff.append(w)
    return diff
i=0
for l in train.question1:
    diff=getDiff(l,train.question2[i])
    if train.is_duplicate[i]:
        for w in diff:
            duplicateWordsList.append(w)
    else:
        for w in diff:
            nonDuplicateWordsList.append(w)
    i+=1
test = pd.read_csv("./train.csv")[40001:50000]
i=0
for l in test.question1:
    test.question1[40001+i]=getWords(test.question1[40001+i])
    test.question2[40001+i]=getWords(test.question2[40001+i])
    i+=1
i=0
ans={}
actual={}
accuracy=0
for l in test.question1:
    score=0
    diff=getDiff(l,test.question2[40001+i])
    for w in diff:
        if w in duplicateWordsList:
            score+=1
        if w in nonDuplicateWordsList:
            score-=1
    actual[40001+i]=test.is_duplicate[40001+i]
    if score>0:
        ans[40001+i]=1
    else:
        ans[40001+i]=0
    if(actual[40001+i]==ans[40001+i]):
        accuracy+=1
    i+=1


print accuracy,i,accuracy//i
