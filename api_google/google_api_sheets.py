import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from config.config import path_credentials_directory


def get_sheets_service():
    """
    Authorize in Google via OAuth Flow.

    :return: Authenticated service object.
    """
    google_api_scopes = [
        'https://www.googleapis.com/auth/spreadsheets.readonly'
    ]
    credentials = None

    if os.path.exists(path_credentials_directory / 'token_sheets.pickle'):
        with open(path_credentials_directory / 'token_sheets.pickle', 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                path_credentials_directory / 'credentials.json',
                google_api_scopes)

            credentials = flow.run_local_server(port=0)

        with open(path_credentials_directory / 'token_sheets.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    service = build('sheets', 'v4', credentials=credentials)

    return service


def get_multiple_ranges(service, spreadsheet_id, range_names):
    """
    Get multiple ranges from Google Sheets.

    :param service: Authenticated sheets service object
    :param spreadsheet_id: Id of the spreadsheet
    :param range_names: Ranges to get
    :return: Results of the query
    """
    result = service.spreadsheets().values().batchGet(
        spreadsheetId=spreadsheet_id,
        ranges=range_names
    ).execute()

    ranges = result.get('valueRanges', [])

    return ranges


if __name__ == '__main__':
    get_sheets_service()
