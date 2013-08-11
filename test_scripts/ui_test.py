#!/usr/bin/env python
import lazzormanagement
import time

class User(object):
    def __init__(self, username, passcode, active):
        self.username = username
        self.passcode = passcode
        self.active = active

ui = lazzormanagement.UI("lazzormanagement\nbooting...")

users = {"fpletz": User("fpletz","rlrl",True), "fnord": User("fnord","udud",False)}
while True:
    while True:
        user = ui.choose_user(users)

        passcode = ui.get_passcode(user.username)

        if passcode != user.passcode:
            ui.notify_bad_passcode(10)
        elif user.active == False:
            ui.notify_inactive_user(user.username)
        else:
            break
    
