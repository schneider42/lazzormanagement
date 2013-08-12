import ConfigParser
import io
import logging

ADMIN = "admin"
USER = "user"

class User(object):
    def __init__(self, config, name):
        self._username = name
        self._role = config.get(name, 'role')
        self._passcode = config.get(name, 'passcode')
        self._active = config.getboolean(name, 'active')
        self._bad_passcodes = config.getint(name, 'bad_passcodes')

    @property
    def username(self):
        return self._username

    @property
    def active(self):
        return self._active

    @property
    def passcode(self):
        return self._passcode

    @property
    def role(self):
        return self._role

    @property
    def bad_passcodes(self):
        return self._bad_passcodes

    @property
    def timeout(self):
        if self.bad_passcodes > 0:
            return 5
        return 0


class UserManager(object):
    def __init__(self, config):
        self._logger = logging.getLogger(__name__)
        self._users_config_path = config.get('Users', 'users_file')
        
        users_config = ConfigParser.RawConfigParser()
        users_config.read(self._users_config_path)
        
        self._users = {}
        for name in users_config.sections():
            self._users[name] = User(users_config, name)
    
    @property
    def users(self):
        return self._users

    def check_passcode(self, user, passcode):
        if user.passcode == passcode:
            user._bad_passcodes = 0
            self._logger.info("Passcode OK")
            return True

        self._logger.info("Passcode WRONG")
        user._bad_passcodes += 1
        return False

