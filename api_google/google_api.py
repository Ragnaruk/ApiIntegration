"""
https://developers.google.com/admin-sdk/directory/v1/quickstart/python
https://developers.google.com/resources/api-libraries/documentation/admin/directory_v1/python/latest/index.html
https://developers.google.com/identity/protocols/googlescopes

https://developers.google.com/admin-sdk/groups-settings/v1/reference/groups
https://developers.google.com/admin-sdk/directory/v1/guides/manage-group-members
"""
from transliterate import translit


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

    members = results.get('members', [])

    while 'nextPageToken' in results:
        results = service.members().list(
            groupKey=group,
            maxResults=500,
            pageToken=results['nextPageToken']
        ).execute()

        members += results.get('members', [])

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


def create_group(service, name, description):
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
            "email": (translit(name, "ru", reversed=True)).lower() + "@miem.hse.ru",
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
