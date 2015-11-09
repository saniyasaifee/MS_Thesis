#!/usr/bin/env python

# Author: Saniya Saifee

import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from Word2VecUtility import Word2VecUtility
import pandas as pd
import numpy as np

if __name__ == '__main__':
    train = pd.read_csv(os.path.join(os.path.dirname(__file__)), 'data', 'labeledTrainData.tsv', header = 0,\
                        delimiter = "\t", quoting=3)
    test = pd.read_csv(os.path.join(os.path.dirname(__file__)), 'data', 'testData.tsv', header = 0,\
                        delimiter = "\t", quoting=3)
    print 'The first review is:'
    print train["review"][0]
    raw_input("Press Enter to continue..")
    # Initialize an empty list to hold clean_reviews
    clean_train_reviews = []
    # Loop over each review; create an index i that goes from 0 to the length of the movie review list
    print "Cleaning and parsing the training set movie reviews...\n"
    for i in xrange(0, len(train["review"])):
        clean_train_reviews.append("".join(Word2VecUtility.review_to_wordlist(train["review"][i], True)))

    # ****** Create a bag of words from the training set
    print "Creating the bag of words...\n"
    # Initialize CountVectorizer object which is Scikit-learn bag of words tool
    vectorizer = CountVectorizer(analyzer = "word", \
                            tokenizer = None, \
                            preprocessor = None, \
                            stop_words = None, \
                            max_features=5000)
    # fit_transform does two functions: First it fits the model and learns the vocabulary
    # second; it transforms our training data into feature vectors. The input should be a list of strings
    train_data_features = vectorizer.fit_transform(clean_train_reviews)
    # Convert to numpy array
    train_data_features = train_data_features.toarray()

    # train RandomForest using bag of words
    print "Training the random forest (this may take a while)..."
    # Initialize a RandomForestClassifier
    forest = RandomForestClassifier(n_estimators=100)
    # fit the forest to training set using the bag of words as features and sentiment labels as the response variables
    forest = forest.fit(train_data_features, train["sentiment"])
    # create an empty list and append the clean review one by one
    clean_test_reviews = []
    print "Cleaning and parsing the test set movie reviews...\n"
    for i in xrange(1, len(test["review"])):
        clean_test_reviews.append(Word2VecUtility.review_to_wordlist(test["review"][i], True))
    # Get a bag of words for the test set, and convert to a numpy array
    test_data_features = vectorizer.transform(clean_test_reviews)
    test_data_features = test_data_features.toarray()
    # Use the random forest to make sentiment label predictions
    print "Predicting test labels...\n"
    result = forest.predict(test_data_features)

    # Copy the results to a pandas dataframe with an "id" column and
    # a "sentiment" column
    output = pd.DataFrame( data={"id":test["id"], "sentiment":result} )

    # Use pandas to write the comma-separated output file
    output.to_csv(os.path.join(os.path.dirname(__file__), 'data', 'Bag_of_Words_model.csv'), index=False, quoting=3)
    print "Wrote results to Bag_of_Words_model.csv"




