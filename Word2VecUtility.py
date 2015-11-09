__author__ = 'saniyasaifee'
#!/usr/bin/env python

import re
import nltk
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
#Word2VecUtility is a utility class for processing raw HTML text into segments for further learning
class Word2VecUtility(object):

    # Function to convert a document to a sequence of words,
    # optionally removing stop words.  Returns a list of words.
    @staticmethod
    def review_to_wordlist(review, remove_stopwords = False):
        # 1. Remove HTML
        review_text = BeautifulSoup(review).get_text()

        # 2. Remove non-letter
        review_text = re.sub("[^a-zA-Z]", " ", review_text)

        # 3. convert words to lower case and split them
        words = review_text.lower().split()

        # 4. optionally remove stopwords
        if remove_stopwords:
            stops = set(stopwords.words("english"))
            words = [w for w in words if not w in stops]
        return words

    # Define a function to split the review into parsed sentences
    # Returns a list of sentences, where each sentence is a list of words
    @staticmethod
    def review_to_sentences(review, tokenizer, remove_stopwords=False):
        # 1. Use NLTK tokenzer to split the paragraph into sentences
        raw_sentences = tokenizer.tokenize(review.decode('utf8').strip())

        # 2. Loop over each sentence
        sentences = []
        for raw_sentence in raw_sentences:
            # if a sentencce is empty skip it
            if len(raw_sentence)>0:
                # Otherwise, call review_to_wordlist to get a list of words
                sentences.append(Word2VecUtility.review_to_wordlist(raw_sentence, remove_stopwords))
        return sentences