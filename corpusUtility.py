import collections
import copy
import unidecode
import squarify
import re
import logging
import random

from datetime import datetime
from nltk.corpus import stopwords

from corpusConstants import CorpusLetter
from corpusConstants import CorpusWord
from corpusConstants import CorpusPhrase
from corpusConstants import unusual_letters
from corpusConstants import wikipedia_stopPhrases
from corpusConstants import wikipedia_stopWords

from corpusConstants import PRE_TOKEN
from corpusConstants import PRE_COUNT
from corpusConstants import POST_TOKEN
from corpusConstants import POST_COUNT
from corpusConstants import LETTER
from corpusConstants import WORD
from corpusConstants import MAIN_WORD
from corpusConstants import PHRASE
from corpusConstants import COUNT
from corpusConstants import PHRASE_TOLERANCE
from corpusConstants import WORDS_BY_PHRASE
from corpusConstants import CUMULATIVE_FREQUENCY
import csv
from corpusConstants import CSV_ALPHA_ANALYSIS_FILE
from corpusConstants import CSV_WORD_ANALYSIS_FILE
from corpusConstants import CSV_PHRASE_ANALYSIS_FILE
from corpusConstants import CSV_RANDOM_PHRASES

import matplotlib.pyplot as plt
from corpusConstants import LETTERS_FREQUENCY_ORDER
from corpusConstants import WORDS_FREQUENCY_ORDER


def clean_raw_data(raw_data):
    logging.info('Entering clean_raw_data')
    logging.debug('raw_data length before cleaning process %d', len(raw_data))
    logging.debug(raw_data[0:500])

    raw_data = re.sub('<.*>', '', raw_data)
    logging.debug('raw_data length after removing XML markup: %d', len(raw_data))
    logging.debug(raw_data[0:500])
    raw_data = re.sub('^\n', '', raw_data, flags=re.MULTILINE)
    logging.debug("raw_data length after removing '\\n' characters found at string start: %d", len(raw_data))
    logging.debug(raw_data[0:500])

    raw_data = re.sub('\n\n+', '\n', raw_data)
    logging.debug("raw_data length after removing consecutive '\\n' characters: %d", len(raw_data))
    logging.debug(raw_data[0:500])

    raw_data = re.sub(';+\n', '\n', raw_data)
    logging.debug("raw_data length after removing semicolons preceding'\\n' characters: %d", len(raw_data))
    logging.debug(raw_data[0:500])

    raw_data = re.sub('^\s*\w+\s*\n', '', raw_data, flags=re.MULTILINE)
    logging.debug("raw_data length after removing stand-alone words: %d", len(raw_data))
    logging.debug(raw_data[0:500])

    raw_data = re.sub('^\s*\w+\s\.*\n', '', raw_data, flags=re.MULTILINE)
    logging.debug("raw_data length after removing stand-alone 2 words: %d", len(raw_data))
    logging.debug(raw_data[0:500])

    raw_data = re.sub('\((\s*|\+*|\w\.\s*)\d+(-*|\s*|,\s*)\d*-*\)', '', raw_data)
    logging.debug("raw_data length after removing numbers and dates in parenthesis: %d", len(raw_data))

    raw_data = re.sub('\(\s*\)', '', raw_data)
    logging.debug("raw_data length after removing empty parenthesis: %d", len(raw_data))

    raw_data = re.sub('\s*-\s', ' ', raw_data)
    logging.debug("raw_data length after removing dashes: %d", len(raw_data))

    raw_data = re.sub('\s+\.', ' ', raw_data)
    logging.debug("raw_data length after removing dots presided by whitespace: %d", len(raw_data))
    logging.debug(raw_data[0:500])

    for wikipedia_stopPhrase in wikipedia_stopPhrases:
        raw_data = raw_data.replace(wikipedia_stopPhrase, '')
        logging.debug('raw_data length after removing %s recurrent phrase: %d', wikipedia_stopPhrase, len(raw_data))

    for wikipedia_stopWord in wikipedia_stopWords:
        raw_data = raw_data.replace(wikipedia_stopWord, '')
        logging.debug('raw_data length after removing %s recurrent phrase: %d', wikipedia_stopWord, len(raw_data))

    punctuation_no_period = '[!"#$%&\'()*+,-/:;?@[\]^_`{|}~]'
    raw_data = re.sub(punctuation_no_period, '', raw_data)
    logging.debug("raw_data length after removing punctuation but period: %d", len(raw_data))

    logging.info("raw_data length after cleaning process: %d", len(raw_data))
    logging.debug(raw_data[0:500])
    return raw_data


