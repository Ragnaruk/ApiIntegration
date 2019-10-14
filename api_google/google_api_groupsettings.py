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