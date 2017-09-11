#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 22:04:52 2017

@author: akashmantry
"""

import os
from models import ParserModel
from bs4 import BeautifulSoup
from readability.readability import Document
from text_utils import TextFilter


class Parser:
    def __init__(self, path):
        self.path = path
    
    @staticmethod
    def parse_document(url, htmltext):
        print ("Parsing " + url)
        try:
            readable_article = Document(htmltext).summary()
            readable_title = Document(htmltext).short_title()

            soup = BeautifulSoup(readable_article, "html.parser")
            final_article = soup.text
        except Exception as e:
            print (str(e))
            final_article = ''
        cleaned_final_article = TextFilter.filter_text(final_article)
        Parser.store_data_in_db(url, cleaned_final_article)
    
    @staticmethod
    def store_data_in_db(url, text):
        parser_object = ParserModel(url=url, text=text)
        parser_object.save()
            
    def read_html_files(self):
        for file_name in os.listdir(self.path):
            file_path = self.path + '/' + file_name
            with open(file_path, 'rt', encoding='utf-8') as f:
                temp_list = f.readlines()
            url = temp_list[0].strip()
            document = ''.join(temp_list[1:])
            print('Parsing ', url)
            Parser.parse_document(url, document)
        
parser = Parser('/Users/akashmantry/Documents/folfox_search/FolfoxSearch/100_files')
parser.read_html_files()