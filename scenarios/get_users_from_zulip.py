import pickle
import csv

from logs.logging import get_logger
from api_zulip.zulip_api import get_client, get_all_users
from config.config import get_users_from_zulip, path_data_directory


def main():
    logger = get_logger('get_users_from_zulip', get_users_from_zulip['logging_level'])

    data_path = path_data_directory / 'get_users_from_zulip'
    data_path.mkdir(parents=True, exist_ok=True)

    try:
        # client = get_client()
        #
        # users = get_all_users(client)['members']
        # users.sort(key=lambda x: x['user_id'])
        #
        # with open(data_path / 'users.pickle', 'wb') as file:
        #     pickle.dump(users, file)
        with open(data_path / 'users.pickle', 'rb') as file:
            users = pickle.load(file)

        [logger.debug(x) for x in users]

        with open(data_path / 'users.csv', 'w', newline='') as csvfile:
            fieldnames = [
                'avatar_url', 'is_admin', 'full_name', 'is_guest', 'bot_type', 'is_bot', 'email',
                'is_active', 'bot_owner', 'user_id'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for u in users:
                writer.writerow(u)

    except Exception as exception:
        logger.error(exception, exc_info=True)


if __name__ == '__main__':
    main()
