#-*- coding:utf-8 _*-
""" 
@author:yvan 
@file: lda_test.py 
@time: 2017/08/13 
"""
import sys
from gensim import corpora

reload(sys)
sys.setdefaultencoding('utf8')

documents = ["Human machine interface for lab abc computer applications",
    "A survey of user opinion of computer system response time",
    "The EPS user interface management system",
    "System and human system engineering testing of EPS",
    "Relation of user perceived response time to error measurement",
    "The generation of random binary unordered trees",
    "The intersection graph of paths in trees",
    "Graph minors IV Widths of trees and well quasi ordering",
    "Graph minors A survey"]
"""
#use StemmedCountVectorizer to get stemmed without stop words corpus
Vectorizer = StemmedCountVectorizer
# Vectorizer = CountVectorizer
vectorizer = Vectorizer(stop_words='english')
vectorizer.fit_transform(documents)
texts = vectorizer.get_feature_names()
# print(texts)
"""
texts = [doc.lower().split() for doc in documents]
print 'text'
print(texts)
print 'dict'
dict = corpora.Dictionary(texts)    # 自建词典
print dict, dict.token2id
# 通过dict将用字符串表示的文档转换为用id表示的文档向量
corpus = [dict.doc2bow(text) for text in texts]
print 'corpus'
print(corpus)