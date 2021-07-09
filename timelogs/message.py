import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, regexp_tokenize
import re
import spacy
from .regex_const import DATA_REGEX, TIME_REGEX
from datetime import date, datetime, timedelta

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
        self.text = text
        tokens_dirty = nltk.word_tokenize(text)
        self.tokens = [word for word in tokens_dirty if not word in STOP_WORDS]
        self.tokens = tokens_dirty
        self.user = user
        self.ts = ts
        self.timelogs = []


    def check_delete(self):
        '''
            Check if delete keyword is in message
            return data of timelogs which will be deleted
        '''
        #print("----------     check delete     ------------")
        if 'delete' in self.text.lower():
            if 'today' in self.text.lower():
                today_str = datetime.today().strftime("%d.%m.%Y")
                return datetime.strptime(today_str, "%d.%m.%Y")
            data = re.findall('\d+.\d{2}.\d{4}', self.text)
            if data:
                return datetime.strptime(data[0], '%d.%m.%Y')
        return None


    def check_add_me(self):
        #should check also if user is not in master_db
        name = None
        #print("----------     check_add_me      ------------")
        ADD_ME_REGEX = '([aAdD]{3}.[mMeE]{2})\s(\w+)'
        #print(f'token: {self.text}')
        for match in re.finditer(ADD_ME_REGEX, self.text):
            name = match[2]
            print(match.groups())
            print(name)
            return name


    def to_records(self):
        nlp_pipe = self.nlp_pipe()
        print("-------------------   nlp_pipe: {}         --------------".format(nlp_pipe))
        timelog = {}
        timelog['project_name'] = 'meeting'
        timelog['h'] = None
        timelog['date'] = None
        time1, time2 = None, None
        for ind, word in enumerate(nlp_pipe):
            if word[1] == 'NUM':
                date_or_time = str(word[0])
                print(f"there is a num: {date_or_time}")
                if re.match(DATA_REGEX, date_or_time):
                    print("jest data: {}".format(date_or_time))
                    timelog['date'] = date_or_time
                if re.match(TIME_REGEX, date_or_time):
                    if not time1:
                        time1 = str(word[0])
                        time1_timetype = datetime.strptime(time1, '%H:%M')
                        #print("type(time1): {}".format(type(time1)))
                        print(f"time1: {time1}")
                    else:
                        time2 = str(word[0])
                        time2_timetype = datetime.strptime(time2, '%H:%M')
                        print("type(time12): {}".format(type(time2_timetype)))
                        print(f"time2: {time2}")
            if word[1] == 'NOUN':
                word = str(word[0])
                if word.lower() == 'today':
                    today_str = datetime.today().strftime("%d.%m.%Y")
                    timelog['date'] = datetime.strptime(today_str, "%d.%m.%Y")
                elif word.lower() == 'yesterday':
                    yesterday = datetime.today() - timedelta(days=1)
                    yesterday_str = yesterday.strftime("%d.%m.%Y")
                    timelog['date'] = datetime.strptime(yesterday_str, "%d.%m.%Y")
                else:
                    timelog['project_name'] = word

            if word[1] == 'ADJ' or word[1] == 'VERB':
                timelog['project_name'] = str(word[0])

        if time1 == None:
            timelog['start_time'] = time2
            timelog['end_time'] = None
        if time2 == None:
            timelog['start_time'] = time1
            timelog['end_time'] = None
        if time1 and time2:
            timelog['start_time'] = time1
            timelog['end_time'] = time2

            working_hours = ((time1_timetype - time2_timetype).total_seconds())/3600
            if working_hours < 0:
                working_hours = -working_hours
            timelog['h'] = working_hours

        # if date and start time this timelogs is useful
        if timelog['date'] and timelog['start_time']:
            timelog['user'] = self.user
            timelog['ts'] = self.ts
            self.timelogs.append(timelog)
            print(f'timelog: {timelog}')
            return self.timelogs

        return None


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
