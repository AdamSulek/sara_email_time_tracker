import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, regexp_tokenize
import re
import spacy
from app.parse import DATA_REGEX, TIME_REGEX

nltk.download("stopwords")
STOP_WORDS = set(stopwords.words("english"))

class Message:
    """
    A class implementing Natural language processing
    to parse timelog information from messages.

    Parameters
    ----------
    text: str, optional
        The parameter to fetch information from text message.
        by default None
    user: str, optional
        The parameter to store author of message.
        by default None
    """
    def __init__(self, text: str = None, user: str = None):
        tokens_dirty = nltk.word_tokenize(text)
        self.tokens = [word for word in tokens_dirty if not word in STOP_WORDS]
        self.user = user
        self.timelogs = []


    def to_records(self):
        nlp_pipe = self.nlp_pipe()
        num = 0
        for ind, word in enumerate(nlp_pipe):
            # cache words sequence 'NUM' 'NUM' and 'ADJ' or 'NOUN'
            # ('NUM', 'NUM', 'ADJ), ('NUM', 'NUM', NOUN') in - way to solve ('NUM', NOUN', 'NUM')
            timelog = {}
            if ind <= len(nlp_pipe)-3:
                if nlp_pipe[ind][1] == 'NUM' and \
                   nlp_pipe[ind+1][1] == 'NUM' and \
                   nlp_pipe[ind+2][1] == 'NOUN' or \
                   nlp_pipe[ind][1] == 'NUM' and \
                   nlp_pipe[ind+1][1] == 'NUM' and \
                   nlp_pipe[ind+2][1] == 'ADJ':

                    num += 1
                    timelog_name = f'timelog_{num}'
                    timelog['timelog_name'] = f'timelog_{num}'
                    timelog['start_time'] = str(nlp_pipe[ind][0])
                    timelog['end_time'] = str(nlp_pipe[ind+1][0])
                    timelog['project_name'] = str(nlp_pipe[ind+2][0])
                    timelog['employee'] = self.find_employee() or 'Someone'
                    timelog['user'] = self.user
                    self.timelogs.append(timelog)

        return self.timelogs


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


    def nlp_pipe(self):
        '''
            nlp.pipe function process a (potentially very large) iterable of texts
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
