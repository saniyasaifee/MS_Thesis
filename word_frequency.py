#!/usr/bin/python
from __future__ import division
import sys, getopt
import nltk
from nltk.corpus import reuters, stopwords, brown
from Tkinter import *
import ttk
from nltk.collocations import *
import Tkconstants, tkFileDialog
import re
import requests
from bs4 import BeautifulSoup

REGEX = r'About (.*) results'


class ListBoxChoice(object):
    def __init__(self, master=None, title=None, message=None, list=[]):
        self.master = master
        self.master.title("Find word frequency")
        #self.master.attributes('-fullscreen', True)
        self.corpus_value = None
        self.unigram = False
        self.bigram = False
        self.trigram = False
        self.list = list[:]

        # self.listFrame = Frame(self.master)

        if message:
            Label(self.master, text=message).grid(row=0)

            # listFrame = Frame(self.modalPane)
            # self.listFrame.pack(side=TOP, padx=5, pady=5)
            # scrollBar = Scrollbar(self.listFrame)
            # scrollBar.pack(side=RIGHT, fill=Y)
        self.listBox = Listbox(self.master, height=2, selectmode=SINGLE)
        self.listBox.grid(row=1, column=0, padx=5, pady=5)
        # scrollBar.config(command=self.listBox.yview)
        # self.listBox.config(yscrollcommand=scrollBar.set)
        self.list.sort()
        self.listBox.insert(END, "Reuter corpus")
        self.listBox.insert(END, "Brown corpus")
        self.listBox.bind('<<ListboxSelect>>', self._choose)
        # buttonFrame = Frame(self.listFrame)
        # buttonFrame.pack(side=BOTTOM)

        chooseButton1 = Button(self.master, text="Unigram Frequency", command=self._setUnigram)
        chooseButton1.grid(row=1, column=1)
        chooseButton2 = Button(self.master, text="Bigram Frequency", command=self._setBigram)
        chooseButton2.grid(row=1, column=2)
        chooseButton3 = Button(self.master, text="Trigram Frequency", command=self._setTrigram)
        chooseButton3.grid(row=1, column=3)
        chooseButton4 = Button(self.master, text="LSA", command=self._setLSA)
        chooseButton4.grid(row=1, column=4)
        cancelButton = Button(self.master, text="Cancel", command=self._cancel)
        cancelButton.grid(row=1, column=5)

    def _choose(self, event=None):
        try:
            firstIndex = self.listBox.curselection()[0]
            self.corpus_value = firstIndex
        except IndexError:
            print "error"
            self.corpus_value = None
            # self.modalPane.destroy()

    def new_window(self):
        # self.newWindow = Toplevel(self.master)
        self.app = Unigram(self.master, self.corpus_value)

    def _setUnigram(self, event=None):
        self.unigram = True
        self.ngramLF = LabelFrame(self.master, text="Unigram", padx=10, pady=10)
        self.ngramLF.grid(row=2, column=0, rowspan=4, columnspan=3, sticky=W + E + N + S)
        Label(self.ngramLF, text="Enter word for unigram frequency evaluation in universal set").grid(row=0)
        word = StringVar()
        self.file_name = StringVar()
        word_ug_corpus = Entry(self.ngramLF, bd=1, textvariable=word).grid(row=0, column=1)
        button_ug = Button(self.ngramLF, text="find", width=10, command=lambda: self.callback1_bigram(word.get())).grid(row=0,
                                                                                                                 column=2)
        Label(self.ngramLF, text="Select test document for unigram evaluation").grid(row=2)
        test_file_entry = Entry(self.ngramLF, bd=1, textvariable=self.file_name).grid(row=2, column=1)
        # define buttons
        Button(self.ngramLF, text='askopenfile', command=self.selectfile).grid(row=2, column=2)
        word_test = StringVar()
        Label(self.ngramLF, text="Enter word for unigram frequency evaluation in test document").grid(row=3)
        word_ug_test = Entry(self.ngramLF, bd=1, textvariable=word_test).grid(row=3, column=1)
        button_ug_test = Button(self.ngramLF, text="find", width=10,
                                command=lambda: self.callback1_test(word_test.get())).grid(row=3, column=2)
        if self.file_name != '':
            print self.file_name
            # self.frame = Frame(self.master)

    def _setBigram(self, event=None):
        self.bigram = True
        self.ngramLF = LabelFrame(self.master, text="Bigram", padx=10, pady=10)
        self.ngramLF.grid(row=2, column=0, rowspan=4, columnspan=3, sticky=W + E + N + S)
        Label(self.ngramLF, text="Enter word for bigram frequency evaluation in universal set").grid(row=0)
        word = StringVar()
        self.file_name = StringVar()
        word_ug_corpus = Entry(self.ngramLF, bd=1, textvariable=word).grid(row=0, column=1)
        button_bg = Button(self.ngramLF, text="find", width=10, command=lambda: self.callback1_bigram(word.get())).grid(
            row=0,
            column=2)
        Label(self.ngramLF, text="Select test document for bigram evaluation").grid(row=2)
        test_file_entry = Entry(self.ngramLF, bd=1, textvariable=self.file_name).grid(row=2, column=1)
        # define buttons
        Button(self.ngramLF, text='askopenfile', command=self.selectfile).grid(row=2, column=2)
        word_test = StringVar()
        Label(self.ngramLF, text="Enter two words for bigram frequency evaluation in test document").grid(row=3)
        word_bg_test = Entry(self.ngramLF, bd=1, textvariable=word_test).grid(row=3, column=1)
        button_bg_test = Button(self.ngramLF, text="find", width=10,command=lambda: self.callback1_test_bigram(word_test.get())).grid(row=3, column=2)
        if self.file_name != '':
            print self.file_name
            # self.frame = Frame(self.master)
            
    def _setTrigram(self, event=None):
        self.trigram = True
        self.ngramLF = LabelFrame(self.master, text="Trigram", padx=10, pady=10)
        self.ngramLF.grid(row=2, column=0, rowspan=4, columnspan=3, sticky=W + E + N + S)
        Label(self.ngramLF, text="Enter word for Trigram frequency evaluation in universal set").grid(row=0)
        word = StringVar()
        self.file_name = StringVar()
        word_ug_corpus = Entry(self.ngramLF, bd=1, textvariable=word).grid(row=0, column=1)
        button_bg = Button(self.ngramLF, text="find", width=10, command=lambda: self.callback1_bigram(word.get())).grid(
            row=0,
            column=2)
        Label(self.ngramLF, text="Select test document for Trigram evaluation").grid(row=2)
        test_file_entry = Entry(self.ngramLF, bd=1, textvariable=self.file_name).grid(row=2, column=1)
        # define buttons
        Button(self.ngramLF, text='askopenfile', command=self.selectfile).grid(row=2, column=2)
        word_test = StringVar()
        Label(self.ngramLF, text="Enter three words for trigram frequency evaluation in test document").grid(row=3)
        word_bg_test = Entry(self.ngramLF, bd=1, textvariable=word_test).grid(row=3, column=1)
        button_bg_test = Button(self.ngramLF, text="find", width=10, command=lambda: self.callback1_test_trigram(word_test.get())).grid(row=3, column=2)
    
    def _setLSA(self, event=None):
        self.trigram = True
        word = StringVar()
        self.file_name = StringVar()
        self.ngramLF = LabelFrame(self.master, text="LSA", padx=10, pady=10)
        self.ngramLF.grid(row=2, column=0, rowspan=4, columnspan=3, sticky=W + E + N + S)
        Label(self.ngramLF, text="Select test document for Trigram evaluation").grid(row=0)
        test_file_entry = Entry(self.ngramLF, bd=1, textvariable=self.file_name).grid(row=0, column=1)
        # define buttons
        Button(self.ngramLF, text='askopenfile', command=self.selectfile).grid(row=0, column=2)
        button_bg_test = Button(self.ngramLF, text="Calculate LSA", width=10, command=lambda: self.callback1_test_LSA()).grid(row=0, column=3)

    def selectfile(self):

        """Returns an opened file in read mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """
        # get filename
        filename = tkFileDialog.askopenfilename(multiple=False)
        # open file on your own
        if filename:
            self.file_name.set(filename)

    def callback1(self, word):
        print word
        stop_words = stopwords.words('english')
        user_input = self.corpus_value  # raw_input('Please enter:\n  1 if you want the Reuter corpus and \n  2 for Brown corpus:')
        if user_input == '0':
            universal_words = [w.lower() for w in reuters.words() if
                               w.lower().isalpha() and w.lower() not in stop_words]
        elif user_input == '1':
            universal_words = [w.lower() for w in brown.words() if w.lower().isalpha() and w.lower() not in stop_words]
        # Porter stemmer is used for stemming the text.
        porter = nltk.PorterStemmer()
        # universal_stemmed_words is a list of words that has been stemmed
        universal_stemmed_words = [porter.stem(t) for t in universal_words]
        # Calculate the probability of occurrence of the word passed as an argument by calculating the the frequency distribution
        #of the word and dividing it by the total number of words in the list
        fdist = nltk.FreqDist(universal_stemmed_words)
        prob_word_univ_set = fdist[porter.stem(word)] / fdist.N()
        prob_word_univ_set = round(prob_word_univ_set, 4)
        Label(self.ngramLF, text="The frequency of the word in the selected corpus is " + str(prob_word_univ_set)).grid(
            row=1)


    def callback1_test(self, test_word_input):
        stop_words = stopwords.words('english')
        a = self.file_name.get()
        print a
        f = open(self.file_name.get(), 'rU')
        raw_test_data = f.read()
        test_words_list = nltk.word_tokenize(raw_test_data)
        # take a subset of universal set here an article of reuters whose categories are tea and barley
        # test_set_words contain only thise words from article that are non- empty and all characters are alphabetic
        # the program also filters out all stop words. We have normalized the text to lowercase
        test_set_words = [w.lower() for w in test_words_list if w.lower().isalpha() and w.lower() not in stop_words]
        # Porter stemmer is used for stemming the text.
        porter = nltk.PorterStemmer()
        # universal_stemmed_words is a list of words that has been stemmed
        test_stemmed_words = [porter.stem(t) for t in test_set_words]
        fdist_test = nltk.FreqDist(test_stemmed_words)
        # Calculate the probability of occurrence of the word passed as an argument by calculating the the frequency distribution
        # of the word and dividing it by the total number of words in the list
        prob_word_test_set = fdist_test[porter.stem(test_word_input.lower())] / fdist_test.N()
        prob_word_test_set = round(prob_word_test_set, 4)
        Label(self.ngramLF, text="The frequency of the word in the test document is " + str(prob_word_test_set)).grid(
            row=4)

    def callback1_test_bigram(self, test_word_input):
        stop_words = stopwords.words('english')
        a = self.file_name.get()
        print test_word_input.lower()
        f = open(self.file_name.get(), 'rU')
        raw_test_data = f.read()
        test_words_list = nltk.word_tokenize(raw_test_data)
        # take a subset of universal set here an article of reuters whose categories are tea and barley
        # test_set_words contain only thise words from article that are non- empty and all characters are alphabetic
        # the program also filters out all stop words. We have normalized the text to lowercase
        test_set_words = [w.lower() for w in test_words_list if w.lower().isalpha() and w.lower() not in stop_words]
        # Porter stemmer is used for stemming the text.
        porter = nltk.PorterStemmer()
        # universal_stemmed_words is a list of words that has been stemmed
        test_stemmed_words = [porter.stem(t) for t in test_set_words]
        # Create your bigrams
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        bgs = nltk.bigrams(test_stemmed_words)
        a = test_word_input.split(' ')
        test_bigram = '';
        for w in a:
            test_bigram = test_bigram + porter.stem(w.lower()) + ' '
        test_bigram = test_bigram.strip()
        print test_bigram
        #compute frequency distribution for all the bigrams in the text
        word_fd = nltk.FreqDist(test_stemmed_words)
        bigram_fd = nltk.FreqDist(bgs)
        finder = BigramCollocationFinder(word_fd, bigram_fd)
        scored = finder.score_ngrams(bigram_measures.raw_freq)
        tokens = test_bigram.split()
        test_bgs = nltk.bigrams(tokens)
        test_bgs = tuple(test_bgs)
        print tuple(test_bgs)
        for k, v in scored:
            if (cmp(k, test_bgs[0]) == 0):
                Label(self.ngramLF, text="The frequency of the bigram in the test document is " + str(v)).grid(row=4)

    def callback1_bigram(self, test_word_input):
        google_main = self.number_of_search_results('\"' + test_word_input + '\"')
        Label(self.ngramLF, text="The string " + test_word_input + " occurred " + str(
            google_main) + " times in the universal set.").grid(row=1)


    

    def callback1_test_trigram(self, test_word_input):
        stop_words = stopwords.words('english')
        a = self.file_name.get()
        print test_word_input.lower()
        f = open(self.file_name.get(), 'rU')
        raw_test_data = f.read()
        test_words_list = nltk.word_tokenize(raw_test_data)
        # take a subset of universal set here an article of reuters whose categories are tea and barley
        # test_set_words contain only thise words from article that are non- empty and all characters are alphabetic
        # the program also filters out all stop words. We have normalized the text to lowercase
        test_set_words = [w.lower() for w in test_words_list if w.lower().isalpha() and w.lower() not in stop_words]
        # Porter stemmer is used for stemming the text.
        porter = nltk.PorterStemmer()
        # universal_stemmed_words is a list of words that has been stemmed
        test_stemmed_words = [porter.stem(t) for t in test_set_words]
        # Create your bigrams
        trigram_measures = nltk.collocations.TrigramAssocMeasures()
        tgs = nltk.trigrams(test_stemmed_words)
        a = test_word_input.split(' ')
        test_bigram = '';
        for w in a:
            test_bigram = test_bigram + porter.stem(w.lower()) + ' '
        test_bigram = test_bigram.strip()
        #compute frequency distribution for all the bigrams in the text
        word_fd = nltk.FreqDist(test_stemmed_words)
        bigram_fd = nltk.FreqDist(tgs)
        finder = TrigramCollocationFinder.from_words(test_stemmed_words)
        scored = finder.score_ngrams(trigram_measures.raw_freq)
        tokens = test_bigram.split()
        test_bgs = nltk.trigrams(tokens)
        test_bgs = tuple(test_bgs)
        flag = 0
        for k, v in scored:
            if cmp(k, test_bgs[0]) == 0:
                flag = 1
                Label(self.ngramLF, text="The frequency of the trigram in the test document is " + str(v)).grid(row=4)
        if flag == 0:
            Label(self.ngramLF, text="The frequency of the trigram in the test document is 0.").grid(row=4)
            
    def callback1_test_LSA(self):
        stop_words = stopwords.words('english')
        a = self.file_name.get()
        print test_word_input.lower()
        f = open(self.file_name.get(), 'rU')
        raw_test_data = f.read()
        test_words_list = nltk.word_tokenize(raw_test_data)
        # take a subset of universal set here an article of reuters whose categories are tea and barley
        # test_set_words contain only thise words from article that are non- empty and all characters are alphabetic
        # the program also filters out all stop words. We have normalized the text to lowercase
        test_set_words = [w.lower() for w in test_words_list if w.lower().isalpha() and w.lower() not in stop_words]
        # Porter stemmer is used for stemming the text.
        porter = nltk.PorterStemmer()
        # universal_stemmed_words is a list of words that has been stemmed
        test_stemmed_words = [porter.stem(t) for t in test_set_words]
        # Create your bigrams
        trigram_measures = nltk.collocations.TrigramAssocMeasures()
        tgs = nltk.trigrams(test_stemmed_words)
        a = test_word_input.split(' ')
        test_bigram = '';
        for w in a:
            test_bigram = test_bigram + porter.stem(w.lower()) + ' '
        test_bigram = test_bigram.strip()
        #compute frequency distribution for all the bigrams in the text
        word_fd = nltk.FreqDist(test_stemmed_words)
        bigram_fd = nltk.FreqDist(tgs)
        finder = TrigramCollocationFinder.from_words(test_stemmed_words)
        scored = finder.score_ngrams(trigram_measures.raw_freq)
        tokens = test_bigram.split()
        test_bgs = nltk.trigrams(tokens)
        test_bgs = tuple(test_bgs)
        flag = 0
        for k, v in scored:
            if cmp(k, test_bgs[0]) == 0:
                flag = 1
                Label(self.ngramLF, text="The frequency of the trigram in the test document is " + str(v)).grid(row=4)
        if flag == 0:
            Label(self.ngramLF, text="The frequency of the trigram in the test document is 0.").grid(row=4)


    def _cancel(self, event=None):
        self.master.destroy()

    def returnValue(self):
        self.master.wait_window(self.master)
        return self.corpus_value

    def close_windows(self):
        self.master.destroy()

    def number_of_search_results(self, key):
        url = google_main_url = 'https://www.google.com/search?q=' + key
        search_results = requests.get(url)
        soup = BeautifulSoup(search_results.text)
        result_stats = soup.find(id='resultStats')
        m = re.match(REGEX, result_stats.text)
        # print m.group(1)
        return int(m.group(1).replace(',', ''))

    def probabilty_dist():
        # et all the stopwords in the english language
        stop_words = stopwords.words('english')
        user_input = self.corpus_value  # raw_input('Please enter:\n  1 if you want the Reuter corpus and \n  2 for Brown corpus:')
        if user_input == '0':
            universal_words = [w.lower() for w in reuters.words() if
                               w.lower().isalpha() and w.lower() not in stop_words]
        elif user_input == '1':
            universal_words = [w.lower() for w in brown.words() if w.lower().isalpha() and w.lower() not in stop_words]
            # for the univesral set of words the program is using Reuters Corpus
        # that contains 10,788 news documents totaling 1.3 million words
        # universal_words contain only thise words from reuters that are non- empty s is non-empty and all characters are alphabetic
        # the program also filters out all stop words. We have normalized the text to lowercase
        # universal_words = [w.lower() for w in reuters.words() if w.lower().isalpha() and w.lower() not in stop_words]

        # Porter stemmer is used for stemming the text.
        porter = nltk.PorterStemmer()
        #universal_stemmed_words is a list of words that has been stemmed
        universal_stemmed_words = [porter.stem(t) for t in universal_words]
        '''Calculate the probability of occurrence of the word passed as an argument by calculating the the frequency distribution
        #of the word and dividing it by the total number of words in the list'''
        fdist = nltk.FreqDist(universal_stemmed_words)
        #print "list of most common 20 words in the universal set:"
        #print fdist.most_common(20)
        user_word_input = raw_input('Please enter the word whose frequency you want to find in thhe universal set:')
        print "The frequency of word '%s' in the universal set is %d" % (
            user_word_input, fdist[porter.stem(user_word_input)])
        prob_word_univ_set = fdist[porter.stem(user_word_input)] / fdist.N()
        print "The overall probability of occurence of the word ' %s 'in the universal set is %f" % (
            user_word_input, prob_word_univ_set)

        # Calculate the probability of occurrence of the word passed as an argument for the test set
        # test set is a subset of universal set
        test_file = raw_input(
            "Please enter the test filename(full path) whose word frequency you would like to evaluate: ")
        f = open(test_file, 'rU')
        raw_test_data = f.read()
        test_words_list = nltk.word_tokenize(raw_test_data)
        # take a subset of universal set here an article of reuters whose categories are tea and barley
        # test_set_words contain only thise words from article that are non- empty and all characters are alphabetic
        # the program also filters out all stop words. We have normalized the text to lowercase
        test_set_words = [w.lower() for w in test_words_list if w.lower().isalpha() and w.lower() not in stop_words]

        #universal_stemmed_words is a list of words that has been stemmed
        test_stemmed_words = [porter.stem(t) for t in test_set_words]
        #Calculate the probability of occurrence of the word passed as an argument by calculating the the frequency distribution
        #of the word and dividing it by the total number of words in the list
        fdist_test = nltk.FreqDist(test_stemmed_words)
        print "list of most common 20 words in the test file:"
        print fdist_test.most_common(20)
        test_word_input = raw_input('Please enter the word whose frequency you want to find in the test file:')
        print "The frequency of word '%s' in the test file is %d" % (
            test_word_input, fdist_test[porter.stem(test_word_input)])
        prob_word_test_set = fdist_test[porter.stem(test_word_input)] / fdist_test.N()
        print ("The overall probability of occurence of the word '%s'in the test set is %f" % (
            test_word_input, prob_word_test_set))

        #bigram frequency


if __name__ == "__main__":
    root = Tk()
    returnValue = True
    while returnValue:
        lb = ListBoxChoice(root, "Word Frequency", "Select one Corpus").returnValue()

    mainloop()
    #probabilty_dist()
