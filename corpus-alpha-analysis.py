import nltk
from collections import Counter
import re
import string
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
#import seaborn as sns

#nltk.download('punkt')
from nltk.probability import FreqDist
from corpusConstants import filenameList
from corpusConstants import xml_stopWords
from corpusConstants import wikipedia_stopWords
from corpusConstants import CorpusLetter
from corpusConstants import DOC_SIZE
from corpusConstants import NUMBER_OF_WORDS
from corpusConstants import SHOW_CHARTS

from corpusUtility import get_pre_post_corpus
from corpusUtility import get_common_info
from corpusUtility import create_csv_file
from corpusUtility import plot_common_info
from corpusUtility import get_normalized_alpha_chars
from corpusUtility import clean_raw_data

from nltk.collocations import *
from nltk import bigrams
from nltk.corpus import stopwords
from nltk.util import ngrams

alphaChars = []
textTokens = []
word_tokens = []

# \w+ matches 1 or more word characters (same as [a-zA-Z0-9_]+).
tokenizer = nltk.RegexpTokenizer(r"\w+")

for i in range(DOC_SIZE):
    print("Analyzing file #", i)
    filename = nltk.data.find(filenameList[i])
    with open(filename, encoding='latin-1') as file:
        raw_data = file.read().lower()

    #Uncomment to look raw_data
    #print(raw_data[0:100])
    textTokens.extend(tokenizer.tokenize(clean_raw_data(raw_data)))
    #TextTokens 3227788 -> AFTER CLEANING UP 3107885

# In order to get only alpha tokens
word_tokens = [word for word in textTokens if word.isalpha() and word not in xml_stopWords
               and word not in wikipedia_stopWords and len(word) > 0]

alphaChars = get_normalized_alpha_chars(word_tokens)

mostCommonWords = get_common_info(word_tokens, 30)
mostCommonLetters = get_common_info(alphaChars, 1)

if len(mostCommonLetters) > 5:
    mostCommonLetters.pop()
    mostCommonLetters.pop()
    mostCommonLetters.pop()

pre_post_corpus_flag = True

if pre_post_corpus_flag:

    create_csv_file(get_pre_post_corpus(mostCommonLetters, word_tokens, True), True)
    corpusWords = get_pre_post_corpus(mostCommonWords, word_tokens)
    create_csv_file(corpusWords, word_tokens)

    corpusPhrases = []
    for corpusWord in corpusWords:
        corpus_phrase = ""
        if corpusWord.pre_tokens[0][1] > corpusWord.post_tokens[0][1]:
            corpus_phrase = corpusWord.pre_tokens[0][0] + " " + corpusWord.name
        else:
            corpus_phrase = corpusWord.name + " " + corpusWord.post_tokens[0][0]

        print(corpus_phrase)
        corpusPhrases.append(corpus_phrase)



# bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
finder = QuadgramCollocationFinder.from_words(word_tokens)
# #finder.nbest(bigram_measures.pmi, 10)
print("---------------------------")
print(finder.nbest(trigram_measures.pmi, 10))
print("---------------------------")
# bingrams = bigrams(word_tokens)

ngram = ngrams(word_tokens, 15)

l = reduce(lambda x, y: list(x)+list(y), zip(ngram))
flatten = [item for sublist in l for item in sublist]

flatten_counter = Counter(flatten)
ngram_counter = Counter(ngram)

#print(ngram_counter)
print(ngram_counter.most_common(10))
# create_csv_file(get_pre_post_corpus(corpusPhrases, words))

if SHOW_CHARTS:
    f_dist = FreqDist(alphaChars)
    f_dist.plot(NUMBER_OF_WORDS, cumulative=False, title="Frecuencia de letras")
    plot_common_info(mostCommonLetters, True)
    plot_common_info(mostCommonWords)

    df = pd.DataFrame.from_records(ngram_counter, columns=['Phrase', 'Count'])
    df['Phrase'] = df['Phrase'].apply(lambda x: ' '.join([w for w in x]))

    df = df.nlargest(columns="Count", n=10)
    plt.figure(figsize=(15, 4))
    # ax = sns.barplot(data=df, x="Phrase", y="Count")
    # ax.set(ylabel='Count')
    # plt.show()

print("Routine Finished")
