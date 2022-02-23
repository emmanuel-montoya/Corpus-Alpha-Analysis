ROOT_DIR = "X:/raw_es/"

filename_list = ['spanishText_10000_15000.txt', 'spanishText_15000_20000.txt', 'spanishText_20000_25000.txt',
                'spanishText_25000_30000.txt', 'spanishText_45000_50000.txt', 'spanishText_40000_45000.txt',
                'spanishText_70000_75000.txt', 'spanishText_90000_95000.txt', 'spanishText_110000_115000.txt',
                'spanishText_120000_125000.txt', 'spanishText_180000_185000.txt', 'spanishText_185000_190000.txt',
                'spanishText_200000_205000.txt', 'spanishText_205000_210000.txt', 'spanishText_210000_215000.txt',
                'spanishText_225000_230000.txt', 'spanishText_230000_235000.txt', 'spanishText_260000_265000.txt',
                'spanishText_265000_270000.txt', 'spanishText_270000_275000.txt', 'spanishText_285000_290000.txt',
                'spanishText_305000_310000.txt', 'spanishText_310000_315000.txt', 'spanishText_315000_320000.txt',
                'spanishText_320000_325000.txt', 'spanishText_325000_330000.txt', 'spanishText_330000_335000.txt',
                'spanishText_335000_340000.txt', 'spanishText_340000_345000.txt', 'spanishText_345000_350000.txt',
                'spanishText_350000_355000.txt', 'spanishText_355000_360000.txt', 'spanishText_360000_365000.txt',
                 'spanishText_365000_370000.txt', 'spanishText_370000_375000.txt', 'spanishText_375000_380000.txt',
                 'spanishText_380000_385000.txt', 'spanishText_385000_390000.txt', 'spanishText_390000_395000.txt',
                 'spanishText_395000_400000.txt', 'spanishText_400000_405000.txt', 'spanishText_405000_410000.txt',
                 'spanishText_410000_415000.txt', 'spanishText_415000_420000.txt', 'spanishText_420000_425000.txt',
                 'spanishText_425000_430000.txt', 'spanishText_430000_435000.txt', 'spanishText_435000_440000.txt',
                 'spanishText_440000_445000.txt', 'spanishText_445000_450000.txt', 'spanishText_450000_455000.txt',
                 'spanishText_455000_460000.txt', 'spanishText_460000_465000.txt', 'spanishText_465000_470000.txt',
                 'spanishText_470000_475000.txt', 'spanishText_475000_480000.txt', 'spanishText_480000_485000.txt']

unusual_letters = ['th', 'ae', 'ss']

wikipedia_stopWords = ['wikisalamanca', 'endofarticle', 'systematics',
                       'ppp', 'index', 'international', 'plant', 'names',
                       'catalogue', 'life', 'encyclopedia', 'http',
                       'www', 'mobot', 'research', 'apweb', 'site',
                       'biopl', 'edu']

wikipedia_stopPhrases = ['véase también', 'vease tambíen',
                         'enlaces externos',
                         'enlace externo',
                         'enlace a']

DOC_SIZE = 56
NUMBER_OF_WORDS = 1000
PHRASE_TOLERANCE = 25
SHOW_CHARTS = True
PRE_POST_CORPUS_FLAG = True

LETTERS_FREQUENCY = "Frecuencia de letras"
LETTER = "Letra"
WORD = "Palabra"
PHRASE = "Frase"
MAIN_WORD = "Palabra Principal"
COUNT = "Count"
WORDS_BY_PHRASE = "Palabras por Frase"
WORDS_BY_PHRASE = "Palabras por Frase"
CUMULATIVE_FREQUENCY = "Frecuencia Acumulada"
PRE_TOKEN = "Pre_token"
PRE_COUNT = "Pre_count"
POST_TOKEN = "Post_token"
POST_COUNT = "Post_count"

CSV_ALPHA_ANALYSIS_FILE = 'corpus-csv/corpus-alpha-analysis.csv'
CSV_WORD_ANALYSIS_FILE = 'corpus-csv/corpus-word-analysis.csv'
CSV_PHRASE_ANALYSIS_FILE = 'corpus-csv.csv'
CSV_RANDOM_PHRASES = 'corpus-random-phrases'

LETTERS_FREQUENCY_ORDER = 'Orden de frecuencia relativa de letras'
WORDS_FREQUENCY_ORDER = 'Orden de frecuencia relativa de palabras'


class CorpusLetter:
    def __init__(self, name, count, pre_tokens, post_tokens):
        self.name = name
        self.count = count
        self.pre_tokens = pre_tokens
        self.post_tokens = post_tokens


class CorpusWord:
    def __init__(self, name, count, pre_tokens, post_tokens):
        self.name = name
        self.count = count
        self.pre_tokens = pre_tokens
        self.post_tokens = post_tokens


class CorpusPhrase:
    def __init__(self, main_word, phrase, phrase_words, count=0, pre_tokens=[], post_tokens=[]):
        self.main_word = main_word
        self.phrase = phrase
        self.phrase_words = phrase_words
        self.count = count
        self.pre_tokens = pre_tokens
        self.post_tokens = post_tokens
