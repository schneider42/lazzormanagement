#!/usr/bin/env python
import lazzormanagement

class User(object):
    def __init__(self, username):
        self.username = username

ui = lazzormanagement.UI("lazzormanagement\nbooting...")

users = {"fpletz": User("fpletz"), "fnord": User("fnord")}
user = ui.choose_user(users)

passcode = ui.get_passcode(user.username)

if passcode != 'rlrl':
    ui.notify_bad_passcode(10)
else:
    ui.notify_inactive_user(user.username)
print(passcode)
