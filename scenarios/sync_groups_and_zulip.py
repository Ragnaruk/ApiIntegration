from time import sleep

from logs.logging import get_logger
from api_google import google_auth
from api_google.google_api import get_groups_for_domain, get_members_for_group
from api_zulip.zulip_api import create_stream, get_all_users
from config.config import sync_groups_and_zulip, path_data_directory


def main():
    logger = get_logger('sync_groups_and_zulip', sync_groups_and_zulip['logging_level'])

    while True:
        try:
            service = google_auth.get_directory_service()

            # Get all groups of a domain
            groups = get_groups_for_domain(service, sync_groups_and_zulip['google_domain'])

            # Get all current Zulip users
            zulip_user_emails = set([member['email'] for member in get_all_users()['members']])

            # Get members of Google Groups and remove those who aren't registered in Zulip,
            # then create streams and invite remaining users.
            for group in groups:
                logger.debug('Group: %s', group)

                members = get_members_for_group(service, group['id'])
                member_emails = set([member['email'] for member in members])

                logger.debug('Group members\' emails: %s', member_emails)

                member_emails = list(member_emails & zulip_user_emails)
                member_emails += sync_groups_and_zulip['mandatory_members']

                logger.debug('Registered emails: %s', member_emails)

                result = create_stream(group['name'], group['description'], member_emails, True)

                logger.debug('Result: %s', result)
        except Exception as exception:
            logger.error(exception)

        logger.info('Update finished. Sleeping for %s seconds.', sync_groups_and_zulip['sleep_time'])
        sleep(sync_groups_and_zulip['sleep_time'])


if __name__ == '__main__':
    main()
