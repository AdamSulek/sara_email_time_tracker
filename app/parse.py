import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, regexp_tokenize
import re

nltk.download("stopwords")
STOP_WORDS = set(stopwords.words("english"))
# dd/mm/yyyy, dd-mm-yyyy, dd.mm.yyyy, dd/Month/yyyy, dd Month yyyy,
# dd/MONTH/yyyy or dd MONTH yyyy format
DATA_REGEX = re.compile('(^(?:(?:(?:31(?:(?:([-.\/])'
      '(?:0?[13578]|1[02])\2)|(?:([-.\/ ])'
      '(?:Jan|JAN|Mar|MAR|May|Apr|APR|MAY|Jul|JUL|Aug|AUG|Oct|OCT|Dec|DEC)\3)))|'
      '(?:(?:29|30)(?:(?:([-.\/])(?:0?[13-9]|1[0-2])\4)|(?:([-.\/ ])'
      '(?:Jan|JAN|Mar|MAR|Apr|APR|May|MAY|Jun|JUN|Jul|JUL|Aug|AUG|Sep|SEP|Oct|OCT|Nov|NOV|Dec|DEC)\5))))'
      '(?:(?:1[6-9]|[2-9]\d)?\d{2}))$|^(?:29(?:(?:([-.\/])(?:0?2)\6)|(?:([-.\/ ])'
      '(?:Feb|FEB)\7))(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|'
      '(?:(?:16|[2468][048]|[3579][26])00)))$|'
      '^(?:(?:0?[1-9]|1\d|2[0-8])(?:(?:([-.\/])(?:(?:0?[1-9]|(?:1[0-2])))\8)|'
      '(?:([-.\/ ])(?:Jan|JAN|Feb|FEB|Mar|MAR|Apr|APR|May|MAY|Jul|JUL|Aug|AUG|Oct|OCT|Dec|DEC)\9))'
      '(?:(?:1[6-9]|[2-9]\d)?\d{2}))$)')

TIME_REGEX = re.compile( '(^(0?[1-9]|1[0-2]):[0-5][0-9]$|)'                 #HH:MM 12-hour format
                         '((1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm]))|' #HH:MM 12-hour format, mandatory (AM/PM)
                         '(^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$)|'           #HH:MM 24-hour with leading 0
                         '(^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$)|'     #HH:MM 24-hour format, optional leading 0
                         '(?:[01]\d|2[0-3]):(?:[0-5]\d):(?:[0-5]\d)'      #HH:MM:SS 24-hour format with leading 0
                        )

def parser_stop_words(file_path: str):
    processed_email = []
    with open(file_path, 'r') as email_text:
        for word in email_text:
            if word.casefold() not in STOP_WORDS:
                processed_email.append(word)
    return processed_email


def data_parser(file_path: str):
    data_result = []
    with open(file_path, 'r') as email_text:
        for line in email_text.readlines():
            for word in line.split():
                if re.match(DATA_REGEX, word):
                    data_result.append(word)
    return data_result


def time_parser(file_path: str):
    time_result = []
    with open(file_path, 'r') as email_text:
        for line in email_text.readlines():
            for word in line.split():
                if re.match(TIME_REGEX, word):
                    time_result.append(word)
    return time_result
