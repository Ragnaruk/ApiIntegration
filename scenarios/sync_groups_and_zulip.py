import pickle
from time import sleep

from logs.logging import get_logger
from api_google import google_auth
from api_google.google_api_directory import get_groups_for_domain, get_members_for_group
from api_zulip.zulip_api import create_stream, get_all_users
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
            service = google_auth.get_directory_service()

            # Get all Google groups of a domain
            groups = get_groups_for_domain(service, sync_groups_and_zulip['google_domain'])

            # Get all current Zulip users
            zulip_user_emails = set([member['email'] for member in get_all_users()['members']])

            # Get members of Google Groups and remove those who aren't registered in Zulip,
            # then create streams and invite remaining users.
            for group in groups:
                logger.debug('Group: %s', group)

                # Create a set for the group if it doesn't exist yet
                if group['email'] not in synced_users:
                    synced_users[group['email']] = set()

                members = get_members_for_group(service, group['id'])
                member_emails = set([member['email'] for member in members])

                logger.debug('Group members\' emails: %s', member_emails)

                # Get emails only of those who are registered in Zulip
                # plus mandatory members'
                # minus users' who have already been subscribed
                member_emails = \
                    (member_emails & zulip_user_emails
                     | set(sync_groups_and_zulip['mandatory_members'])
                     ) - synced_users[group['email']]

                # Update synced users set
                synced_users[group['email']] |= member_emails

                member_emails = list(member_emails)

                logger.debug('Emails to register: %s', member_emails)

                if not synced_users_dictionary_creation:
                    result = create_stream(group['name'], group['description'], member_emails, True)
                    number_of_registered_users += len(member_emails)

                    logger.debug('Result: %s', result)
        except Exception as exception:
            logger.error(exception)

        logger.debug('Writing synced users to: %s', synced_users_path)
        with open(synced_users_path, 'wb') as f:
            pickle.dump(synced_users, f)

        logger.info('Update finished. Registered %s users. Sleeping for %s seconds.',
                    number_of_registered_users, sync_groups_and_zulip['sleep_time'])
        sleep(sync_groups_and_zulip['sleep_time'])


if __name__ == '__main__':
    main()
