import pickle
from time import sleep

from logs.logging import get_logger
from api_google.google_auth import get_directory_service, get_groupsettings_service
from api_google.google_api import get_users_for_domain, get_groups_for_domain, \
    create_group, add_user_to_group, get_group_settings, update_group_settings
from config.config import google_groups_logging_level, path_data_directory, \
    google_groups_google_domain, google_groups_user_filter_query


def main():
    logger = get_logger('create_google_groups', google_groups_logging_level)

    try:
        service = get_directory_service()

        # Get all students in domain filtered by query
        users = get_users_for_domain(
            service,
            google_groups_google_domain,
            google_groups_user_filter_query
        )

        with open(path_data_directory / 'users.pickle', 'wb') as file:
            pickle.dump(users, file)
        with open(path_data_directory / 'users.pickle', 'rb') as file:
            users = pickle.load(file)

        # Get unique orgUnitPaths from users
        groups = set()
        for user in users:
            groups.add(user['orgUnitPath'])

        with open(path_data_directory / 'groups.pickle', 'wb') as file:
            pickle.dump(groups, file)
        with open(path_data_directory / 'groups.pickle', 'rb') as file:
            groups = pickle.load(file)

        [logger.debug(x) for x in groups]

        # Get group names from orgUnitPaths
        group_names = []
        for group in groups:
            group_names.append(group.split("/")[-1])

        # Filter out existing groups
        existing_groups = get_groups_for_domain(service, google_groups_google_domain)

        for group in existing_groups:
            if group['name'] in group_names:
                group_names.remove(group['name'])

        with open(path_data_directory / 'new_groups.pickle', 'wb') as file:
            pickle.dump(group_names, file)
        with open(path_data_directory / 'new_groups.pickle', 'rb') as file:
            group_names = pickle.load(file)

        [logger.debug(x) for x in group_names]

        # Create groups
        group_results = []
        for group_name in group_names:
            group_results.append(create_group(service, group_name, ""))

        group_results.sort(key=lambda x: x['name'])
        users.sort(key=lambda x: x['orgUnitPath'])

        # A client should wait 1 minute before adding users or sending messages to a new group
        sleep(60)

        with open(path_data_directory / 'group_results.pickle', 'wb') as file:
            pickle.dump(group_results, file)
        with open(path_data_directory / 'group_results.pickle', 'rb') as file:
            group_results = pickle.load(file)

        [logger.debug(x) for x in group_results]

        group_users = {}
        for group_result in group_results:
            group_users[group_result['email']] = []

            for user in users:
                if group_result['name'] in user['orgUnitPath']:
                    group_users[group_result['email']].append([user['primaryEmail'], 'MEMBER'])

            # Mandatory user
            group_users[group_result['email']].append(['support@miem.hse.ru', 'OWNER'])

        with open(path_data_directory / 'group_users.pickle', 'wb') as file:
            pickle.dump(group_users, file)
        with open(path_data_directory / 'group_users.pickle', 'rb') as file:
            group_users = pickle.load(file)

        [logger.debug(x) for x in group_users]

        # Add users to groups
        user_results = []
        for group in group_users:
            for group_user in group_users[group]:
                user_results.append(
                    add_user_to_group(service, group, group_user[0], group_user[1])
                )

        with open(path_data_directory / 'user_results.pickle', 'wb') as file:
            pickle.dump(user_results, file)
        with open(path_data_directory / 'user_results.pickle', 'rb') as file:
            user_results = pickle.load(file)

        [logger.debug(x) for x in user_results]

        # # -----
        # # Might need rework
        # # -----
        #
        # service = get_groupsettings_service()
        #
        # from transliterate import translit
        # group_emails = []
        # for group_name in group_names:
        #     group_emails.append(
        #         (translit(group_name, "ru", reversed=True)).lower() + "@miem.hse.ru"
        #     )
        #
        # with open(path_data_directory / 'group_emails.pickle', 'wb') as file:
        #     pickle.dump(group_emails, file)
        # with open(path_data_directory / 'group_emails.pickle', 'rb') as file:
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
        # with open(path_data_directory / 'settings_results.pickle', 'wb') as file:
        #     pickle.dump(settings_results, file)
        # with open(path_data_directory / 'settings_results.pickle', 'rb') as file:
        #     settings_results = pickle.load(file)
        #
        # [logger.debug(x) for x in settings_results]

    except Exception as exception:
        logger.error(exception)


if __name__ == '__main__':
    main()