def normalize_alpha_chars(words):
    logging.info('Normalizing alpha characters to remove accents using unidecode.')
    alpha_chars = []
    for word in words:
        alpha_chars.extend([unidecode.unidecode(char) for char in word
                            if (unidecode.unidecode(char) not in unusual_letters and char.isalpha())])
    return alpha_chars


def count_letter_occurrences(chars, size=0):
    logging.debug("Entering count_letter_occurrences method")
    logging.debug("Removing special characters combined as 'th', 'ss', 'ae'")
    no_special_chars = (x for x in chars if len(x) == 1 and x.isalpha())
    chars_counter = collections.Counter(no_special_chars)

    logging.debug(chars_counter.most_common(size) if size > 0 else chars_counter.most_common())
    return chars_counter.most_common(size) if size > 0 else chars_counter.most_common()


def count_word_occurrences(word_tokens, size=0):
    logging.debug("Entering count_word_occurrences method.")

    words = [word for word in word_tokens if word.isalpha()]
    words_counter = collections.Counter(words)
    logging.debug(words_counter.most_common(size) if size > 0 else words_counter.most_common())

    return words_counter.most_common(size) if size > 0 else words_counter.most_common()


def plot_common_info(most_common_tokens, is_letter=False):
    logging.info("Entering plot_common_info")
    label_letters = []
    size_letters = []
    for a in range(len(most_common_tokens)):
        label_letters.append(most_common_tokens[a][0])
        size_letters.append(most_common_tokens[a][1])

    squarify.plot(sizes=size_letters, label=label_letters, alpha=.8)
    plt.axis('off')
    plt.title(LETTERS_FREQUENCY_ORDER) if is_letter else plt.title(WORDS_FREQUENCY_ORDER)
    plt.show()


def plot_corpus_words(corpus_words):
    logging.info("Entering plot_common_info")
    label_letters = []
    size_letters = []
    for corpus_word in corpus_words:
        label_letters.append(corpus_word.name)
        size_letters.append(corpus_word.count)

    squarify.plot(sizes=size_letters, label=label_letters, alpha=.8)
    plt.axis('off')
    plt.title(WORDS_FREQUENCY_ORDER)
    plt.show()


def build_corpus_letters(common_letter_tokens, text_tokens):
    logging.info("Entering get_pre_post_letter_corpus method")
    corpus_letters = []

    for token in common_letter_tokens:
        token_text = token[0]
        token_count = token[1]
        pre_tokens = []
        post_tokens = []

        logging.debug("Pre|Post Tokens for letter: %s", token_text)
        word_indexes = [i for i, w in enumerate(text_tokens) if w.find(token_text) != -1]

        for word_index in word_indexes:
            word = text_tokens[word_index]
            letter_index = word.index(token_text)

            if letter_index > 0:
                pre_tokens.append(word[letter_index - 1])

            if letter_index < (len(word) - 1):
                post_tokens.append(word[letter_index + 1])

        pre_letters_counter = count_letter_occurrences(pre_tokens)
        post_letters_counter = count_letter_occurrences(post_tokens)

        corpus_letters.append(CorpusLetter(token_text, token_count, pre_letters_counter, post_letters_counter))
        logging.info("Letter: %s - %d | Most_common_pre_letter: %s - %d | Most_common_post_letter %s - %d",
                     token_text, token_count, pre_letters_counter[0][0], pre_letters_counter[0][1],
                     post_letters_counter[0][0], post_letters_counter[0][1])

    return corpus_letters


