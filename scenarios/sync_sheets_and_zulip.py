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
                        id = name = ranges[i + 0]['values'][j][0]
                        description = \
                            ranges[i + 1]['values'][j][0] if ranges[i + 1]['values'][j] else ''
                        leader_email = ranges[i + 2]['values'][j][0]

                        if id not in synced_users:
                            synced_users[id] = set()

                        # Checking for renamed streams (streams that start with value of name)
                        similar_stream_names = [x for x in zulip_stream_names if x.startswith(name)]

                        logger.debug('similar_stream_names: %s', similar_stream_names)

                        if len(similar_stream_names) > 1:
                            more_similar_stream_names = \
                                [x for x in similar_stream_names if x.startswith(name + ' ')]

                            logger.debug('more_similar_stream_names: %s', more_similar_stream_names)

                            if len(more_similar_stream_names) == 1:
                                name = more_similar_stream_names[0]
                            else:
                                logger.error('Several streams starting with: %s', name)
                                logger.error('Without space: %s', similar_stream_names)
                                logger.error('With space: %s', more_similar_stream_names)
                        elif len(similar_stream_names) == 1:
                            name = similar_stream_names[0]

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

                        logger.debug('Name, Description, Users: %s, %s, %s',
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


if __name__ == '__main__':
    main()
