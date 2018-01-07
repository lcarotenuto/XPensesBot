import os
import httplib2
import pycountry
import locale
from datetime import datetime
from config import *

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


def get_credentials():
    """
    Returns:
        Credentials, the obtained credential.
    """
    client_secret_path = VARS['CLIENT_SECRET_PATH']
    scopes = VARS['SCOPES']
    application_name = VARS['APPLICATION_NAME']

    current_dir = os.getcwd()
    credential_dir = os.path.join(current_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    credentials_filename = CONSTANTS['CREDENTIALS_FILENAME']
    credential_path = os.path.join(credential_dir, credentials_filename)
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secret_path, scopes)
        flow.user_agent = application_name
        if flags:
            credentials = tools.run_flow(flow, store)

        print("Storing credentials {0} to {1}".format(credentials, credential_path))

    return credentials


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
    discovery_url = VARS['DISCOVERY_URL']
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discovery_url)


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
