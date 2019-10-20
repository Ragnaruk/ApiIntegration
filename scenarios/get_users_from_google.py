import pickle
import json

from logs.logging import get_logger
from api_google.google_api_directory import get_directory_service, get_users_for_domain
from config.config import get_users_from_google, path_data_directory


def main():
    logger = get_logger('get_users_from_google', get_users_from_google['logging_level'])

    data_path = path_data_directory / 'get_users_from_google'
    data_path.mkdir(parents=True, exist_ok=True)

    try:
        service = get_directory_service()

        # Get all students in domain filtered by query
        users = get_users_for_domain(
            service,
            get_users_from_google['google_domain'],
            get_users_from_google['user_filter_query']
        )

        with open(data_path / 'users.pickle', 'wb') as file:
            pickle.dump(users, file)
        with open(data_path / 'users.pickle', 'rb') as file:
            users = pickle.load(file)

        [logger.debug(x) for x in users]

        # Get unique orgUnitPaths from users
        groups = set()
        for user in users:
            groups.add(user['orgUnitPath'])

        with open(data_path / 'groups.pickle', 'wb') as file:
            pickle.dump(groups, file)
        with open(data_path / 'groups.pickle', 'rb') as file:
            groups = pickle.load(file)

        [logger.debug(x) for x in groups]

        with open(data_path / 'users.txt', 'w') as file:
            for group in groups:
                print(group + ':', file=file)
                for user in [x for x in users if x['orgUnitPath'] == group]:
                    print('    ' + json.dumps(user['primaryEmail']), file=file)
    except Exception as exception:
        logger.error(exception, exc_info=True)


if __name__ == '__main__':
    main()
