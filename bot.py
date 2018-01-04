import requests
import os
import httplib2
import pycountry
import locale
from datetime import datetime

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'res/client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

def get_credentials():
    """
    Returns:
        Credentials, the obtained credential.
    """

    current_dir = os.getcwd()
    credential_dir = os.path.join(current_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_angent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store)
        else: # Python 2 compatibility
            credentials = tools.run(flow, store)
        print("Storing credentials {0} to {1}".format(credentials, credential_path))

    return credentials

def listener():
    print("Sono Listener")

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

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discovery_url = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discovery_url)

    spreadsheet_id = '1UU0fr7jpVrW6d5YQWLOwfYgtim5AN090Tjhfp9lljPs'

    day, month = get_date()
    range_name = "{0}!A2:C2".format(month)

    values = [
        [day, "mioTest", 30]
    ]
    body = {
        "values": values
    }

    result = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id,
                                                    range=range_name,
                                                    valueInputOption="USER_ENTERED",
                                                    body=body).execute()
    print(result)


if __name__ == '__main__':
    main()