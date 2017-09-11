from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re
from .english_stopwords import stop_words
import string


class TextFilter:

    stop_words = set(stop_words)
    regex_non_ascii = re.compile(r'[^\x00-\x7F]+')
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    ps = PorterStemmer()
    
    @staticmethod
    def filter_text(text):

        filtered_text = text.lower()
        filtered_text = TextFilter.clean_non_ascii(filtered_text)
        filtered_text = filtered_text.translate(TextFilter.translator)
        filtered_text = word_tokenize(filtered_text)
        words = set(filtered_text) - TextFilter.stop_words
        stemmed_words = []
        for word in words:
            word = ''.join([i for i in word if not i.isdigit()])
            stemmed_words.append(TextFilter.ps.stem(word))
        set_stemmed_words = set(stemmed_words)
        return " ".join(set_stemmed_words)
    
        
    @staticmethod
    def clean_non_ascii(text):
        return re.sub(TextFilter.regex_non_ascii, "", text)

    
