import logging
import nltk

from csv import reader
from corpusConstants import CSV_PHRASE_ANALYSIS_FILE
from corpusUtility import create_random_sample_csv


logging.basicConfig(format='%(levelname)s:%(asctime)s - %(message)s', level=logging.INFO)
logging.info('Getting corpus phrases from csv file %s ', CSV_PHRASE_ANALYSIS_FILE)

# project_root = os.path.dirname(os.path.dirname(__file__))
project_root = "X:/codebase_python/Corpus-Alpha-Analysis/Corpus-Alpha-Analysis/"
output_path = project_root + CSV_PHRASE_ANALYSIS_FILE

filename = nltk.data.find(output_path)

phrases = []
with open(filename, 'r', encoding='latin-1') as file:
    csv_reader = reader(file)
    header = next(csv_reader)
    if header is not None:
        for row in csv_reader:
            phrases.append(row[1])

create_random_sample_csv(phrases, 20)

logging.info("Routine Finished")
