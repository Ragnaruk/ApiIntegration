from pathlib import Path
from logging import ERROR, INFO, DEBUG

# Paths
path_working_directory = Path(__file__).parent.parent

path_credentials_directory = path_working_directory / 'credentials'
path_credentials_directory.mkdir(parents=True, exist_ok=True)

path_data_directory = path_working_directory / 'data'
path_data_directory.mkdir(parents=True, exist_ok=True)

path_logs_directory = path_working_directory / 'logs'
path_logs_directory.mkdir(parents=True, exist_ok=True)

# Scenario: Sync Groups and Zulip
sync_groups_and_zulip = {
    'logging_level': INFO,
    'google_domain': '',
    'mandatory_members': [],
    'sleep_time': 60 * 10
}

# Scenario: Create Google Groups
create_google_groups = {
    'logging_level': INFO,
    'google_domain': '',
    'user_filter_query': '',
    'mandatory_members': []
}

# Scenario: Get Users From Google
get_users_from_google = {
    'logging_level': INFO,
    'google_domain': '',
    'user_filter_query': ''
}

# Scenario: Sync Google Sheets and Zulip
sync_sheets_and_zulip = {
    'logging_level': INFO,
    'spreadsheet_id': '',
    'range_names': [],
    'mandatory_members': [],
    'sleep_time': 60 * 30
}

# Scenario: Sync Trello and Zulip
sync_trello_and_zulip = {
    'logging_level': INFO,
    'mandatory_members': [],
    'sleep_time': 60 * 10
}
