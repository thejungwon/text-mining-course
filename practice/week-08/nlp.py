import csv
from konlpy.tag import Okt
import pandas as pd
import numpy as np


def get_data(path='data/article_sample.txt'):
    document_list = []
    with open(path, encoding="utf-8") as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            #0: 토픽, 1: 출처, 2: 날짜, 3: 제목, 4: 내용 
            label = row[0]
            source = row[1]
            datetime = row[2]
            title = row[3]
            content = row[4]
            document_list.append([label, source, datetime, title, content])
    return document_list

def get_nouns(documents):
    stops_words = []
    okt = Okt()
    with open('data/stopword.txt', encoding="utf-8") as f:
        for line in f.readlines():
            stops_words.append(line.strip())
    
    POS_LIST = ["Noun"]
    tokenized_sentence_list = []
    for document in documents:
        tokens = []
        for pos in okt.pos(document):
            condition = pos[1] in POS_LIST and pos[0] not in stops_words
            if condition:
                tokens.append(pos[0])
        tokenized_sentence_list.append(tokens)
    return tokenized_sentence_list
def get_tf_matrix(tokennized_documents):
    unique_terms = []
    for tokennized_document in tokennized_documents:
        unique_terms += tokennized_document
        unique_terms= list(set(unique_terms))
        unique_terms = sorted(unique_terms)
    tf_matrix = np.zeros((len(tokennized_documents), len(unique_terms)))
    
    for row_n, tokennized_document in enumerate(tokennized_documents):
        for token in tokennized_document:
            col_n = unique_terms.index(token)
            tf_matrix[row_n,col_n]+=1

    tf_matrix_origin = pd.DataFrame(data=tf_matrix,columns=unique_terms)
    tf_matrix = tf_matrix_origin.div(tf_matrix_origin.sum(axis=1), axis=0)
    return tf_matrix
def get_tf_idf_matrix(tokennized_documents):
    unique_terms = []
    for tokennized_document in tokennized_documents:
        unique_terms += tokennized_document
        unique_terms= list(set(unique_terms))
        unique_terms = sorted(unique_terms)
    tf_matrix = np.zeros((len(tokennized_documents), len(unique_terms)))
    
    for row_n, tokennized_document in enumerate(tokennized_documents):
        for token in tokennized_document:
            col_n = unique_terms.index(token)
            tf_matrix[row_n,col_n]+=1

    tf_matrix_origin = pd.DataFrame(data=tf_matrix,columns=unique_terms)
    tf_matrix = tf_matrix_origin.div(tf_matrix_origin.sum(axis=1), axis=0)
    
    df_matrix = (tf_matrix_origin>0).sum(axis=0)
    N = tf_matrix.shape[0]
    idf_matrix = np.log(N/df_matrix+1)
    tf_idf_matrix = tf_matrix * idf_matrix
    return tf_idf_matrix
  
    

