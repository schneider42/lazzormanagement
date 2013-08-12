#!/usr/bin/env python
import time
import logging

from ui import UI
from usermanager import UserManager
from lazzor import Lazzor
import nupay

class LazzorManager(object):
    def __init__(self, config):
        self._logger = logging.getLogger(__name__)
        self._ui = UI("lazzormanagement\nbooting...")
        self._user_manager = UserManager(config)
        self._lazzor = Lazzor()
 
        while True:
            try:
                self._upay_session_manager = nupay.SessionManager(config)
                break
            except:
                continue

        self._token_reader = nupay.USBTokenReader()

    def _login(self):
        while True:
            user = self._ui.choose_user(self._user_manager.users)

            passcode = self._ui.get_passcode(user.username)
            
            passcode_ok = self._user_manager.check_passcode(user, passcode)

            if passcode_ok == False:
                self._ui.notify_bad_passcode(user.timeout)
            elif user.active == False:
                self._ui.notify_inactive_user(user.username)
            else:
                self._logger.debug("Leaving user selection mode")
                return user
    
    def _activate_laser(self, user):

        def ui_update(session):
            if session.credit % 5 == 0:
                self._ui.update_credit(session.credit)

        self._logger.info("Waiting for USB stick with purse")
        self._ui.notify_waiting_for_usb()
        
        while True: 
            try:
                tokens = self._token_reader.read_tokens()
                break
            except nupay.NoTokensAvailableError:
                if self._ui.check_button_pressed():
                    self._ui.wait_for_buttons()
                    return
                time.sleep(1)

        self._logger.info("Read %d tokens"%len(tokens))
        self._ui.notify_credit()

        with self._upay_session_manager.create_session() as session:
            session.validate_tokens(tokens, ui_update)
            self._ui.update_credit(session.credit)
            self._logger.info("Balance is %.02f Eur" % session.credit)
            self._ui.wait_for_ok()

            total_on_time = 0
            now_on_time = 0
            prev_on_time = 0

            paid_time = 0
            turn_on_timestamp = 0
            #minute_cost = Decimal(0.5)
            
            #self._ui.active_screen()

            #while self._token_reader.medium_valid:
            #    if total_on_time > paid_time:
            #        try:
            #            session.cash(price)
            #            paid_time += 60
            #        except nupay.NotEnoughCreditError:
            #            break
            #    if not self._lazzor.is_laser_unlocked and self._lazzor.is_switch_turned_on():
            #        self._lazzor.unlock_laser()
            #        turn_on_timestamp = time.time()

            #    if self._lazzor.is_laser_unlocked:
            #        now_on_time = time.time() - turn_on_timestamp

            #    if self._lazzor.is_laser_unlocked and self._lazzor.is_switch_turned_on():
            #        self._lazzor.lock_laser()
            #        prev_on_time += now_on_time
            #        now_on_time = 0

            #    time.sleep(1)
            #    total_on_time = now_on_time + prev_on_time

        #self._logger.info("Waiting for medium to vanish")
    def _change_passcode(self, user):
        pass

    def run(self):
        while True:
            user = self._login()
            while True:
                options = ["Activate Laser", "Logout", "Change Passcode"]

                option = self._ui.choose_option("Action:", options)
                if option == "Logout":
                    break
                if option == "Activate Laser":
                    self._activate_laser(user)
                if option == "Change Passcode":
                    self._change_passcode(user)
