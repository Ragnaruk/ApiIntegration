import zulip

from config.config import path_credentials_directory


def get_client():
    """
    Authorize in Zulip.

    :return: Authenticated client object
    """
    client = zulip.Client(config_file=path_credentials_directory / 'zuliprc.txt')

    return client


def get_client_user():
    """
    Authorize in Zulip.

    :return: Authenticated client object
    """
    client = zulip.Client(config_file=path_credentials_directory / 'zuliprc_user.txt')

    return client


def create_stream(client, name, description, member_emails, invite_only):
    """
    Create a stream in Zulip and invite users to it.

    :param client: A Zulip client object
    :param name: Name of the stream
    :param description: Description of the stream
    :param member_emails: List of emails of all users to be invited
    :param invite_only: Option to make the stream invite only
    :return: Result of request
    """
    result = client.add_subscriptions(
        streams=[
            {
                'name': name,
                'description': description
            }
        ],
        principals=member_emails,
        invite_only=invite_only,
    )

    return result


def get_all_users(client):
    """
    Get all current Zulip users.

    :param client: A Zulip client object
    :return: Dictionary containing all current users.
    """
    result = client.get_members()

    return result


def get_all_streams(client):
    """
    Get all current Zulip streams.

    :param client: A Zulip client object
    :return: Dictionary containing all current streams.
    """
    result = client.get_streams()

    return result


def get_user_groups(client):
    """
    Get all current Zulip user groups.

    :param client: A Zulip client object
    :return: Dictionary containing all current groups.
    """
    result = client.get_user_groups()

    return result


def create_user_group(client, name, description, members):
    """
    Create Zulip user group.

    :param client: A Zulip client object
    :param name: Name of the group
    :param description: Description of the group
    :param members: List of ids of group members
    :return: Dictionary containing all current streams.
    """
    current_groups = client.get_user_groups()
    group_id = None

    if 'user_groups' in current_groups.keys():
        for group in current_groups['user_groups']:
            if group['name'] == name:
                group_id = group['id']

    if group_id:
        client.remove_user_group(group_id)

    request = {
        'name': name,
        'description': description,
        'members': members,
    }

    result = client.create_user_group(request)

    return result
