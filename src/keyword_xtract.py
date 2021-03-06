#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gensim
import argparse
import numpy as np
import wget
from os import path
from glob import glob
from itertools import compress
from sklearn.metrics import pairwise

from rake_base import Rake
from text2vec import make_feature_vec, get_avg_feature_vecs


def percentage(x):
    x = int(x)
    if x <= 0:
        raise argparse.ArgumentTypeError("Please enter a value between 1 and 100")
    elif x > 100:
        raise argparse.ArgumentTypeError("Please enter a value between 1 and 100")
    return x


ap = argparse.ArgumentParser()

ap.add_argument("-s", "--stopword", type=str, default="data/stop_words/sklearn_stopwords.txt",
                help="path to a list of stop words in text format")
ap.add_argument("-c", "--char", type=int, default=4,
                help="minimum number of characters in key word")
ap.add_argument("-w", "--word_len", type=int, default=5,
                help="maximum number of words in key word")
ap.add_argument("-f", "--word_freq", type=int, default=3,
                help="minimum threshold number of occurrences for key word")
ap.add_argument("-m", "--model", type=str, default="w2v_models/google_trunc_w2v.gz",
                help="choice of model or path to user-defined Word2Vec model, default model is a truncated "
                     "version of model trained on Google News dataset")
ap.add_argument("-t", "--test", type=str, default="data/evaluation/",
                help="path to directory containing test text files used to evaluate relevance of extracted key words")
ap.add_argument("-o", "--output", type=str, default="results/results.txt",
                help="path to output directory for keyword extraction results")
ap.add_argument("-n", "--n_keyword", type=percentage, default=50,
                help="top n%% of extracted keywords to rank; enter an integer between 1 and 100")
ap.add_argument("-p", "--print_output", type=bool, default=None,
                help="whether to print final ranked keywords")
required_ap = ap.add_argument_group('required arguments')
required_ap.add_argument("-i", "--input",
                         type=str, default="data/demo/script.txt",
                         help="path to a single document to extract keywords from")
args = vars(ap.parse_args())


# ====== DOWNLOADING Word2Vec MODELS ======
# =========================================

# Map model names to download links
MODELS = {
    # "google": "https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit",
    "glove_6B": "http://nlp.stanford.edu/data/glove.6B.300d.zip",
    "glove_42B": "http://nlp.stanford.edu/data/glove.42B.300d.zip",
    "glove_840B": "http://nlp.stanford.edu/data/glove.840B.300d.zip",
    "glove_twitter": "http://nlp.stanford.edu/data/glove.twitter.27B.zip"
}
if args["model"] is not "w2v_models/google_trunc_w2v.gz":
    if args["model"] not in MODELS:
        if not path.exists(args["model"]):
            raise AssertionError("The --model command line argument should be a key in the `MODELS` dictionary, "
                                 "or else should be a path to a custom Word2Vec model")


# Download word embeddings for Word2Vec model, if not already present
model_dir = "w2v_models/" + args["model"] + ".bin"
if args["model"] in MODELS:
    if not path.exists(model_dir):
        print("downloading ", args["model"], " Word2Vec model")
        print("this may take a while, file may be up to 2GB in size")
        url = MODELS[args["model"]]
        file = wget.download(url=url, out=model_dir)
        print("downloaded model!")

# load Word2Vec model
if args["model"] in MODELS:
    if path.exists(model_dir):
        print("loading ", args["model"], " Word2Vec model")
        print("this may take a few minutes...")
        model = gensim.models.KeyedVectors.load_word2vec_format(model_dir, binary=True)
        print("loaded model!")
else:
    print("loading Word2Vec model")
    print("this may take a few minutes...")
    model = gensim.models.KeyedVectors.load_word2vec_format(args["model"], binary=True)
    print("loaded model!")

# ====== KEYWORD EXTRACTION ======
# ================================

print("extracting keywords")
# Initialize RAKE object,
rake_object = Rake(stop_words_path=args["stopword"], min_char_length=args["char"],
                   max_words_length=args["word_len"], min_keyword_frequency=args["word_freq"])

# 2. run on RAKE on a given text
sample_file = open(args["input"], 'r')
text = sample_file.read()

keywords = rake_object.run(text)
print("%d keywords extracted" % (len(keywords)))

# 3. print results
# print("Keywords:", keywords)

# =========== Word2Vec - KEYWORDS ===========
# ===========================================

# filter previously generated keywords to include only those present in the Word2Vec model's vocabulary
# this is done automatically for the test documents
index2word_set = set(model.index2word)
bool_split = [word[0] in index2word_set for word in keywords]
keyword_in_model = list(compress(keywords, bool_split))

# sort keywords + choose top n to examine
sorted_keyword = sorted(keyword_in_model, key=lambda x: x[1], reverse=True)
n_keywords = int(args["n_keyword"]*len(sorted_keyword)//100)
keyword_list = sorted_keyword[0:n_keywords]
print("using top %d keywords " % n_keywords)

# compute vector representations of extracted keywords
keyword_vecs = [(model.word_vec(word[0])) for word in keyword_list]

# (optional) generating candidate words from test docs
# test_words = generate_candidate_keywords(split_sentences(test_docs[0]), stopword_pattern=stopword,
#                                         min_char_length=2, max_words_length=2)


# ========== Word2Vec - TEST DOCS ===========
# ===========================================

# extract average Word2Vec representation for test documents, to be utilised for evaluating keywords
test_dirs = glob(path.join(args["test"], "*txt"))
test_docs = [doc.read() for doc in [open(test_file, "r") for test_file in test_dirs]]
print("extracting vector representation of test docs; %d docs in total" % (len(test_docs)))
test_vecs = [get_avg_feature_vecs([doc],
                                  model=model,
                                  num_features=model.vector_size)
             for doc in test_docs]


# ======= KEYWORD RANKING ========
# ================================

similar_keywords = []

# compute cosine similarity between keywords and test docs
for vec in test_vecs:
    similar_keywords.append([pairwise.cosine_similarity(X=key_word.reshape(1, -1),
                                                        Y=vec.reshape(1, -1))
                             for key_word in keyword_vecs])

# averaging cosine similarities to get a single 'rank' for each keyword
sum_keyword = np.zeros_like(similar_keywords[0])
for doc in similar_keywords:
    sum_keyword = sum_keyword + doc
keyword_similarities = sum_keyword/3

# list of keywords
names_key = [k[0] for k in keyword_list]

# include names with keyword rankings and unstack array of arrays
final_keywords = []
for i in range(len(names_key)):
    final_keywords.append((names_key[i], keyword_similarities[i][0][0]))

ranked = sorted(keyword_list, key=lambda x: x[1], reverse=True)


# ========= SAVE OUTPUT ==========
# ================================

print("saving results")

with open(args["output"], "w") as outdir:
    for line in ranked:
        strs = "    score: ".join(str(x) for x in line)
        outdir.write(strs + "\n")

if args["print_output"]:
    for line in ranked:
        strs = "    score: ".join(str(x) for x in line)
        print(strs)

"""
# ================================
# Tutorial looking at RAKE
# ================================

# 1. initialize RAKE by providing a path to a stopwords file
rake_object = rake.Rake(stoppath)

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

"""
