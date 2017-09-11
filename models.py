#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 23:43:05 2017

@author: akashmantry
"""

from mongoengine import *
connect('indexer')

class IndexerModel(Document):
    word = StringField(required=True)
    urls = ListField(required=True)
    
    meta = {'collections':'indexer'}

class ParserModel(Document):
    url = StringField(required=True)
    text = StringField(required=True)
    
    meta = {'collection': 'parsed_pages'}
    

class TfIdfModel(Document):
    word = StringField(required=True)
    url = StringField(required=True)
    tf_idf = FloatField(required=True)
    
    meta = {'collection': 'tf_idf',
            'indexes':[
                    'word',
                    'url'
                    ]}
    
class IdfModel(Document):
    word = StringField(required=True)
    idf = FloatField(required=True)
    
    meta = {'collection': 'idf',
            'indexes':[
                    'word'
                    ]}
    
class TfModel(Document):
    word = StringField(required=True)
    url = StringField(required=True)
    tf = FloatField(required=True)
    
    meta = {'collection': 'tf',
            'indexes':[
                    'word',
                    'url'
                    ]}
    
class VectorModel(EmbeddedDocument):
    word = StringField(required=True)
    tf_idf = FloatField(required=True)
    
    
class UrlVectorModel(Document):
    url = StringField(required=True)
    vector = EmbeddedDocumentListField(VectorModel)
    
    meta = {'collection': 'url_vector',
            'indexes':[
                    'url'
                    ]}
            
class PageRankModel(Document):
    url = StringField(required=True)
    rank = FloatField(required=True)
    
    meta = {'collection': 'page_rank',
            'indexes':[
                    'url'
                    ]}