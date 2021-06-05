import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, regexp_tokenize
import re
import spacy
from app.parse import DATA_REGEX, TIME_REGEX

nltk.download("stopwords")
STOP_WORDS = set(stopwords.words("english"))

class Message:
    '''
        In the future it will be in prefect
    '''
    def __init__(self, text: str = None, user: str = None):
        tokens_dirty = nltk.word_tokenize(text)
        self.tokens = [word for word in tokens_dirty if not word in STOP_WORDS]
        self.user = user
        self.timelog = {}

    def parse_text(self):
        nlp_pipe = self.nlp_pipe()
        num = 0
        for ind, word in enumerate(nlp_pipe):
            # cache words sequence 'NUM' 'NUM' and 'ADJ' or 'NOUN'
            # ('NUM', 'NUM', 'ADJ), ('NUM', 'NUM', NOUN') in - way to solve ('NUM', NOUN', 'NUM')
            event = {}
            if ind <= len(nlp_pipe)-3:
                if nlp_pipe[ind][1] == 'NUM' and \
                   nlp_pipe[ind+1][1] == 'NUM' and \
                   nlp_pipe[ind+2][1] == 'NOUN' or \
                   nlp_pipe[ind][1] == 'NUM' and \
                   nlp_pipe[ind+1][1] == 'NUM' and \
                   nlp_pipe[ind+2][1] == 'ADJ':

                    num += 1
                    event_name = f'event_{num}'
                    event['start_time'] = nlp_pipe[ind][0]
                    event['end_time'] = nlp_pipe[ind+1][0]
                    event['project_name'] = nlp_pipe[ind+2][0]
                    event['employee'] = self.find_employee() or 'Someone'

                    self.timelog[event_name] = event

        return self.timelog


    def find_employee(self):
        self.employee = None
        nlp_pipe = self.nlp_pipe()
        for ind, word in enumerate(nlp_pipe):
            if word[1] == 'NOUN':
                self.employee = word[0]
                break
            # after 4 token break, name should be in first 4 words
            if ind > 3:
                break
        return str(self.employee)


    def to_dict(self):
        self.timelog['user'] = self.user
        return self.timelog


    def nlp_pipe(self):
        '''
            nlp.pipe to process a (potentially very large) iterable of texts
            as a stream

            nlp.pipe
                Args: seqeunce -> List
        '''
        nlp = spacy.load("en_core_web_sm")
        nlp_result = []
        for doc in nlp.pipe(self.tokens):
            for ent in doc:
                nlp_result.append((ent, ent.pos_))
        return nlp_result


    def data_parser(self):
        data_result = []
        for token in self.tokens:
            if re.match(DATA_REGEX, token):
                data_result.append(token)
        return str(data_result)


    def time_parser(self):
        time_result = []
        for token in self.tokens:
            if re.match(TIME_REGEX, token):
                time_result.append(token)
        return time_result
