from config import *
from utils import get_date
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


class GDocument:
    def __init__(self, spreadsheet_id):
        self.credentials = self.__init_credentials()
        self.spreadsheet_id = spreadsheet_id

    def __init_credentials(self):
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
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(client_secret_path, scopes)
            flow.user_agent = application_name
            creds = tools.run_flow(flow, store)

            print("Storing credentials {0} to {1}".format(creds, credential_path))

        self.credentials = creds

        return self.credentials

    def write_expense(self, title, value):
        http = self.credentials.authorize(httplib2.Http())
        discovery_url = VARS['DISCOVERY_URL']
        service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discovery_url)

        day, month = get_date()
        range_name = "{0}!A2:C2".format(month)

        body = {
            "values": [
                [day, title, value]
            ]
        }

        result = service.spreadsheets().values().append(spreadsheetId=self.spreadsheet_id,
                                                        range=range_name,
                                                        valueInputOption="USER_ENTERED",
                                                        body=body).execute()

        return result
