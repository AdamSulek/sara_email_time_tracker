import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, regexp_tokenize
import re
import spacy
from .regex_const import DATA_REGEX, TIME_REGEX

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
    def __init__(self, text: str = None, user: str = None, ts: float = None):
        tokens_dirty = nltk.word_tokenize(text)
        self.tokens = [word for word in tokens_dirty if not word in STOP_WORDS]
        self.tokens = tokens_dirty
        self.user = user
        self.ts = ts
        self.timelogs = []


    def to_records(self):
        nlp_pipe = self.nlp_pipe()
        print("nlp_pipe: {}".format(nlp_pipe))
        num = 0
        for ind, word in enumerate(nlp_pipe):
            # cache words sequence 'NUM' 'NUM' and 'ADJ' or 'NOUN'
            # ('NUM', 'NUM', 'ADJ), ('NUM', 'NUM', NOUN') in - way to solve ('NUM', NOUN', 'NUM')
            timelog = {}
            if ind <= len(nlp_pipe):

                if nlp_pipe[ind][1] == 'NUM' and \
                   nlp_pipe[ind+1][1] == 'NUM' and \
                   nlp_pipe[ind+2][1] == 'NOUN' or \
                   nlp_pipe[ind][1] == 'NUM' and \
                   nlp_pipe[ind+1][1] == 'NUM' and \
                   nlp_pipe[ind+2][1] == 'ADJ':

                    num += 1
                    timelog['start_time'] = str(nlp_pipe[ind][0])
                    timelog['end_time'] = str(nlp_pipe[ind+1][0])
                    timelog['project_name'] = str(nlp_pipe[ind+2][0])
                    timelog['user'] = self.user
                    timelog['ts'] = self.ts
                    print(timelog)
                    self.timelogs.append(timelog)
                else:
                    print("message not match to timelog")

        return self.timelogs


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
