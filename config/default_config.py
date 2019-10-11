from pathlib import Path
from logging import INFO, ERROR

# Paths
path_working_directory = Path(__file__).parent.parent

path_credentials_directory = path_working_directory / 'credentials'
path_credentials_directory.mkdir(parents=True, exist_ok=True)

path_data_directory = path_working_directory / 'data'
path_data_directory.mkdir(parents=True, exist_ok=True)

path_logs_directory = path_working_directory / 'logs'
path_logs_directory.mkdir(parents=True, exist_ok=True)

# Google API
google_api_scopes = [
    'https://www.googleapis.com/auth/admin.directory.user',
    'https://www.googleapis.com/auth/admin.directory.group',
    'https://www.googleapis.com/auth/apps.groups.settings'
]

# Scenario: Sync Groups and Zulip
zulip_sync_logging_level = ERROR
zulip_sync_google_domain = ''
zulip_sync_mandatory_members = ['']
zulip_sync_sleep_time = 60 * 10

# Scenario: Create Google Groups
google_groups_logging_level = ERROR
google_groups_google_domain = ''
google_groups_user_filter_query = ''
