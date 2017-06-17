# keyword_i2x

Built this package as a toy challenge to do the following:

1 - Compute the most important key-words (a key-word can be between 1-3 words)
2 - Choose the top n words from the previously generated list. Compare these key- words with all the words occurring in all of the transcripts.
3 - Generate a score (rank) for these top n words based on analysed transcripts.

What this package does:

1 - Generates the keywords (from 1-3 words in length) from a document based, based on the RAKE algorithm

2 - Generate vector representations of all key words and words in a test corpus, using Word2Vec.

    Note: For comparison, we compute paragraph and/or document vector representations from the test corpus. 
    We want to find a way to measure the 'similarity' of each keyword to each test document; as opposed to doing a keyword-to-word comparison,
    it makes more sense to do a keyword-to-paragraph or keyword-to-document comparison! Details of the paragraph or document to vector conversion will be explained below.

3 - Ranks key words by comparing key word vectors with paragraph/document vectors from test corpus - DETAILS COMING SOON.
    
    
---  ---  ---  ---  ---  ---
## Installing dependencies

The code was developed with python 3.5 and requires the following libraries/versions:

gensim==2.0.0
numpy==1.12.1
scikit-learn==0.18.1
wget==3.2

These dependencies are specified in requirements.txt, and can be downloaded via the following command:

```bash
pip install -r requirements.txt
```
---  ---  ---  ---  ---  ---

## Usage

Running the keyword_xtract file, will carry out the steps described above (keyword extraction -> compute vector representations -> rank key words)

```bash
$python src/keyword_xtract.py --help

usage: keyword_xtract.py [-h] [-s STOPWORD] [-c CHAR] [-w WORD_LEN]
                         [-f WORD_FREQ] [-m MODEL] [-t TEST] [-o OUTPUT]
                         [-n N_KEYWORD] [-p SHOW_OUTPUT] [-i INPUT]

optional arguments:
  -h, --help            show this help message and exit
  -s STOPWORD, --stopword STOPWORD
                        path to a list of stop words in text format
  -c CHAR, --char CHAR  minimum number of characters in key word
  -w WORD_LEN, --word_len WORD_LEN
                        maximum number of words in key word
  -f WORD_FREQ, --word_freq WORD_FREQ
                        minimum threshold number of occurrences for key word
  -m MODEL, --model MODEL
                        choice of model or path to user-defined Word2Vec
                        model, default model is a truncated version of model
                        trained on Google News dataset
  -t TEST, --test TEST  path to directory containing test text files used to
                        evaluate relevance of extracted key words
  -o OUTPUT, --output OUTPUT
                        path to output directory for keyword extraction
                        results
  -n N_KEYWORD, --n_keyword N_KEYWORD
                        top n% of extracted keywords to rank; enter an integer
                        between 1 and 100
  -p SHOW_OUTPUT, --show_output SHOW_OUTPUT
                        whether to print final ranked keywords

required arguments:
  -i INPUT, --input INPUT
                        path to a single document to extract keywords from
```

Models available:

A truncated version of Google's pre-trained Word2Vec model is available as default. GloVe Word2Vec models (https://nlp.stanford.edu/projects/glove/) can also be downloaded by specifying the model required at run time:

glove_6B - Wikipedia 2014 + Gigaword 5 (6B tokens, 400K vocab, uncased, 50d, 100d, 200d, & 300d vectors, 822 MB download)
glove_42B - Common Crawl (42B tokens, 1.9M vocab, uncased, 300d vectors, 1.75 GB download): glove.42B.300d.zip
glove_840B - Common Crawl (840B tokens, 2.2M vocab, cased, 300d vectors, 2.03 GB download): glove.840B.300d.zip
glove_twitter - Twitter (2B tweets, 27B tokens, 1.2M vocab, uncased, 25d, 50d, 100d, & 200d vectors, 1.42 GB download)

Use the labels above as inputs for the '-m/--model' command line arguments. If the selected model is not present, the model will be downloaded; this may take some time. It is also possible to use custom user-defined Word2Vec models by supplying a path to the model.

NOTE - the default evaluation docs provided for ranking keywords are 3 document pages related to food, which were extracted from Wikipedia. Please provide your own relevant evaluation documents for accurate keyword ranking. Otherwise, keywords can simply be extracted and the ranking scores ignored.

---  ---  ---  ---  ---  ---

## RAKE algorithm + implementation

I modified an existing RAKE implementation to work with Python 3 and different parameters. In this implementation, RAKE does the following:

(i) Generate key word candidates
(ii) Computes 'scores' for each candidate. Words are scored according to their frequency and the typical length of a candidate phrase in which they appear.

Originally implemented by: https://github.com/aneesha/RAKE
Forked from: https://github.com/BelalC/RAKE-tutorial/tree/master

A Python implementation of the Rapid Automatic Keyword Extraction (RAKE) algorithm as described in: 
Rose, S., Engel, D., Cramer, N., & Cowley, W. (2010). Automatic Keyword Extraction from Individual Documents. In M. W. Berry & J. Kogan (Eds.), Text Mining: Theory and Applications: John Wiley & Sons.

The source code is released under the MIT License.

---  ---  ---  ---  ---  ---

## Word2Vec + Ranking

Utilising gensim and pre-trained Word2Vec models, keyword vector representations are computed. Vector representations of evaluation documents are computed by taking the average of the word vectors present in a specified document. The pairwise cosine similarity between each keyword vector and evaluation document vector are computed and averaged, giving a single score which can be utilised as a 'rank' for the keyword.

	
Gensim - https://radimrehurek.com/gensim/index.html
Vector represenations of words and phrases - Distributed Representations of Words and Phrases and their Compositionality; Mikolov, Tomas; Sutskever, Ilya; Chen, Kai; Corrado, Greg; Dean, Jeffrey, arXiv:1310.4546

