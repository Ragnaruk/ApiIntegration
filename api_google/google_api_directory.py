"""
https://developers.google.com/admin-sdk/directory/v1/quickstart/python
https://developers.google.com/resources/api-libraries/documentation/admin/directory_v1/python/latest/index.html
https://developers.google.com/identity/protocols/googlescopes

https://developers.google.com/admin-sdk/directory/v1/guides/manage-group-members
"""
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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

    if os.path.exists(path_credentials_directory / 'token_directory.pickle'):
        with open(path_credentials_directory / 'token_directory.pickle', 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                path_credentials_directory / 'credentials.json',
                google_api_scopes)

            credentials = flow.run_local_server(port=0)

        with open(path_credentials_directory / 'token_directory.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    service = build('admin', 'directory_v1', credentials=credentials)

    return service


def get_groups_for_domain(service, domain):
    """
    Get all groups for a specified domain via Google API.

    :param service: Authenticated directory service object
    :param domain: The domain for groups
    :return: List of all groups
    """
    results = service.groups().list(domain=domain, maxResults=500).execute()

    groups = results.get('groups', [])

    while 'nextPageToken' in results:
        results = service.groups().list(domain=domain, maxResults=500,
                                        pageToken=results['nextPageToken']).execute()

        groups += results.get('groups', [])

    return groups


def get_members_for_group(service, group):
    """
    Get all members for a specified group via Google API.

    :param service: Authenticated directory service object
    :param group: The id for the group
    :return: List of all members
    """
    results = service.members().list(
        groupKey=group,
        maxResults=500
    ).execute()

    direct_members = results.get('members', [])

    while 'nextPageToken' in results:
        results = service.members().list(
            groupKey=group,
            maxResults=500,
            pageToken=results['nextPageToken']
        ).execute()

        direct_members += results.get('members', [])

    members = []

    for member in direct_members:
        if member['type'] == 'GROUP':
            members.extend(get_members_for_group(service, member['email']))
        else:
            members.append(member)

    return members


def get_users_for_domain(service, domain, query):
    """
    Get all users for a specified domain via Google API.

    :param service: Authenticated directory service object
    :param domain: The domain for users
    :return: List of all users
    """
    results = service.users().list(
        domain=domain,
        maxResults=500,
        query=query,
    ).execute()

    users = results.get('users', [])

    while 'nextPageToken' in results:
        results = service.users().list(
            domain=domain,
            maxResults=500,
            query=query,
            pageToken=results['nextPageToken']
        ).execute()

        users += results.get('users', [])

    return users


def create_group(service, email, name, description):
    """
    Create a Google Group via Google API.
    Groups created en masse might appear after 6-72 hours pass.

    :param service: Authenticated directory service object
    :param name: Name of the group
    :return: Results of the query
    """
    results = service.groups().insert(
        body={
            "kind": "admin#directory#group",
            "email": email,
            "name": name,
            "description": description,
        }
    ).execute()

    return results


def add_user_to_group(service, group_key, user_email, role):
    """
    Add user to a Google Group.

    :param service: Authenticated directory service object
    :param group_key: Unique identifier of the group (string, email, or id)
    :param user_email: Email of the user
    :param role: Role of the member
    :return: Results of the query
    """
    results = service.members().insert(
        groupKey=group_key,
        body={
            "email": user_email,
            "role": role
        }
    ).execute()

    return results


if __name__ == '__main__':
    get_directory_service()