def build_corpus_words(common_word_tokens, text_tokens):
    logging.info("Entering get_pre_post_word_corpus method")
    corpus_words = []

    for token in common_word_tokens:
        token_text = token[0]
        token_count = token[1]
        pre_token = []
        post_token = []

        if len(token_text) == 1 or (token_text in stopwords.words('spanish')
                                    or token_text in stopwords.words('english')):
            continue

        logging.debug("Pre|Post Tokens for word: %s ", token_text)
        word_indexes = [i for i, w in enumerate(text_tokens) if w.find(token_text) != -1]

        for word_index in word_indexes:
            if word_index > 0:
                pre_token.append(text_tokens[word_index - 1])

            if word_index < (len(text_tokens) - 1):
                post_token.append(text_tokens[word_index + 1])

        pre_words_counter = count_word_occurrences(pre_token)
        post_words_counter = count_word_occurrences(post_token)

        corpus_words.append(CorpusWord(token_text, token_count, pre_words_counter, post_words_counter))
        logging.info("Word: %s - %d | Most_common_pre_word: %s - %d | Most_common_post_word %s - %d",
                     token_text, token_count, pre_words_counter[0][0], pre_words_counter[0][1],
                     post_words_counter[0][0], post_words_counter[0][1])
        if len(corpus_words) == -1:
            break

    return corpus_words


