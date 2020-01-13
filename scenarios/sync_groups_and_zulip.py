import pickle
from time import sleep

from logs.logging import get_logger
from api_google.google_api_directory import get_directory_service, \
    get_groups_for_domain, get_members_for_group
from api_zulip.zulip_api import get_client, get_client_user, create_stream, get_all_users, \
    get_all_streams, create_user_group
from config.config import sync_groups_and_zulip, path_data_directory


def main():
    logger = get_logger('sync_groups_and_zulip', sync_groups_and_zulip['logging_level'])

    data_path = path_data_directory / 'sync_groups_and_zulip'
    data_path.mkdir(parents=True, exist_ok=True)

    synced_users_path = data_path / 'synced_users.pickle'

    while True:
        number_of_registered_users = 0
        synced_users_dictionary_creation = False

        # Getting a list of users who have already been synced
        if synced_users_path.exists():
            logger.debug('Reading synced users from: %s', synced_users_path)
            with open(synced_users_path, 'rb') as f:
                synced_users = pickle.load(f)
        else:
            logger.info('Creating synced users dictionary')
            synced_users = dict()
            synced_users_dictionary_creation = True

        try:
            service = get_directory_service()
            client = get_client()
            client_user = get_client_user()

            # Get all Google groups of a domain
            groups = get_groups_for_domain(service, sync_groups_and_zulip['google_domain'])

            # Get all current Zulip users
            zulip_users = get_all_users(client)['members']
            zulip_user_emails = set(
                [member['email'] for member in zulip_users]
            )

            zulip_stream_names = sorted(
                [stream['name'] for stream in get_all_streams(client)['streams']]
            )

            # Get members of Google Groups and remove those who aren't registered in Zulip,
            # then create streams and invite remaining users.
            for group in groups:
                logger.debug('Group: %s', group)

                name = get_current_stream_name(logger, zulip_stream_names, group['name'])

                # Create a set for the group if it doesn't exist yet
                if group['email'] not in synced_users:
                    synced_users[group['email']] = set()

                members = get_members_for_group(service, group['id'])
                member_emails = set([member['email'] for member in members])

                # Get emails only of those who are registered in Zulip
                # plus mandatory members'
                # minus users' who have already been subscribed
                member_emails &= zulip_user_emails
                member_emails |= set(sync_groups_and_zulip['mandatory_members'])
                member_emails -= synced_users[group['email']]

                # Update synced users set
                synced_users[group['email']] |= member_emails

                member_emails = list(member_emails)

                logger.debug('Emails to register: %s', member_emails)

                if member_emails and not synced_users_dictionary_creation:
                    # Creating or updating a stream
                    result = create_stream(
                        client,
                        name,
                        group['description'],
                        member_emails,
                        False
                    )

                    # Update a user group
                    update_user_group(logger, client_user, zulip_users, group['name'],
                                      group['description'], member_emails)

                    number_of_registered_users += len(member_emails)

                    logger.debug('Result: %s', result)
        except Exception as exception:
            logger.error(exception, exc_info=True)

        logger.debug('Writing synced users to: %s', synced_users_path)
        with open(synced_users_path, 'wb') as f:
            pickle.dump(synced_users, f)

        logger.info('Update finished. Registered %s users. Sleeping for %s seconds.',
                    number_of_registered_users, sync_groups_and_zulip['sleep_time'])
        sleep(sync_groups_and_zulip['sleep_time'])


def get_current_stream_name(logger, zulip_stream_names, stream_id):
    """
    Check all Zulip streams and get a name for the current stream.
    Raise ValueError if it is impossible to narrow down stream names.

    :param logger: Logger object
    :param zulip_stream_names: List of Zulip stream names
    :param stream_id: ID of the stream (default name)
    :return: Name of the current stream
    """
    name = stream_id

    if stream_id not in zulip_stream_names:
        names_with_id = [x for x in zulip_stream_names if x.startswith(stream_id)]

        logger.debug('Stream names with id: %s', names_with_id)

        if not names_with_id:
            pass
        elif len(names_with_id) == 1:
            name = names_with_id[0]
        elif len(names_with_id) > 1:
            names_with_id_and_space = [x for x in names_with_id if x.startswith(stream_id + ' ')]

            logger.debug('names_with_id_and_space: %s', names_with_id_and_space)

            if len(names_with_id_and_space) == 1:
                name = names_with_id_and_space[0]
            else:
                logger.error('Several streams starting with: %s', stream_id)
                logger.error('Without space: %s', names_with_id)
                logger.error('With space: %s', names_with_id_and_space)

                raise ValueError

    return name


def update_user_group(logger, client_user, zulip_users, name, description, member_emails):
    """
    Update a Zulip user group.

    :param logger: Logger object
    :param client_user: Authenticated client object
    :param zulip_users: All Zulip users
    :param name: Name of the group
    :param description: Description of the group
    :param member_emails: Emails of members of the group
    :return: ...
    """
    member_ids = []

    for user in zulip_users:
        if user['email'] in member_emails:
            member_ids.append(user['user_id'])

    logger.debug('Member ids: %s', member_ids)

    create_user_group(client_user, name, description, member_ids)


if __name__ == '__main__':
    main()
