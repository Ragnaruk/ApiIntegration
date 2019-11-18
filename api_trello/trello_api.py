from trello import TrelloClient
import json

from config.config import path_credentials_directory


def get_client():
    """
    Authorize in Trello.

    :return: Authenticated client object.
    """
    with open(path_credentials_directory / "trello_credentials.json", "r") as file:
        creds = json.load(file)

    client = TrelloClient(
        api_key=creds["key"],
        api_secret=creds["token"]
    )

    return client


def get_boards_and_users(
        client: TrelloClient
):
    """
    Get list of all boards and users subscribed to them.

    :param client: A Trello client object
    :return: Results of request
    """
    boards = []

    all_boards = client.list_boards()
    print(all_boards[0].name)
    print(all_boards[0].description)

    all_members = all_boards[0].all_members()
    print(all_members[0].username)
    print(all_members[0].id)
    print(all_members[0].full_name)

    # for board in all_boards:
    #     boards.append(
    #         {
    #             "name": board.name,
    #             "description": board.description,
    #             "users": board.all_members()
    #         }
    #     )

