import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, regexp_tokenize
import re
import spacy

from app.parse import DATA_REGEX, TIME_REGEX

nltk.download("stopwords")
STOP_WORDS = set(stopwords.words("english"))

class Parser:

    def __init__(self, file_path: str = None):
        with open(file_path, 'r') as email_text:
            text_mail = email_text.read()
            tokens_dirty = nltk.word_tokenize(text_mail)
        self.tokens = [word for word in tokens_dirty if not word in STOP_WORDS]
        self.dates = self.data_parser()
        self.times = self.time_parser()
        self.nlp_pipe = self.nlp_pipe()


    def nlp_pipe(self):
        '''
            nlp.pipe to process a (potentially very large) iterable of texts
            as a stream
        '''

        nlp = spacy.load("en_core_web_sm")
        nlp_result = []
        for doc in nlp.pipe(self.tokens, disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"]):
            for ent in doc.ents:
                nlp_result.append((ent.text, ent.label_))
        return nlp_result

    def data_parser(self):
        data_result = []
        for token in self.tokens:
            if re.match(DATA_REGEX, token):
                data_result.append(token)
        return data_result


    def time_parser(self):
        time_result = []
        for token in self.tokens:
            if re.match(TIME_REGEX, token):
                time_result.append(token)
        return time_result
