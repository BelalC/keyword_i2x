#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'b_chaudhary'

import rake
from text2vec import make_feature_vec, get_avg_feature_vecs

import gensim
import operator
import io
from os import path
from glob import glob

import argparse

ap = argparse.ArgumentParser()

ap.add_argument("-s", "--stopword", type=str, default="stop_words/sklearn_stopwords.txt",
                help="path to a list of stop words in text format")
ap.add_argument("-c", "--char", type=int, default=5,
                help="minimum number of characters in key word")
ap.add_argument("-w", "--word_len", type=int, default=3,
                help="maximum number of words in key word")
ap.add_argument("-f", "--word_freq", type=int, default=4,
                help="minimum threshold number of occurrences for key word")
# ap.add_argument("-t", "--test", type=str, default="...",
#                help="path to directory containing test text files used to evaluate relevance of extracted key words")
required_ap = ap.add_argument_group('required arguments')
required_ap.add_argument("-i", "--input",
                         type=str, default=None, required=True,
                         help="path to single text file to extract keywords from")
# required_ap.add_argument("-m", "--model",
#                         type=str, default="resnet", required=True,
#                         help="name of pre-trained network to use")
args = vars(ap.parse_args())


# ====== KEYWORD EXTRACTION ======
# ================================

# Initialize RAKE object,
rake_object = rake.Rake(stoppath=args["stopword"], min_char_length=args["char"],
                        max_words_length=args["word_len"], min_keyword_frequency=args["word_freq"])

# 2. run on RAKE on a given text
sample_file = io.open(args["input"], 'r', encoding="iso-8859-1")
text = sample_file.read()

keywords = rake_object.run(text)

# 3. print results
print("Keywords:", keywords)

print("----------")

# ====== KEYWORD RANKING =========
# ================================

print("loading Word2Vec model...")
model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz',
                                                        binary=True)
print("loaded Word2Vec model.")

test_dirs = [path.join(args["test"], test_doc) for test_doc in glob(path.join(args["test"], "*txt"))]
test_docs = [doc.read() for doc in test_dirs]
test_vecs = [get_avg_feature_vecs([test_doc],
                                  model=model,
                                  num_features=model.vector_size)
             for test_doc in test_docs]


# ====== SAVE OUTPUT =============
# ================================


# EXAMPLE TWO - BEHIND THE SCENES (from https://github.com/aneesha/RAKE/rake.py)

# 1. initialize RAKE by providing a path to a stopwords file
rake_object = rake.Rake(stoppath)

text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility " \
       "of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. " \
       "Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating"\
       " sets of solutions for all types of systems are given. These criteria and the corresponding algorithms " \
       "for constructing a minimal supporting set of solutions can be used in solving all the considered types of " \
       "systems and systems of mixed types."


# 1. Split text into sentences
sentenceList = rake.split_sentences(text)

for sentence in sentenceList:
    print("Sentence:", sentence)

# generate candidate keywords
stopwordpattern = rake.build_stop_word_regex(stoppath)
phraseList = rake.generate_candidate_keywords(sentenceList, stopwordpattern)
print("Phrases:", phraseList)

# calculate individual word scores
wordscores = rake.calculate_word_scores(phraseList)

# generate candidate keyword scores
keywordcandidates = rake.generate_candidate_keyword_scores(phraseList, wordscores)
for candidate in keywordcandidates.keys():
    print("Candidate: ", candidate, ", score: ", keywordcandidates.get(candidate))

# sort candidates by score to determine top-scoring keywords
sortedKeywords = sorted(six.iteritems(keywordcandidates), key=operator.itemgetter(1), reverse=True)
totalKeywords = len(sortedKeywords)

# for example, you could just take the top third as the final keywords
for keyword in sortedKeywords[0:int(totalKeywords / 3)]:
    print("Keyword: ", keyword[0], ", score: ", keyword[1])

print(rake_object.run(text))
