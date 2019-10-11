import zulip

from config.config import path_credentials_directory


def get_client():
    """
    Authorize in Zulip.

    :return: Authenticated client object.
    """
    client = zulip.Client(config_file=path_credentials_directory / 'zuliprc.txt')

    return client


def create_stream(name, description, member_emails):
    """
    Create a stream in Zulip and invite users to it.

    :param name: Name of the stream.
    :param description: Description of the stream.
    :param member_emails: Emails of all users to be invited.
    :return: Result of request.
    """
    client = get_client()

    result = client.add_subscriptions(
        streams=[
            {
                'name': name,
                'description': description
            }
        ],
        principals=member_emails,
        invite_only=True,
    )

    return result


def get_all_users():
    """
    Get all currect Zulip users.

    :return: Dictionary containing all current users.
    """
    client = get_client()

    result = client.get_members()

    return result
