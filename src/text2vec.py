#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


def make_feature_vec(words, model, num_features):
    """
    Function to average all of the word vectors in a given paragraph
    :param words:
    :param model:
    :param num_features:
    :return:
    """
    # Pre-initialize an empty numpy array (for speed)
    feature_vec = np.zeros((num_features,), dtype="float32")

    n_words = 0

    # Index2word is a list that contains the names of the words in
    # the model's vocabulary. Convert it to a set, for speed
    index2word_set = set(model.index2word)

    # Loop over each word in the review and, if it is in the model's
    # vocabulary, add its feature vector to the total
    for word in words:
        if word in index2word_set:
            n_words += 1
            feature_vec = np.add(feature_vec, model[word])

    # Divide the result by the number of words to get the average
    # feature_vec = np.divide(feature_vec, n_words)
    return feature_vec


def get_avg_feature_vecs(reviews, model, num_features):
    # Given a set of reviews (each one a list of words), calculate
    # the average feature vector for each one and return a 2D numpy array
    #
    # Initialize a counter
    counter = 0
    #
    # Pre-allocate a 2D numpy array, for speed
    review_feature_vecs = np.zeros((len(reviews), num_features), dtype="float32")
    #
    # Loop through the reviews
    for review in reviews:
        # Print a status message
        # if counter % 1000 == 0:
        # print("Document %d of %d" % (counter, len(reviews)))

        # Call the function (defined above) that makes average feature vectors
        review_feature_vecs[counter] = make_feature_vec(review, model, num_features)
        # Increment the counter
        counter += 1
    return review_feature_vecs
