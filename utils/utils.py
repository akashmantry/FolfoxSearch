import mongoengine
import json
import os

unique_word_file = '/Users/akashmantry/Documents/folfox_search/FolfoxSearch/db_dump/unique_words.txt'

#Use this function to store unique words in a file if it doesn't exist
def get_unique_words_to_form_the_vector(IndexerModel):
    unique_word_list = []
    for row in IndexerModel.objects():
        if len(row.urls) == 1:
            unique_word_list.append(row.word)
            
    with open(unique_word_file, 'w') as f:
        for word in unique_word_list:
            f.write("%s\n" % word)
    return unique_word_list

def get_unique_words_from_file():
    unique_words = list()

    with open(unique_word_file, 'r') as f:
        for word in f.readlines():
            unique_words.append(word.strip('\n'))
    return unique_words

# Utility function to convert out_links file to a dictionary.
# This out_links was calculated while crawling.
def file_to_dict(file_name):
    results = dict()
    with open(file_name) as data_file:
        if os.stat(file_name).st_size == 0:
            return results
        results = json.load(data_file) 
    return results

