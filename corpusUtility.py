import collections

import unidecode
import csv
import matplotlib.pyplot as plt
import squarify
import re
import string

from corpusConstants import CorpusLetter


def get_common_info(chars, size=0):
    counter_letters = collections.Counter(chars)
    print(counter_letters.most_common(size))
    return counter_letters.most_common(size) if size > 0 else counter_letters.most_common()


def get_pre_post_corpus(common_tokens, word_corpus, is_letter=False):
    corpus_letters = []

    for token in common_tokens:
        token_text = token[0]
        token_count = token[1]
        pre_token = []
        post_token = []

        if len(token_text) < 4 and is_letter is False:
            continue

        print("Pre y Post Tokens for letter: ", token_text)
        word_indexes = [i for i, w in enumerate(word_corpus) if w.find(token_text) != -1]

        for word_index in word_indexes:
            if is_letter:
                word = word_corpus[word_index]
                letter_index = word.index(token_text)
                if letter_index > 0:
                    pre_token.append(unidecode.unidecode(word[letter_index - 1]).lower())

                if letter_index < (len(word) - 1):
                    post_token.append(unidecode.unidecode(word[letter_index + 1]).lower())
            else:
                pre_token.append(unidecode.unidecode(word_corpus[word_index - 1]).lower())
                post_token.append(unidecode.unidecode(word_corpus[word_index + 1]).lower())

        corpus_letters.append(CorpusLetter(token_text, token_count, get_common_info(pre_token, 50), get_common_info(post_token, 50)))
    return corpus_letters


def create_csv_file(pre_post_corpus, is_letter=False, common_limit=2):
    field_names = []
    csv_rows = []

    for corpusLetter in pre_post_corpus:
        if len(csv_rows) == 0:
            field_names.append("Letra") if is_letter else field_names.append("Palabra")
            field_names.append("Count")

        csv_row = [corpusLetter.name, corpusLetter.count]

        for i in range(common_limit):
            if len(csv_rows) == 0:
                field_names.append("PreToken" + str(i))
                field_names.append("PreCount" + str(i))
                field_names.append("PostToken" + str(i))
                field_names.append("PostCount" + str(i))

            if i < len(corpusLetter.pre_tokens):
                csv_row.append(corpusLetter.pre_tokens[i][0])
            if i < len(corpusLetter.pre_tokens):
                csv_row.append(corpusLetter.pre_tokens[i][1])
            if i < len(corpusLetter.post_tokens):
                csv_row.append(corpusLetter.post_tokens[i][0])
            if i < len(corpusLetter.post_tokens):
                csv_row.append(corpusLetter.post_tokens[i][1])

        csv_rows.append(csv_row)

    csv_file_name = 'corpus-alpha-analysis.csv' if is_letter else 'corpus-word-analysis.csv'

    with open(csv_file_name, 'w') as csv_file:
        wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL, lineterminator='\n')
        wr.writerow(field_names)
        for row in csv_rows:
            wr.writerow(row)


def plot_common_info(most_common_tokens, is_letter=False):
    label_letters = []
    size_letters = []
    for a in range(len(most_common_tokens)):
        label_letters.append(most_common_tokens[a][0])
        size_letters.append(most_common_tokens[a][1])

    squarify.plot(sizes=size_letters, label=label_letters, alpha=.8)
    plt.axis('off')
    plt.title('Orden de frecuencia relativa de letras.') if is_letter else plt.title('Orden de frecuencia relativa de palabras.')
    plt.show()


def get_normalized_alpha_chars(words):
    alpha_chars = []
    for word in words:
        alpha_chars.extend([unidecode.unidecode(char) for char in word])
    return alpha_chars

