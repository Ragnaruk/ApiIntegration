import pickle
from time import sleep

import googleapiclient.errors
from transliterate import translit

from logs.logging import get_logger
from api_google.google_api_sheets import get_sheets_service, get_multiple_ranges
from api_google.google_api_directory import get_directory_service, get_users_for_domain, \
    get_groups_for_domain, create_group, add_user_to_group
from api_google.google_api_groupsettings import get_groupsettings_service, \
    get_group_settings, update_group_settings
from config.config import sync_sheets_and_groups, path_data_directory


def main():
    logger = get_logger('sync_sheets_and_groups', sync_sheets_and_groups['logging_level'])

    data_path = path_data_directory / 'sync_sheets_and_groups'
    data_path.mkdir(parents=True, exist_ok=True)

    synced_users_path = data_path / 'synced_users.pickle'

    while True:
        # number_of_registered_users = 0
        # synced_users_dictionary_creation = False
        #
        # # Getting a list of users who have already been synced
        # if synced_users_path.exists():
        #     logger.debug('Reading synced users from: %s', synced_users_path)
        #     with open(synced_users_path, 'rb') as f:
        #         synced_users = pickle.load(f)
        # else:
        #     logger.info('Creating synced users dictionary')
        #     synced_users = dict()
        #     synced_users_dictionary_creation = True

        try:
            service_directory = get_directory_service()
            service_sheets = get_sheets_service()

            # ranges = get_multiple_ranges(
            #     service_sheets,
            #     sync_sheets_and_groups['spreadsheet_id'],
            #     sync_sheets_and_groups['range_names']
            # )
            #
            # with open(data_path / 'ranges.pickle', 'wb') as file:
            #     pickle.dump(ranges, file)
            with open(data_path / 'ranges.pickle', 'rb') as file:
                ranges = pickle.load(file)
            #
            # [logger.debug(x) for x in ranges]

            # group_results = []
            # for group in ranges[0]['values']:
            #     group_name = group[0].split(" ", 1)[0]
            #
            #     email = (translit(group_name, "ru", reversed=True)).lower() \
            #             + "@" \
            #             + sync_sheets_and_groups['google_domain']
            #
            #     try:
            #         group_results.append(create_group(service_directory, email, group_name, ""))
            #     except googleapiclient.errors.HttpError as exception:
            #         # If group already exists among other things
            #         logger.error(exception, exc_info=False)
            #
            #     logger.debug(group_name, email)
            #
            # group_results.sort(key=lambda x: x['name'])

            # with open(data_path / 'group_results.pickle', 'wb') as file:
            #     pickle.dump(group_results, file)
            with open(data_path / 'group_results.pickle', 'rb') as file:
                group_results = pickle.load(file)
            #
            # [logger.debug(x) for x in group_results]

            created_group_names = [x['name'] for x in group_results]

            [logger.debug(x) for x in created_group_names]

            # # A client should wait 1 minute before adding users or sending messages to a new group
            # sleep(60)

            students = dict(zip(
                [i[0] if i else "" for i in ranges[1]['values']],
                [i[0] if i else "" for i in ranges[2]['values']]
            ))

            logger.debug(students.items())

            leaders = dict(zip(
                [i[0] if i else "" for i in ranges[3]['values']],
                [i[0] if i else "" for i in ranges[4]['values']]
            ))

            logger.debug(leaders.items())

            group_users = {}
            for group in ranges[0]['values']:
                id = group[0].split(" ", 1)[0]

                if id not in created_group_names:
                    logger.debug("Skipping group: ", id)
                    continue
                else:
                    logger.debug("Adding users to group: ", id)

                group_users[id] = []

                # Leader email
                group_users[id].append(
                    [leaders[group[1]], 'MEMBER']
                )

                # Member emails
                for i in range(2, len(group)):
                    group_users[id].append(
                        [students[group[i]], 'MEMBER']
                    )

                # Mandatory user
                group_users[id] += sync_sheets_and_groups['mandatory_members']

            with open(data_path / 'group_users.pickle', 'wb') as file:
                pickle.dump(group_users, file)
            with open(data_path / 'group_users.pickle', 'rb') as file:
                group_users = pickle.load(file)

            [logger.debug(x) for x in group_users]

            # # Add users to groups
            # user_results = []
            # for group in group_users:
            #     for group_user in group_users[group]:
            #         user_results.append(
            #             add_user_to_group(service, group, group_user[0], group_user[1])
            #         )
            #
            # with open(data_path / 'user_results.pickle', 'wb') as file:
            #     pickle.dump(user_results, file)
            # with open(data_path / 'user_results.pickle', 'rb') as file:
            #     user_results = pickle.load(file)
            #
            # [logger.debug(x) for x in user_results]

            # students = dict(zip(
            #     [i[0] if i else "" for i in ranges[1]['values']],
            #     [i[0] if i else "" for i in ranges[2]['values']]
            # ))
            #
            # leaders = dict(zip(
            #     [i[0] if i else "" for i in ranges[3]['values']],
            #     [i[0] if i else "" for i in ranges[4]['values']]
            # ))

            # if id not in synced_users:
            #     synced_users[id] = set()
            #
            # member_emails = set()
            #
            # # Leader email
            # member_emails.add(
            #     leaders[group[1]]
            # )
            #
            # # Member emails
            # for i in range(2, len(group)):
            #     member_emails.add(
            #         students[group[i]]
            #     )
            #
            # # Mandatory emails
            # member_emails |= set(sync_sheets_and_groups['mandatory_members'])
            #
            # # Synced users
            # member_emails -= synced_users[id]
            # synced_users[id] |= member_emails
            #
            # member_emails = list(member_emails)
            #
            # logger.debug('Name: %s - Description: %s - Users: %s',
            #              name, description, member_emails)
            #
            # if not synced_users_dictionary_creation:
            #     # TODO
            #     number_of_registered_users += len(member_emails)
            #
            #     logger.debug('Result: %s', result)

            # # -----
            # # Might need rework
            # # -----
            #
            # service = get_groupsettings_service()
            #
            # group_emails = []
            # for group_name in group_names:
            #     group_emails.append(
            #         (translit(group_name, "ru", reversed=True)).lower() \
            #                     + "@" \
            #                     + create_google_groups['google_domain']
            #     )
            #
            # with open(data_path / 'group_emails.pickle', 'wb') as file:
            #     pickle.dump(group_emails, file)
            # with open(data_path / 'group_emails.pickle', 'rb') as file:
            #     group_emails = pickle.load(file)
            #
            # [logger.debug(x) for x in group_emails]
            #
            # settings_results = []
            # for group_email in group_emails:
            #     settings_results.append(
            #         update_group_settings(
            #             service,
            #             group_email,
            #             {
            #                 "whoCanJoin": "INVITED_CAN_JOIN",
            #                 "whoCanViewMembership": "ALL_IN_DOMAIN_CAN_VIEW",
            #                 "whoCanViewGroup": "ALL_IN_DOMAIN_CAN_VIEW",
            #                 "whoCanPostMessage": "ALL_IN_DOMAIN_CAN_POST",
            #                 "isArchived": "true"
            #             }
            #         )
            #     )
            #
            # with open(data_path / 'settings_results.pickle', 'wb') as file:
            #     pickle.dump(settings_results, file)
            # with open(data_path / 'settings_results.pickle', 'rb') as file:
            #     settings_results = pickle.load(file)
            #
            # [logger.debug(x) for x in settings_results]
        except Exception as exception:
            logger.error(exception, exc_info=True)

        # logger.debug('Writing synced users to: %s', synced_users_path)
        # with open(synced_users_path, 'wb') as f:
        #     pickle.dump(synced_users, f)
        #
        # logger.info('Update finished. Registered %s users. Sleeping for %s seconds.',
        #             number_of_registered_users, sync_sheets_and_groups['sleep_time'])
        sleep(sync_sheets_and_groups['sleep_time'])


if __name__ == '__main__':
    main()
