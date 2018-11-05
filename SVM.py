# -*- coding: utf-8 -*-
import jieba
from sklearn import svm
from gensim import corpora
import nltk
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

#获取所有单词
def getAllWords(lines):
    words = []
    # for line in lines:
    #     sens = nltk.sent_tokenize(line)
    #     for sent in sens:
    #         for i in nltk.word_tokenize(sent):
    #             if i not in words:
    #                 words.append(i)
    for line in lines:
        for i in jieba.cut(line):
            if i not in words:
                words.append(i)
    print words
    return words



#每篇文章一个词向量
def getVocter(d,words):
    ws = []
    v = []
    # sens = nltk.sent_tokenize(d)
    # for sent in sens:
    #     for i in nltk.word_tokenize(sent):
    #         ws.append(i)
    # for w in words:
    #     number = ws.count(w)
    #     v.append(number)
    for i in jieba.cut(d):
        ws.append(i)
    for w in words:
        number = ws.count(w)
        v.append(number)
    return v

#矩阵
def CVS(ls1,words):
    vs1 = []
    count = 0
    number = len(ls1)
    for d in ls1:
        count = count + 1
        print "进度: " + str(count) + " % " + str(number)
        v = getVocter(d, words)
        vs1.append(v)
    return vs1

filename = "note_training.txt"
fp = open(filename)
x = []#traing samples
y = []#training target
clf = svm.SVC() #class
t = ""
for i in fp.read().split('\n'):
    t = i.split('	')
    if t == ['']:
        break
    print t
    y.append(t[1])
    x.append(t[2])
words = getAllWords(x)
vs1 = CVS(x,words)
clf.fit(vs1,y)

filename="note_unknown.txt"
fp = open(filename)
for i in fp.read().split('\n'):
    t = i.split('	')
    if t == ['']:
        break
    string = t[1]
    vec = getVocter(string,words)
    result = clf.predict(vec)
    print t[0] + "结果为:" + str(result)
# for i in xrange(1,41):
#     filename = './ham/%d.txt' % i
#     string = open(filename).read()
#     vec = getVocter(string,words)
#     result = clf.predict(vec)
#     print result
# for i in xrange(1,41):
#     filename = './spam/%d.txt' % i
#     string = open(filename).read()
#     vec = getVocter(string,words)
#     result = clf.predict(vec)
#     print result