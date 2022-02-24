from pathlib import Path
import configparser
from seeq.addons.udf_ui import backend
from seeq import spy

TEST_DIR = Path(__file__).resolve().parent
TEST_CONFIG_FILE = TEST_DIR.joinpath('test_config.ini')
DEFAULT_CREDENTIALS_PATH = TEST_DIR.joinpath('credentials.key')

if not Path(TEST_CONFIG_FILE).exists():
    raise FileNotFoundError(f"File {TEST_CONFIG_FILE} could not be found.")

config = configparser.ConfigParser(allow_no_value=True)
config.read(TEST_CONFIG_FILE)


def login(url=config['seeq']['seeq_url'], credentials_file=config['seeq']['credentials_file']):
    if not credentials_file:
        credentials_file = DEFAULT_CREDENTIALS_PATH if DEFAULT_CREDENTIALS_PATH.is_file() else \
            get_server_data_folder().joinpath('keys', 'agent.key')
    if isinstance(credentials_file, str):
        credentials_file = Path(credentials_file)
    if not credentials_file.is_file():
        raise FileNotFoundError(f'Could not find file {credentials_file} to get login credentials. '
                                f'Please provide a valid credentials_file path as argument or in test_config.ini. '
                                f'In the credentials_file, put your username in the first line, '
                                f'and password in the second line. '
                                f'You can also try passing the Seeq data directory as a "data_dir" kwarg')
    if not url:
        raise FileNotFoundError(f'Seeq url not provided. Please provide a url or add it in test_config.ini ')

    credentials = open(credentials_file, "r").read().splitlines()
    spy.login(credentials[0], credentials[1], url=url, ignore_ssl_errors=True)


def get_server_data_folder(data_dir=None):
    if data_dir is not None:
        return data_dir
    cwd = Path().absolute()
    return Path(cwd.drive).joinpath('/ProgramData', 'Seeq', 'data')


def admin_clean_up(package_names):
    """This function will not succeed for non-admin users and therefore some tests run by non-admin users will fail
    due to limitations on overwriting existing UDFs """
    if spy.user.is_admin:
        for package in package_names:
            backend.delete_udf_package(package_name=package, is_permanent=True)
