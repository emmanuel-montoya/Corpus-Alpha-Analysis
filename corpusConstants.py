# from sklearn.feature_extraction.text import CountVectorizer
#
# #Declaring all sentences and assigning to a document
# sentence1="This is my code on bag of words."
# sentence2="Bag of words is a NLP technique."
# sentence3="I will explain it to you in a simple way"
#
# #Making a list or Document from all sentences
# Doc=[sentence1,sentence2,sentence3]
#
# #Initializing CountVectorizer from sklearn
# vectorizer = CountVectorizer(stop_words='english')
#
# X = vectorizer.fit_transform(Doc)
#
# print(vectorizer.get_feature_names())
# ['bag', 'code', 'explain', 'nlp', 'simple', 'technique', 'way', 'words']
#
# print(X.toarray())
#

ROOT_DIR = "X:/raw_es/"

filenameList = [ROOT_DIR + 'spanishText_10000_15000.txt', ROOT_DIR + 'spanishText_15000_20000.txt',
                ROOT_DIR + 'spanishText_20000_25000.txt', ROOT_DIR + 'spanishText_25000_30000.txt',
                ROOT_DIR + 'spanishText_45000_50000.txt', ROOT_DIR + 'spanishText_40000_45000.txt',
                ROOT_DIR + 'spanishText_70000_75000.txt', ROOT_DIR + 'spanishText_90000_95000.txt',
                ROOT_DIR + 'spanishText_110000_115000.txt', ROOT_DIR + 'spanishText_120000_125000.txt',
                ROOT_DIR + 'spanishText_180000_185000.txt', ROOT_DIR + 'spanishText_185000_190000.txt',
                ROOT_DIR + 'spanishText_200000_205000.txt', ROOT_DIR + 'spanishText_205000_210000.txt',
                ROOT_DIR + 'spanishText_210000_215000.txt', ROOT_DIR + 'spanishText_225000_230000.txt',
                ROOT_DIR + 'spanishText_230000_235000.txt', ROOT_DIR + 'spanishText_260000_265000.txt',
                ROOT_DIR + 'spanishText_265000_270000.txt', ROOT_DIR + 'spanishText_270000_275000.txt',
                ROOT_DIR + 'spanishText_285000_290000.txt', ROOT_DIR + 'spanishText_305000_310000.txt',
                ROOT_DIR + 'spanishText_310000_315000.txt', ROOT_DIR + 'spanishText_315000_320000.txt',
                ROOT_DIR + 'spanishText_320000_325000.txt', ROOT_DIR + 'spanishText_325000_330000.txt',
                ROOT_DIR + 'spanishText_330000_335000.txt', ROOT_DIR + 'spanishText_335000_340000.txt',
                ROOT_DIR + 'spanishText_340000_345000.txt', ROOT_DIR + 'spanishText_345000_350000.txt',
                ROOT_DIR + 'spanishText_350000_355000.txt', ROOT_DIR + 'spanishText_355000_360000.txt',
                ROOT_DIR + 'spanishText_360000_365000.txt', ROOT_DIR + 'spanishText_365000_370000.txt',
                ROOT_DIR + 'spanishText_370000_375000.txt', ROOT_DIR + 'spanishText_375000_380000.txt',
                ROOT_DIR + 'spanishText_380000_385000.txt', ROOT_DIR + 'spanishText_385000_390000.txt',
                ROOT_DIR + 'spanishText_390000_395000.txt', ROOT_DIR + 'spanishText_395000_400000.txt',
                ROOT_DIR + 'spanishText_400000_405000.txt', ROOT_DIR + 'spanishText_405000_410000.txt',
                ROOT_DIR + 'spanishText_410000_415000.txt', ROOT_DIR + 'spanishText_415000_420000.txt',
                ROOT_DIR + 'spanishText_420000_425000.txt', ROOT_DIR + 'spanishText_425000_430000.txt',
                ROOT_DIR + 'spanishText_430000_435000.txt', ROOT_DIR + 'spanishText_435000_440000.txt',
                ROOT_DIR + 'spanishText_440000_445000.txt', ROOT_DIR + 'spanishText_445000_450000.txt',
                ROOT_DIR + 'spanishText_450000_455000.txt', ROOT_DIR + 'spanishText_455000_460000.txt',
                ROOT_DIR + 'spanishText_460000_465000.txt', ROOT_DIR + 'spanishText_465000_470000.txt',
                ROOT_DIR + 'spanishText_470000_475000.txt', ROOT_DIR + 'spanishText_475000_480000.txt',
                ROOT_DIR + 'spanishText_480000_485000.txt']

xml_stopWords = ['doc', 'id', 'title', 'nonfiltered', 'processed', 'dbindex', 'of', 'The', 'ENDOFARTICLE']
unusual_letters = ['th', 'ae', 'ss']
wikipedia_stopWords = ['systematics', 'ppp', 'index', 'international', 'plant', 'names', 'catalogue', 'life', 'encyclopedia', 'http', 'www', 'mobot', 'research', 'apweb', 'site', 'biopl', 'edu']

#DOC_SIZE = 56
DOC_SIZE = 1
NUMBER_OF_WORDS = 100
NUMBER_OF_LETTERS = 100
SHOW_CHARTS = True

class CorpusLetter:
    def __init__(self, name, count, pre_tokens, post_tokens):
        self.name = name
        self.count = count
        self.pre_tokens = pre_tokens
        self.post_tokens = post_tokens


