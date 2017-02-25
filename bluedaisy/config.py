# -*- coding: utf-8 -*-
"""
bluedaisy.config
~~~~~~~~~~~~~~~~

This module provides the capability to create and read the
``~/.bluedaisy/bluedaisy.conf`` configuration file.

Attributes:
    CONFIG_FILE (str): A path to the ``~/.bluedaisy/bluedaisy.conf``
        configuration file.

    DEFAULT_CONFIG (dict): An ordered dict containing the default
        configurations to instantiate the configuration file if it does
        not exist.
"""

import configparser
import os
import subprocess
from collections import OrderedDict

from pykeyboard import PyKeyboard


CONFIG_FILE = os.path.expanduser('~/.bluedaisy/bluedaisy.conf')

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
    """Handle configurations set in the configuration file.

    This class contains methods necessary for handling the commands set in
    the configuration file.

    Attributes:
        config (configparser.ConfigParser): Handles the configuration file.
    """

    def __init__(self):
        """Config class constructor."""
        self.config = configparser.ConfigParser()

        if not os.path.isfile(CONFIG_FILE):
            self.config.read_dict(DEFAULT_CONFIG)
            self._write_config_file()
        else:
            self.config.read(CONFIG_FILE)

    def execute_command(self, section, option):
        """Retrieve a command from configuration file and execute it.

        Args:
            section (str): A name of a section present in the configuration
                file.

            option (str): A name of the option present under the section in
                the configuration file.
        """
        if self.config.has_option(section, option):
            value = self.config.get(section, option, fallback='').split(' ')

            # if command begins with 'key', call ``_press_key_command()``
            # else if command begins with 'shell' call ``_run_shell_command``
            if value[0] == 'key':
                self._press_key_command(value[1:])
            elif value[0] == 'shell':
                self._run_shell_command(value[1:])
            else:
                self._run_shell_command(value[1:])

    def add_command(self, section, option, command):
        """Insert a command in the cofiguration file.

        Args:
            section (str): A name of a section to insert the command in.

            option (str): A name of an option under the section to insert the
                command in.

            command (str): The command to be inserted in the provided
                [section][option].
        """
        try:
            self.config.set(section, option, command)
        except configparser.NoSectionError:
            self.config.add_section(section)
            self.config.set(section, option, command)

        self._write_config_file()

    def update_command(self, section, option, command):
        """Update a command in the cofiguration file.

        Args:
            section (str): A name of a section in the configuration file.

            option (str): A name of an option under the section in the
                configuration file.

            command (str): The command to replace the previous command in the
                provided [section][option].
        """
        self.add_command(section, option, command)

    def remove_command(self, section, option):
        """Remove a command in the configuration file.

        Args:
            section (str): A name of a section in the configuration file.

            option (str): A name of an option, under the section, whose
                command is to be removed.
        """
        try:
            self.config.remove_option(section, option)
            self._write_config_file()
        except configparser.NoSectionError:
            pass

    def _write_config_file(self):
        """Write configurations to the configuration file."""
        with open(CONFIG_FILE, 'w') as config_file:
            self.config.write(config_file)

    def _press_key_command(self, keys):
        """Press the keys specified.

        Args:
            keys (list(str)): A list containing names of keys to press.
        """
        kb = PyKeyboard()

        # tap key if there is only one key, else press keys
        if len(keys) == 1:
            kb.tap_key(keys[0])
        else:
            kb.press_keys(keys)

    def _run_shell_command(self, command):
        """Run the command specified.

        Args:
            command (str): A command to be executed.
        """
        return_code = subprocess.run(command).returncode

        if return_code != 0:
            # inform user
            pass
