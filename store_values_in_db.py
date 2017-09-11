#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 11:01:53 2017

@author: akashmantry
"""

from models import IndexerModel, TfModel, IdfModel, UrlVectorModel, TfIdfModel, PageRankModel
import mongoengine
import pandas as pd
import numpy as np
import math
from utils.utils import file_to_dict, get_unique_words_from_file

indexer_file = '/db_dump/indexer.txt'
parsed_pages_file = '/db_dump/parsed_pages.csv'
unique_word_file = '/db_dump/unique_words.txt'
out_links_file = '/db_dump/out_links.json'

translator = str.maketrans('', '', "' ")

df_parsed_pages = pd.read_csv(parsed_pages_file, sep=',')
parsed_pages_urls = df_parsed_pages.iloc[:, 0].values
texts = df_parsed_pages.iloc[:, 1].values

# Change this value depending on the number of urls indexed
total_number_of_docs = 100

def store_indexer_values_in_db():
    df = pd.read_csv(indexer_file,sep='\t')
    words = df.iloc[:, 0].values
    urls = df.iloc[:, 1].values
    
    url_list = []
    for x in urls:
        x = x.translate(translator)
        x=x[5:-2].split(',')
        url_list.append(x)
        
    for i in range(0, len(url_list)):
        indexer_object = IndexerModel(word=words[i].strip(), urls=url_list[i])
        indexer_object.save()
    print('Stored Indexer values in db')
        
def calculate_and_store_tf():
    for row in IndexerModel.objects():
        for url in row.urls:
            index, = np.where(parsed_pages_urls==url)
            converted_to_list = texts[index].tolist()[0].split()
            count = converted_to_list.count(row.word)
            tf = count/len(converted_to_list)
            tf_model_object = TfModel(word=row.word, url=url, tf=tf)
            tf_model_object.save()
    print('Stored Term Frequency values in db')

def calculate_and_store_idf():
    for row in IndexerModel.objects():
        idf = math.log(total_number_of_docs/(1+len(row.urls)), math.e)
        idf_object = IdfModel(word=row.word, idf=idf)
        idf_object.save()
    print('Stored Inverse Document Vector values in db')
        
def calculate_and_store_tf_idf():
    for row in TfModel.objects:
        idf_model_object = IdfModel.objects(word=row.word).get()
        tf_idf_object = TfIdfModel(word=row.word, url=row.url, tf_idf=row.tf*idf_model_object.idf)
        tf_idf_object.save()
    print('Stored Tf-Idf values in db')
    
def save_vectors():
    unique_word_list = get_unique_words_from_file()
    url_vectors = {}
    for url in parsed_pages_urls:
        vector_dict = {}
        for word in unique_word_list:
            vector_dict[word] = 0
        url_vectors[url.strip()] = vector_dict
        
        
    for row in TfIdfModel.objects:
        if row.word in unique_word_list:
            url_vectors[row.url][row.word] = row.tf_idf
        
    for url, vector in url_vectors.items():
        url_vector_object = UrlVectorModel(url=url, vector=vector)
        url_vector_object.save()
    print('Stored url vector values in db')

def compute_ranks(graph_out_dict):
    graph_in_dict = dict()
    ranks_dict = dict()
    damping_factor = 0.8
    number_of_loops = 10
    npages = len(graph_out_dict)
    for page in graph_out_dict:
        ranks_dict[page] = 1.0/npages

    for i in range(0, number_of_loops):
        newranks  = {}
        for page in graph_out_dict:
            newrank = (1 - damping_factor)/npages
            for node in graph_out_dict:
                graph_in_dict[node] = []
                if page in graph_out_dict[node]:
                    newrank = newrank + damping_factor * (ranks_dict[node]/len(graph_out_dict[node]))
                    graph_in_dict[node].append(page)
            newranks[page] = newrank
        ranks_dict = newranks
        
    for page, rank in ranks_dict.items():
        page_rank_object = PageRankModel(url=page, rank=rank)
        page_rank_object.save()
    
def rank():
	print ("Starting to rank pages now")
	graph_out_dict = file_to_dict(out_links_file)
	compute_ranks(graph_out_dict)
	print ("Ranking completed")
    
store_indexer_values_in_db()
calculate_and_store_tf()
calculate_and_store_idf()
calculate_and_store_tf_idf()
save_vectors()
rank()
    

