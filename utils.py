import pycountry
import locale
import os
from datetime import datetime


def get_date():
    language = pycountry.languages.lookup("it")
    if os.name == 'posix':
        locale.setlocale(locale.LC_ALL, language.alpha_2)
    else:
        locale.setlocale(locale.LC_ALL, language.name)

    # TODO: da sistemare
    today = datetime.today()
    day = today.day
    month = datetime.strptime(str(today.month), "%m").strftime("%B").capitalize()

    return day, month
