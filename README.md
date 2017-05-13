# keyword_i2x

Built this package as a toy challenge. These were the challenge instructions:

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

RAKE algorithm + implementation

I modified an existing implementation for Python 3 and to include more flexibility with parameters. In this implementation, RAKE does the following:

(i) Generate key word candidates
(ii) Computes 'scores' for each candidate. Words are scored according to their frequency and the typical length of a candidate phrase in which they appear.

Originally implemented by: https://github.com/aneesha/RAKE
Forked from: https://github.com/BelalC/RAKE-tutorial/tree/master

A Python implementation of the Rapid Automatic Keyword Extraction (RAKE) algorithm as described in: 
Rose, S., Engel, D., Cramer, N., & Cowley, W. (2010). Automatic Keyword Extraction from Individual Documents. In M. W. Berry & J. Kogan (Eds.), Text Mining: Theory and Applications: John Wiley & Sons.

The source code is released under the MIT License.

---  ---  ---  ---  ---  ---

Word2Vec 

Utilising the gensim package to generate vector representations. Paragraph and Document representations were computed by simply taking the average of the word vectors present in a specified paragraph or document.