def build_n_words_corpus_phrases(corpus_words, word_corpus, n_words=1):
    logging.info("Entering get_pre_post_n_word_corpus method")
    corpus_phrases = []
    corpus_n_words_phrases = []

    for corpus_word in corpus_words:
        corpus_phrase_tokens = []
        main_word = corpus_word.name

        if corpus_word.pre_tokens[0][1] > corpus_word.post_tokens[0][1]:
            corpus_phrase = corpus_word.pre_tokens[0][0] + " " + main_word
            corpus_phrase_tokens.append(corpus_word.pre_tokens[0][0])
            corpus_phrase_tokens.append(main_word)
            phrase_count = corpus_word.pre_tokens[0][1]
        else:
            corpus_phrase = main_word + " " + corpus_word.post_tokens[0][0]
            corpus_phrase_tokens.append(main_word)
            corpus_phrase_tokens.append(corpus_word.post_tokens[0][0])
            phrase_count = corpus_word.post_tokens[0][1]

        logging.info("Main phrase: %s found %d times", corpus_phrase, phrase_count)
        corpus_phrases.append(CorpusPhrase(main_word, corpus_phrase, corpus_phrase_tokens, phrase_count))

    for n_word in (n+1 for n in range(n_words)):
        for phrase_index, corpus_phrase in enumerate(corpus_phrases):
            logging.info("Pre|Post Tokens for phrase: %s", corpus_phrase.phrase)

            if not corpus_phrase.phrase_words:
                logging.info("This phrase is empty.")
                continue

            if corpus_phrase.count == 1:
                logging.info("This phrase has already reached its limit and its unique through the whole Corpus.")
                continue

            if phrase_index > (len(corpus_n_words_phrases)-1) or not corpus_n_words_phrases:
                corpus_n_words_phrases.append([])

            if not corpus_n_words_phrases[phrase_index]:
                corpus_n_words_phrases[phrase_index].append(copy.deepcopy(corpus_phrase))
            elif (corpus_phrase.count*100/corpus_n_words_phrases[phrase_index][-2].count) <= PHRASE_TOLERANCE:
                logging.info("This phrase count is equal or below the percentage of tolerance"
                             " to be an acceptable new phrase.")
                continue

            token_text = corpus_phrase.phrase_words[0]
            pre_token = []
            post_token = []
            word_indexes = [i for i, w in enumerate(word_corpus) if w.find(token_text) != -1]

            for word_index in word_indexes:
                post_index = 0
                for word in corpus_phrase.phrase_words:
                    if post_index == 0:
                        logging.debug("First Word: %s - Index: %d", word, word_index)

                    if word_corpus[word_index+post_index] == word:
                        if post_index == 1 and n_word == 1:
                            pre_token.append(word_corpus[word_index - post_index])

                        post_index += 1

                        if post_index == len(corpus_phrase.phrase_words):
                            post_token.append(word_corpus[word_index + post_index])
                            if n_word > 1:
                                pre_token.append(word_corpus[word_index - 1])
                        else:
                            logging.debug("Next Word - Expected: %s Real: %s",
                                          corpus_phrase.phrase_words[post_index], word_corpus[word_index + post_index])
                    else:
                        continue

            pre_words_counter = count_word_occurrences(pre_token)
            post_words_counter = count_word_occurrences(post_token)
            corpus_phrase_tokens = []
            phrase = ""
            new_phrase_count = 0
            if pre_words_counter and post_words_counter:
                if pre_words_counter[0][1] > post_words_counter[0][1]:
                    phrase = pre_words_counter[0][0] + " " + corpus_phrase.phrase
                    corpus_phrase_tokens.append(pre_words_counter[0][0])
                    corpus_phrase_tokens.extend(corpus_phrase.phrase_words)
                    new_phrase_count = pre_words_counter[0][1]
                else:
                    phrase = corpus_phrase.phrase + " " + post_words_counter[0][0]
                    corpus_phrase_tokens.extend(corpus_phrase.phrase_words)
                    corpus_phrase_tokens.append(post_words_counter[0][0])
                    new_phrase_count = post_words_counter[0][1]
            elif pre_words_counter:
                phrase = pre_words_counter[0][0] + " " + corpus_phrase.phrase
                corpus_phrase_tokens.append(pre_words_counter[0][0])
                corpus_phrase_tokens.extend(corpus_phrase.phrase_words)
                new_phrase_count = pre_words_counter[0][1]
            elif post_words_counter:
                phrase = corpus_phrase.phrase + " " + post_words_counter[0][0]
                corpus_phrase_tokens.extend(corpus_phrase.phrase_words)
                corpus_phrase_tokens.append(post_words_counter[0][0])
                new_phrase_count = post_words_counter[0][1]

            logging.info('New most common phrase found %d times: "%s" adding %d word(s) to original',
                         new_phrase_count, phrase, n_word)

            corpus_n_words_phrases[phrase_index].append(CorpusPhrase(corpus_phrases[phrase_index].main_word, phrase,
                                                                     corpus_phrase_tokens, new_phrase_count,
                                                                     pre_words_counter, post_words_counter))

            logging.debug("Updating value of corpus_phrase in specific index for next iteration")
            corpus_phrases[phrase_index].phrase = phrase
            corpus_phrases[phrase_index].phrase_words = corpus_phrase_tokens
            corpus_phrases[phrase_index].pre_tokens = pre_words_counter
            corpus_phrases[phrase_index].post_tokens = post_words_counter
            corpus_phrases[phrase_index].count = new_phrase_count

    return corpus_n_words_phrases


