#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 16:01:52 2017

@author: akashmantry
"""

from models import IndexerModel, IdfModel, UrlVectorModel, PageRankModel
import mongoengine
import numpy as np
from text_utils import TextFilter
import operator     
from utils.utils import get_unique_words_from_file   
                
def make_query_vector(query, unique_word_list):
    filtered_query = TextFilter.filter_text(query)
    
    vector_query = {}
    for word in unique_word_list:
        vector_query[word] = 0
            
    query_words = filtered_query.split()
    
    tf_query = {}
    length_of_query = len(query_words)        
    
    for word in query_words:
        if word in vector_query:
            tf_query[word] = query_words.count(word)/length_of_query
            try:
                idf_model_object = IdfModel.objects(word=word).get()
            except:
                continue
            else:
                vector_query[word] = tf_query[word] * idf_model_object.idf

    return vector_query

def get_matching_urls(query):
    filtered_query = TextFilter.filter_text(query)
    matching_urls = set()
    
    for word in filtered_query.split():
        try:
            indexer_object = IndexerModel.objects(word=word).get()
        except:
            continue
        else:
            for url in indexer_object.urls:
                matching_urls.add(url)
            
    return list(matching_urls)

def cosine_similarity(vector_query, document, unique_word_list):
    document_object = UrlVectorModel.objects(url=document).get()
    document_vector = dict(document_object.vector)
    
    document_vector_list = []
    vector_query_list = []
    for word in unique_word_list:
        document_vector_list.append(document_vector[word])
        vector_query_list.append(vector_query[word])
    
    dot_product = np.dot(document_vector_list, vector_query_list)
    magnitude_of_document_vector = np.linalg.norm(document_vector_list)
    magnitude_of_query_vector = np.linalg.norm(vector_query_list)
    
    similarity = dot_product/(magnitude_of_document_vector * magnitude_of_query_vector)
    return similarity
    
def compare_query_and_matching_urls(vector_query, matching_urls, unique_word_list):
    url_and_similarity = {}
    for url in matching_urls:
        similarity = cosine_similarity(vector_query, url, unique_word_list)
        url_and_similarity[url] = similarity
    return url_and_similarity
 
def rank_query(url_and_similarity):
    for url in url_and_similarity:
        page_rank_object = PageRankModel.objects(url=url).get()
        url_and_similarity[url] = 6 * url_and_similarity[url] + page_rank_object.rank
    return sorted(url_and_similarity.items(), key=operator.itemgetter(1), reverse=True)
        

query = 'Aloyze Vanessa Laws Kansas assistance elected worship likvidacija prayer gugugug ABSEES'
unique_word_list = get_unique_words_from_file()
vector_query = make_query_vector(query, unique_word_list)
matching_urls = get_matching_urls(query)
url_and_similarity = compare_query_and_matching_urls(vector_query, matching_urls, unique_word_list)
url_and_rank = rank_query(url_and_similarity)









