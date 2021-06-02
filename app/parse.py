import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

nltk.download("stopwords")

STOP_WORDS = set(stopwords.words("english"))

def parser_stop_words(file_path: str):
    processed_email = []
    with open(file_path, 'r') as email_text:
        for word in email_text:
            if word.casefold() not in STOP_WORDS:
                processed_email.append(word)

    return processed_email


def data_parser(file_path: str):
    # dd/mm/yyyy, dd-mm-yyyy or dd.mm.yyyy format
    # data_regex = re.compile((' ^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30) '
    #                          ' (\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$| '
    #                          ' ^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]| '
    #                          ' [2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$| '
    #                          ' ^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])| '
    #                          ' (?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$ '
    #                   ))
    #data_string_regex = r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]|(?:Jan|Mar|May|Jul|Aug|Oct|Dec)))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2]|(?:Jan|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)(?:0?2|(?:Feb))\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9]|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep))|(?:1[0-2]|(?:Oct|Nov|Dec)))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$'
    data_string_regex = r'(^(?:(?:(?:31(?:(?:([-.\/])(?:0?[13578]|1[02])\1)|(?:([-.\/ ])(?:Jan|JAN|Mar|MAR|May|MAY|Jul|JUL|Aug|AUG|Oct|OCT|Dec|DEC)\2)))|(?:(?:29|30)(?:(?:([-.\/])(?:0?[13-9]|1[0-2])\3)|(?:([-.\/ ])(?:Jan|JAN|Mar|MAR|Apr|APR|May|MAY|Jun|JUN|Jul|JUL|Aug|AUG|Sep|SEP|Oct|OCT|Nov|NOV|Dec|DEC)\4))))(?:(?:1[6-9]|[2-9]\d)?\d{2}))$|^(?:29(?:(?:([-.\/])(?:0?2)\5)|(?:([-.\/ ])(?:Feb|FEB)\6))(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00)))$|^(?:(?:0?[1-9]|1\d|2[0-8])(?:(?:([-.\/])(?:(?:0?[1-9]|(?:1[0-2])))\7)|(?:([-.\/ ])(?:Jan|JAN|Feb|FEB|Mar|MAR|May|MAY|Jul|JUL|Aug|AUG|Oct|OCT|Dec|DEC)\8))(?:(?:1[6-9]|[2-9]\d)?\d{2}))$)'
    data_result = []
    with open(file_path, 'r') as email_text:
        for word in email_text:
            if re.match(data_string_regex, word):
                data_result.append(word)
    return data_result