def create_corpus_letter_csv(pre_post_corpus, common_limit=2):
    logging.info("Entering create_corpus_letter_csv method")
    field_names = []
    csv_rows = []

    for corpusLetter in pre_post_corpus:
        if len(csv_rows) == 0:
            field_names.append(LETTER)
            field_names.append(COUNT)

        csv_row = [corpusLetter.name, corpusLetter.count]

        for i in range(common_limit):
            if len(csv_rows) == 0:
                field_names.append(PRE_TOKEN + str(i))
                field_names.append(PRE_COUNT + str(i))
                field_names.append(POST_TOKEN + str(i))
                field_names.append(POST_COUNT + str(i))

            if i < len(corpusLetter.pre_tokens):
                csv_row.append(corpusLetter.pre_tokens[i][0])
            if i < len(corpusLetter.pre_tokens):
                csv_row.append(corpusLetter.pre_tokens[i][1])
            if i < len(corpusLetter.post_tokens):
                csv_row.append(corpusLetter.post_tokens[i][0])
            if i < len(corpusLetter.post_tokens):
                csv_row.append(corpusLetter.post_tokens[i][1])

        csv_rows.append(csv_row)

    with open(CSV_ALPHA_ANALYSIS_FILE, 'w') as csv_file:
        wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL, lineterminator='\n')
        wr.writerow(field_names)
        for row in csv_rows:
            wr.writerow(row)


def create_corpus_word_csv(pre_post_corpus, common_limit=2):
    logging.info("Entering create_corpus_word_csv method")
    field_names = []
    csv_rows = []

    for corpus_word in pre_post_corpus:
        if len(csv_rows) == 0:
            field_names.append(WORD)
            field_names.append(COUNT)

        csv_row = [corpus_word.name, corpus_word.count]

        for i in range(common_limit):
            if len(csv_rows) == 0:
                field_names.append(PRE_TOKEN + str(i))
                field_names.append(PRE_COUNT + str(i))
                field_names.append(POST_TOKEN + str(i))
                field_names.append(POST_COUNT + str(i))

            if i < len(corpus_word.pre_tokens):
                csv_row.append(corpus_word.pre_tokens[i][0])
            if i < len(corpus_word.pre_tokens):
                csv_row.append(corpus_word.pre_tokens[i][1])
            if i < len(corpus_word.post_tokens):
                csv_row.append(corpus_word.post_tokens[i][0])
            if i < len(corpus_word.post_tokens):
                csv_row.append(corpus_word.post_tokens[i][1])

        csv_rows.append(csv_row)

    with open(CSV_WORD_ANALYSIS_FILE, 'w') as csv_file:
        wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL, lineterminator='\n')
        wr.writerow(field_names)
        for row in csv_rows:
            wr.writerow(row)


def create_corpus_phrase_csv(corpus_phrases_n):
    logging.info("Entering create_corpus_phrase_csv method")
    field_names = []
    csv_rows = []

    for corpus_phrases in corpus_phrases_n:
        if len(csv_rows) == 0:
            field_names.append(MAIN_WORD)
            field_names.append(PHRASE)
            field_names.append(COUNT)

        for corpus_phrase in corpus_phrases:
            csv_rows.append([corpus_phrase.main_word, corpus_phrase.phrase, corpus_phrase.count])

    with open(CSV_PHRASE_ANALYSIS_FILE, 'w') as csv_file:
        wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL, lineterminator='\n')
        wr.writerow(field_names)
        for row in csv_rows:
            wr.writerow(row)


def create_random_sample_csv(corpus_phrases, random_samples=3):
    logging.info("Entering create_random_sample_csv method")

    field_names = [PHRASE, WORDS_BY_PHRASE, CUMULATIVE_FREQUENCY]
    csv_rows = []
    cumulative_words_frequency = 0
    random_corpus_phrases = random.sample(corpus_phrases, random_samples)

    for phrase in random_corpus_phrases:
        words_in_phrase = len(phrase.split())
        cumulative_words_frequency += words_in_phrase
        csv_rows.append([phrase, words_in_phrase, cumulative_words_frequency])

    date = datetime.now().strftime("%m_%d_%Y-%I_%M_%S_")

    with open(CSV_RANDOM_PHRASES+"_"+date+".csv", 'w') as csv_file:
        wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL, lineterminator='\n')
        wr.writerow(field_names)
        for row in csv_rows:
            wr.writerow(row)

