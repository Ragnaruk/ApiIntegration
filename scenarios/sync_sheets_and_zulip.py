import pickle
from time import sleep

from logs.logging import get_logger
from api_google.google_api_sheets import get_sheets_service, get_muiltiple_ranges
from api_zulip.zulip_api import get_client, create_stream, get_all_users, get_all_streams
from config.config import sync_sheets_and_zulip, path_data_directory


def main():
    logger = get_logger('sync_sheets_and_zulip', sync_sheets_and_zulip['logging_level'])

    data_path = path_data_directory / 'sync_sheets_and_zulip'
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
            service = get_sheets_service()
            client = get_client()

            ranges = get_muiltiple_ranges(
                service,
                sync_sheets_and_zulip['spreadsheet_id'],
                sync_sheets_and_zulip['range_names']
            )

            # with open(data_path / 'ranges.pickle', 'wb') as file:
            #     pickle.dump(ranges, file)
            # with open(data_path / 'ranges.pickle', 'rb') as file:
            #     ranges = pickle.load(file)

            [logger.debug(x) for x in ranges]

            zulip_user_emails = set(
                [member['email'] for member in get_all_users(client)['members']]
            )
            zulip_stream_names = sorted(
                [stream['name'] for stream in get_all_streams(client)['streams']]
            )

            logger.debug(zulip_stream_names)

            for i in [0, 3]:
                for j in range(len(ranges[i]['values'])):
                    # If name and email of the leader both exist
                    if ranges[i + 0]['values'][j] and ranges[i + 2]['values'][j]:
                        id = ranges[i + 0]['values'][j][0]
                        description = ranges[i + 1]['values'][j][0] \
                            if ranges[i + 1]['values'][j] else ''
                        leader_email = ranges[i + 2]['values'][j][0]

                        if id not in synced_users:
                            synced_users[id] = set()

                        try:
                            name = get_current_stream_name(logger, zulip_stream_names, id)
                        except ValueError:
                            continue

                        # Add leader's email if they are registered in Zulip
                        member_emails = set()
                        if leader_email in zulip_user_emails:
                            member_emails.add(leader_email)

                        # Add mandatory members and substract already synced emails
                        member_emails |= set(sync_sheets_and_zulip['mandatory_members'])
                        member_emails -= synced_users[id]

                        # Update synced users
                        synced_users[id] |= member_emails

                        member_emails = list(member_emails)

                        logger.debug('Name: %s - Description: %s - Users: %s',
                                     name, description, member_emails)

                        if not synced_users_dictionary_creation:
                            result = create_stream(
                                client,
                                name,
                                description,
                                member_emails,
                                True
                            )
                            number_of_registered_users += len(member_emails)

                            logger.debug('Result: %s', result)
        except Exception as exception:
            logger.error(exception, exc_info=True)

        logger.debug('Writing synced users to: %s', synced_users_path)
        with open(synced_users_path, 'wb') as f:
            pickle.dump(synced_users, f)

        logger.info('Update finished. Registered %s users. Sleeping for %s seconds.',
                    number_of_registered_users, sync_sheets_and_zulip['sleep_time'])
        sleep(sync_sheets_and_zulip['sleep_time'])


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

        logger.debug('names_with_id: %s', names_with_id)

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


if __name__ == '__main__':
    main()
