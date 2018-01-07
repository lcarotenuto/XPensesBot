import pycountry
from config import *
import locale
import os
from datetime import datetime


def get_date():
    language = pycountry.languages.lookup(CONSTANTS["LOCALE"])
    if os.name == 'posix':
        locale.setlocale(locale.LC_ALL, language.alpha_2)
    else:
        locale.setlocale(locale.LC_ALL, language.name)

    today = datetime.today()
    day = today.day
    month = today.strftime("%B").capitalize()

    return day, month
