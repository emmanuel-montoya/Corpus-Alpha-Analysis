import logging

import nltk
from nltk.probability import FreqDist
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

from corpusConstants import filename_list
from corpusConstants import ROOT_DIR
from corpusConstants import DOC_SIZE
from corpusConstants import NUMBER_OF_WORDS
from corpusConstants import PRE_POST_CORPUS_FLAG
from corpusConstants import SHOW_CHARTS
from corpusConstants import LETTERS_FREQUENCY

from corpusUtility import build_corpus_words, build_n_words_corpus_phrases
from corpusUtility import build_corpus_letters
from corpusUtility import count_letter_occurrences
from corpusUtility import count_word_occurrences
from corpusUtility import create_corpus_letter_csv
from corpusUtility import create_corpus_word_csv
from corpusUtility import create_corpus_phrase_csv
from corpusUtility import plot_common_info
from corpusUtility import plot_corpus_words
from corpusUtility import normalize_alpha_chars
from corpusUtility import clean_raw_data

text_tokens = []
tokenizer = nltk.RegexpTokenizer(r"\w+")
logging.basicConfig(filename='app.log', format='%(levelname)s:%(asctime)s - %(message)s', level=logging.INFO)

for i in range(DOC_SIZE):
    logging.info('Analyzing file #%d: %s', i, filename_list[i])
    filename = nltk.data.find(ROOT_DIR + filename_list[i])
    with open(filename, 'r', encoding='latin-1') as file:
        raw_data = file.read().lower()

    data_tokenized = tokenizer.tokenize(clean_raw_data(raw_data))
    logging.info('Data after tokenization %d', len(data_tokenized))
    logging.debug(data_tokenized[0:500])

    text_tokens.extend(data_tokenized)
    logging.info('Text Tokens Total: %d', len(text_tokens))

alpha_chars = normalize_alpha_chars(text_tokens)
letters_counter = count_letter_occurrences(alpha_chars)
words_counter = count_word_occurrences(text_tokens, NUMBER_OF_WORDS)

corpus_words = []
if PRE_POST_CORPUS_FLAG:
    logging.info("pre_post_corpus")
    corpus_letters = build_corpus_letters(letters_counter, text_tokens)
    create_corpus_letter_csv(corpus_letters)

    corpus_words = build_corpus_words(words_counter, text_tokens)
    create_corpus_word_csv(corpus_words)

    corpus_n_words_phrases = build_n_words_corpus_phrases(corpus_words, text_tokens, 20)
    create_corpus_phrase_csv(corpus_n_words_phrases)

if SHOW_CHARTS:
    f_dist = FreqDist(alpha_chars)
    f_dist.plot(title=LETTERS_FREQUENCY)
    plot_common_info(letters_counter, True)
    plot_common_info(words_counter[0:30])
    plot_corpus_words(corpus_words[0:30])

logging.info("Routine Finished")
