#-*- coding:utf-8 _*-
"""
@author:yvan
@file: lda_train.py
@time: 2017/08/14
"""
import sys
import os
import jieba
import codecs
from gensim.corpora import Dictionary
from gensim.models import LdaModel
reload(sys)
sys.setdefaultencoding('utf8')
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def list_dir(rootDir):

    # 把停用词做成字典
    stopwords = {}
    fstop = open('stopwords.txt', 'r')
    for eachWord in fstop:
        stopwords[eachWord.strip().decode('utf-8', 'ignore')] = eachWord.strip().decode('utf-8', 'ignore')
    fstop.close()
    train_set = []
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir,lists)
        print path
        filer = open(path,'r')
        strr = ''
        for line in filer:
            strr = strr + line
        res  = jieba_s(strr,stopwords)
        # filew = open('./res/'+ path.split('-')[1],'w')
        # filew.write(res)
        train_set.append(res)
        return train_set

def jieba_s(strr,stopwords):
    wordList = jieba.cut(strr,cut_all=False)
    outStr = []
    for word in wordList:
        if word not in stopwords:
            outStr.append(word)
    return outStr

def Train(train_set):

    # stopwords = codecs.open('stopwords.txt', 'r', encoding='utf8').readlines()
    # stopwords = [w.strip() for w in stopwords]
    # train_set = []
    # for line in train:
    #     line = list(jieba.cut(line))
    #     train_set.append([w for w in line if w not in stopwords])


    # 构建训练语料
    dictionary = Dictionary(train_set)
    corpus = [dictionary.doc2bow(text) for text in train_set]

    # lda模型训练
    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=20)
    lda.print_topics(20)


if __name__ == "__main__":
    # list_dir("./paragraph")
    Train(list_dir("./paragraph"))