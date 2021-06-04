import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, regexp_tokenize
import re
import spacy
from sqlalchemy.orm import Session

from sqlalchemy import insert, select, create_engine, MetaData, Table, Column, Integer, String
from app.parse import DATA_REGEX, TIME_REGEX

engine = create_engine('sqlite:///events.db', echo = True)
# holds a collection of Table objects
meta = MetaData()

# Create a database
Events_table = Table(
   'Events', meta,
   Column('id', Integer, primary_key = True),
   Column('date', String),
   Column('start_time', String),
   Column('end_time', String),
   Column('author', String),
   Column('event_name', String),
   Column('employee', String)
)
meta.create_all(engine)

nltk.download("stopwords")
STOP_WORDS = set(stopwords.words("english"))

class Event:

    def __init__(self,
                 date: str = None,
                 start_time: str = None,
                 end_time: str = None,
                 employee: str = None,
                 author: str = None,
                 event_name: str = None):

        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.author = author
        self.event_name = event_name
        self.employee = employee
        print("generate an event - date: {}, start time: {}, end time: {},\
         employee: {}, author: {}, event_name: {}".format(self.date,
                                                          self.start_time,
                                                          self.end_time,
                                                          self.employee,
                                                          self.author,
                                                          self.event_name))
        # conn = engine.connect()

    def __call__(self):
        """Generate an Event"""


class Parser:
    '''
        In the future it will be in prefect
    '''

    def __init__(self, file_path: str = None):
        with open(file_path, 'r') as email_text:
            text_mail = email_text.read()
            tokens_dirty = nltk.word_tokenize(text_mail)
        self.tokens = [word for word in tokens_dirty if not word in STOP_WORDS]
        self.date = self.data_parser() or "date"
        self.nlp_pipe = self.nlp_pipe()
        self.events_list = self.create_events_list()
        self.employee = self.find_employee() or "employee"
        self.author = 'author'


    def insert_into(self):
        with engine.connect() as conn:
            for event in self.events_list:
                evn = insert(Events_table).values(date = self.date,
                                             start_time = str(event[0]),
                                             end_time = str(event[1]),
                                             author = self.author,
                                             event_name = str(event[2]),
                                             employee = self.employee
                                             )
                conn.execute(evn)
            #conn.commit()

    def select_query(self, query: str = None):
        sql_query = select(Events_table)
        with engine.connect() as conn:
            for row in conn.execute(sql_query):
                print(row)


    # def run(self, query: str):
    #     conn = engine.connect()
    #     q = Events_table.select()
    #     result = conn.execute(q)
    #     if query.upper().startswith("SELECT"):
    #         return result.fetchall()


    def create_events_list(self):
        self.events_list = []
        for ind, word in enumerate(self.nlp_pipe):
            # cache words sequence 'NUM' 'NUM' and 'ADJ' or 'NOUN'
            # ('NUM', 'NUM', 'ADJ), ('NUM', 'NUM', NOUN') in - way to solve ('NUM', NOUN', 'NUM')
            if ind <= len(self.nlp_pipe)-3:
                if self.nlp_pipe[ind][1] == 'NUM' and \
                   self.nlp_pipe[ind+1][1] == 'NUM' and \
                   self.nlp_pipe[ind+2][1] == 'NOUN' or \
                   self.nlp_pipe[ind][1] == 'NUM' and \
                   self.nlp_pipe[ind+1][1] == 'NUM' and \
                   self.nlp_pipe[ind+2][1] == 'ADJ':

                    self.events_list.append( (self.nlp_pipe[ind][0],
                                        self.nlp_pipe[ind+1][0],
                                        self.nlp_pipe[ind+2][0]) )
        return self.events_list

    def find_employee(self):
        self.employee = None
        for ind, word in enumerate(self.nlp_pipe):
            if word[1] == 'NOUN':
                self.employee = word[0]
                break
            # after 4 token break, name should be in first 4 words
            if ind > 3:
                break
        return str(self.employee)


    # def create_events_obj(self):
    #     events_object_list = []
    #     for event in self.events_list:
    #         single_event = Event(date = self.date, start_time = event[0], end_time = event[1],
    #                              employee = self.employee, event_name = event[2])
    #         events_object_list.append(single_event)
    #         #single_event.push_to_database()
    #     return events_object_list

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
