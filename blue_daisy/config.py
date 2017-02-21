import configparser
import os
import subprocess
from collections import OrderedDict

from pykeyboard import PyKeyboard


CONFIG_FILE = os.path.expanduser('~/.bluedaisy.conf')

DEFAULT_CONFIG = OrderedDict((
    ('general', OrderedDict((
        ('lock', 'key Super_L Shift_L X'),
        ('brightness_up', ''),
        ('brightness_down', ''),
        ('wifi_on', ''),
        ('wifi_off', ''),
    ))),
    ('media', OrderedDict((
        ('volume_up', ''),
        ('volume_down', ''),
        ('mute', ''),
        ('unmute', ''),
        ('pause', ''),
        ('next', ''),
        ('previous', ''),
    ))),
    ('presentation', OrderedDict((
        ('next', ''),
        ('previous', ''),
    ))),
))


class Config:

    def __init__(self):
        self.config = configparser.ConfigParser()

        if not os.path.isfile(CONFIG_FILE):
            self.config.read_dict(DEFAULT_CONFIG)
            self._write_config_file()
        else:
            self.config.read(CONFIG_FILE)

    def _write_config_file(self):
        with open(CONFIG_FILE, 'w') as config_file:
            self.config.write(config_file)

    def _press_key_command(self, keys):
        kb = PyKeyboard()

        if len(keys) == 1:
            kb.tap_key(keys[0])
        else:
            kb.press_keys(keys)

    def _run_shell_command(self, command):
        return_code = subprocess.run(command).returncode

        if return_code != 0:
            # inform user
            pass

    def execute_command(self, section, option):
        if self.config.has_option(section, option):
            value = self.config.get(section, option, fallback='').split(' ')
            if value[0] == 'key':
                self._press_key_command(value[1:])
            elif value[0] == 'shell':
                self._run_shell_command(value[1:])
            else:
                self._run_shell_command(value[1:])

    def add_command(self, section, option, command):
        try:
            self.config.set(section, option, command)
        except configparser.NoSectionError:
            self.config.add_section(section)
            self.config.set(section, option, command)

        self._write_config_file()

    def update_command(self, section, option, command):
        self.add_command(section, option, command)

    def remove_command(self, section, option):
        try:
            self.config.remove_option(section, option)
        except configparser.NoSectionError:
            pass

        self._write_config_file()