def getListWordsPreprocessed(corpus):
    ''' return a corpus after removing all the patterns and the xml markup (if any) '''
    text = corpus.lower()
    text = re.sub('<.*>', '', text)
    text = re.sub('ENDOFARTICLE.', '', text)
    punctuation2remove = "[" + re.sub('[,.;:?!()+/-]', '', string.punctuation) + "]"
    text = re.sub(punctuation2remove, '', text)
    text = re.sub('\n\n+', '\n', text)
    text = re.sub(';+\n', '\n', text)
    text = re.sub('\s*-\s', ' ', text)
    text = re.sub('\s+\.', ' ', text)
    text = re.sub('^\n', '', text, flags=re.MULTILINE)
    text = re.sub('^\s*\w+\s*\n', '', text, flags=re.MULTILINE)
    text = re.sub('\((\s*|\+*|\w\.\s*)\d+(\-*|\s*|,\s*)\d*\-*\)', ' ', text)
    text = re.sub('\(\s*\)', ' ', text)
    text = text.replace(',', ' <COMMA> ')
    text = text.replace('.', ' <PERIOD> ')
    text = text.replace(';', ' <SEMICOLON> ')
    text = text.replace(':', ' <CCOLONN> ')
    text = text.replace('?', ' <QUESTIONMARK> ')
    text = text.replace('!', ' <EXCLAMATIONMARK> ')
    text = text.replace('(', ' <LEFT_PARENTHESIS> ')
    text = text.replace(')', ' <RIGHT_PARENTHESIS> ')
    text = text.replace('/', ' <SLASH> ')
    text = text.replace('+', ' <PLUS_SIGN> ')
    text = text.replace('-', ' <DASH> ')
    text = re.sub('\s\d+\s', ' <NUMBER> ', text)
    words = text.split()
    #remove all words with 5 or fewer occurences
    word_cnts = collections.Counter(words)
    trimmed_words = [word for word in words if word_cnts[word] > 5]
    return trimmed_words

def clean_raw_data(raw_data):
    # get rid of all the XML markup
    raw_data = re.sub('<.*>', '', raw_data)
    # get rid of the "ENDOFARTICLE." text
    raw_data = re.sub('ENDOFARTICLE.', '', raw_data)
    # get rid of punctuation (except periods!)

    #punctuationNoPeriod = "[" + re.sub("\.", "", string.punctuation) + "]"
    punctuationNoPeriod = '[!"#$%&\'()*+,-/:;?@[\]^_`{|}~]'

    raw_data = re.sub(punctuationNoPeriod, "", raw_data)

    # getting rid of multiple consecutive '\n' characters
    raw_data = re.sub('\n\n+', '\n', raw_data)

    # getting rid of all those strange semicolons that are preceding any '\n\ character
    raw_data = re.sub(';+\n', '\n', raw_data)

    raw_data = re.sub(';+\n', '\n', raw_data)
    # getting rid of all the dashes (that could or could not be present) that are surrounded by any whitespace characters (i.e. [ \t\n\r\f\v])
    # the reson of explicitly getting rid of dashes surrounded by whitespaces characters is to avoid removing dashes that are used by composed words
    # like some last names (i.e. Garica-Rojas, Montero-Calvo) or some relational adjectives (i.e. físco-químico, épico-lírico), etc.
    raw_data = re.sub('\s*-\s', ' ', raw_data)
    # getting rid of any dots (that could or could not be present) that are precided by any whitespace characters
    raw_data = re.sub('\s+\.', ' ', raw_data)
    # Also remove any '\n' that might be found at the begining of a line.
    raw_data = re.sub('^\n', '', raw_data, flags=re.MULTILINE)
    # remove any word that is standing all alone (i.e. single words used as names of chapters/subsections, etc.). These words are not helping us to
    # construct a meaningful embedding (the relationship between these words and other preceding/following words will be learned by the algorithm,
    # but in these special cases, such relationships are just noise).
    raw_data = re.sub('^\s*\w+\s*\n', '', raw_data, flags=re.MULTILINE)
    # remove all numbers and/or dates enclosed in parenthesis
    # i.e. (672-680), (+737) (1980-)
    raw_data = re.sub('\((\s*|\+*|\w\.\s*)\d+(\-*|\s*|,\s*)\d*\-*\)', ' ', raw_data)
    # remove (if any) set of empty parenthesis
    raw_data = re.sub('\(\s*\)', ' ', raw_data)

    raw_data = raw_data.replace('véase también', '')
    raw_data = raw_data.replace('vease tambíen', '')
    raw_data = raw_data.replace('caracteristicas', '')
    raw_data = raw_data.replace('referencias', '')
    raw_data = raw_data.replace('enlaces externos', '')
    raw_data = raw_data.replace('enlaces externo', '')
    raw_data = raw_data.replace('enlace a', '')
    raw_data = raw_data.replace('wikisalamanca', '')

    # check to make sure the file read in alright; let's print out the first 1000 characters
    print(raw_data[0:100])