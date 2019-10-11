from __future__ import print_function
import pickle
import os.path
import httplib2
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

from config.config import path_credentials_directory


def get_directory_service():
    """
    Authorize in Google via OAuth Flow.

    :return: Authenticated service object.
    """
    google_api_scopes = [
        'https://www.googleapis.com/auth/admin.directory.user',
        'https://www.googleapis.com/auth/admin.directory.group'
    ]
    credentials = None

    if os.path.exists(path_credentials_directory / 'token.pickle'):
        with open(path_credentials_directory / 'token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                path_credentials_directory / 'credentials.json',
                google_api_scopes)

            credentials = flow.run_local_server(port=0)

        with open(path_credentials_directory / 'token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    service = build('admin', 'directory_v1', credentials=credentials)

    return service


def get_groupsettings_service():
    flow = flow_from_clientsecrets(
        path_credentials_directory / 'credentials.json',
        scope='https://www.googleapis.com/auth/apps.groups.settings',
        message='Missing client secrets.'
    )

    storage = Storage(path_credentials_directory / 'groupsettings.dat')
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)

    http = httplib2.Http()
    http = credentials.authorize(http)

    service = build('groupssettings', 'v1', http=http)

    return service


if __name__ == '__main__':
    get_directory_service()
    get_groupsettings_service()
