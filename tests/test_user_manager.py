import unittest
import mock
import tempfile
import io
import logging
import shutil
import ConfigParser
import os

from lazzormanagement import usermanager

class UserManagerTest(unittest.TestCase):

    def setUp(self):
        #logging.basicConfig(level=logging.DEBUG)
        logging.basicConfig(level=logging.ERROR)
        
        unused, self.users_config_path = tempfile.mkstemp()

        self.users_config = ConfigParser.RawConfigParser()
        self._usernames = []

        self.add_user_to_config(username="fpletz", role="admin", passcode="rlrl", active="True", bad_passcodes="0")
        self.add_user_to_config(username="bernd", role="user", passcode="udrl", active="True", bad_passcodes="2")
        self.add_user_to_config(username="fnord", role="user", passcode="udrl", active="False", bad_passcodes="0")

        with io.open(self.users_config_path, 'wb') as f:
            self.users_config.write(f)

        self.user_manager = usermanager.UserManager(self.users_config_path)

    def tearDown(self):
        os.remove(self.users_config_path)
    
    def add_user_to_config(self, username, role, passcode, active, bad_passcodes):
        self.users_config.add_section(username)
        self.users_config.set(username, "role", role)
        self.users_config.set(username, "passcode", passcode)
        self.users_config.set(username, "active", active)
        self.users_config.set(username, "bad_passcodes", bad_passcodes)
        self._usernames.append(username)

    def test_user_list(self):
        for username in self._usernames:
            self.assertTrue(username in self.user_manager.users.keys())
            self.assertIsInstance(self.user_manager.users[username], usermanager.User)

    def test_users_active(self):
        self.assertEqual(self.user_manager.users['fpletz'].active, True)
        self.assertEqual(self.user_manager.users['bernd'].active, True)
        self.assertEqual(self.user_manager.users['fnord'].active, False)
 
    def test_users_passcode(self):
        self.assertEqual(self.user_manager.users['fpletz'].passcode, "rlrl")
        self.assertEqual(self.user_manager.users['bernd'].passcode, "udrl")
        self.assertEqual(self.user_manager.users['fnord'].passcode, "udrl")
 
    def test_users_role(self):
        self.assertEqual(self.user_manager.users['fpletz'].role, usermanager.ADMIN)
        self.assertEqual(self.user_manager.users['bernd'].role, usermanager.USER)
        self.assertEqual(self.user_manager.users['fnord'].role, usermanager.USER)
 
    def test_users_bad_passcode(self):
        self.assertEqual(self.user_manager.users['fpletz'].bad_passcodes, 0)
        self.assertEqual(self.user_manager.users['bernd'].bad_passcodes, 2)
        self.assertEqual(self.user_manager.users['fnord'].bad_passcodes, 0)
    
    def test_bad_passcode(self):
        user = self.user_manager.users["bernd"]
        self.assertFalse(self.user_manager.check_passcode(user, 'uuuuu'))
        self.assertEqual(self.user_manager.users['bernd'].bad_passcodes, 3)
        self.assertEqual(self.user_manager.users['bernd'].timeout, 5)

    def test_bad_passcode(self):
        user = self.user_manager.users["bernd"]
        self.assertTrue(self.user_manager.check_passcode(user, 'udrl'))
        self.assertEqual(self.user_manager.users['bernd'].bad_passcodes, 0)
        self.assertEqual(self.user_manager.users['bernd'].timeout, 0)

if __name__ == '__main__':
    unittest.main()
