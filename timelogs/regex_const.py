import re

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
