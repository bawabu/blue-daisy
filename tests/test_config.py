from unittest import TestCase
from unittest.mock import patch, mock_open

from bluedaisy import config


class TestConfig(TestCase):

    @patch('bluedaisy.config.os.path.isfile')
    def test_config_init_without_file(self, is_conf_file):
        is_conf_file.return_value = False
        m = mock_open()
        with patch('bluedaisy.config.open', m):
            c = config.Config()

        m.assert_called_once_with(config.CONFIG_FILE, 'w')
        assert c.config.has_section('general')

    @patch('bluedaisy.config.os.path.isfile')
    def test_config_init_with_file(self, is_conf_file):
        is_conf_file.return_value = True
        m = mock_open(read_data=config.DEFAULT_CONFIG)
        with patch('bluedaisy.config.configparser.open', m):
            config.Config()

        m.assert_called_once_with(config.CONFIG_FILE, encoding=None)
