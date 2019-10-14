from __future__ import print_function
import httplib2
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

from config.config import path_credentials_directory


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


def get_group_settings(service, group_key):
    """
    Get settings for a Google Group.

    https://github.com/googleapis/google-api-python-client/blob/master/samples/groupssettings/groupsettings.py
    :param service: Authenticated group settings service object
    :param group_key: Unique identifier of the group (string, email, or id)
    :return: Results of the query
    """
    results = service.groups().get(
        groupUniqueId=group_key
    ).execute()

    return results


def update_group_settings(service, group_key, settings):
    """
    Update settings for a Google Group.

    https://developers.google.com/admin-sdk/groups-settings/manage
    https://github.com/googleapis/google-api-python-client/blob/master/samples/groupssettings/groupsettings.py
    :param service: Authenticated group settings service object
    :param group_key: Unique identifier of the group (string, email, or id)
    :param settings: JSON of group settings
    :return: Results of the query
    """
    results = service.groups().patch(
        groupUniqueId=group_key,
        body=settings
    ).execute()

    return results