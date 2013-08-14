#!/usr/bin/env python
import time
import logging
import ConfigParser
import os

from ui import UI
from usermanager import UserManager
from lazzor import Lazzor
import nupay
from decimal import Decimal

class LazzorManager(object):
    def __init__(self, config_file_path):
        config = ConfigParser.RawConfigParser()
        config.read(config_file_path)

        self._logger = logging.getLogger(__name__)
        self._ui = UI("lazzormanagement\nbooting...")

        user_config_file_path = os.path.dirname(config_file_path) + \
                os.path.sep + config.get('Users', 'users_file')
        self._user_manager = UserManager(user_config_file_path)
        self._lazzor = Lazzor()
 
        while True:
            try:
                self._upay_session_manager = nupay.SessionManager(config)
                break
            except nupay.SessionConnectionError as e:
                self._logger.warning("Can not reach the database")
                self._ui.warning_database_connection(timeout = 5)
            except nupay.TimeoutError as e:
                self._logger.warning("Timeout while connection to the database")
                self._ui.warning_database_connection(timeout = 5)

            self._ui.notify_try_again()


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
        try:
            with self._upay_session_manager.create_session() as session:
                session.validate_tokens(tokens, ui_update)
                self._ui.update_credit(session.credit)
                self._logger.info("Balance is %.02f Eur" % session.credit)
                self._ui.wait_for_ok()
                if session.credit > 0:
                    self._run_payment_loop(session)
        
        except nupay.SessionConnectionError as e:
            self._logger.warning("Databse connection could not be estalished")
            self._ui.warning_database_connection(timeout = 5)
        except nupay.TimeoutError:
            self._logger.warning("Databse connection timed out")
            self._ui.warning_database_connection(timeout = 5)

        self._lazzor.lock_laser()

    def _run_payment_loop(self, session):
        total_on_time = 0
        now_on_time = 0
        prev_on_time = 0

        paid_time = 0
        turn_on_timestamp = 0
        minute_cost = Decimal(0.5)
        sub_total = Decimal(0)

        self._ui.active_screen()

        self._lazzor.lock_laser()
        while self._token_reader.medium_valid:
            if total_on_time > paid_time:
                self._logger.info("Getting more money")
                try:
                    session.cash(minute_cost)
                    sub_total += minute_cost
                    paid_time += 60
                except nupay.NotEnoughCreditError:
                    self._lazzor.sound_alarm_tone()
                    self._logger.warning("Not enough credit available")
                    self._ui.warning_low_credit(timeout = 30)
                    self._lazzor.silence_alarm_tone()
                    break
                except nupay.TimeoutError:
                    self._logger.warning("Databse connection timed out")
                    self._lazzor.sound_alarm_tone()
                    self._ui.warning_database_connection(timeout = 30)
                    self._lazzor.silence_alarm_tone()
                    break

            if not self._lazzor.is_laser_unlocked and self._ui.is_turn_on_key_pressed:
                self._logger.info("Laser is locked, user wants to turn it on")
                self._lazzor.unlock_laser()
                turn_on_timestamp = time.time()
                sub_total = 0

            if self._lazzor.is_laser_unlocked:
                now_on_time = time.time() - turn_on_timestamp

            if self._lazzor.is_laser_unlocked and self._ui.is_turn_off_key_pressed:
                self._logger.info("Laser is unlocked, user wants to turn it off")
                self._lazzor.lock_laser()
                prev_on_time += now_on_time
                now_on_time = 0

            time.sleep(.1)
            total_on_time = now_on_time + prev_on_time
            self._ui.update_active_screen(now_on_time, total_on_time, sub_total, session.total, session.credit, self._lazzor.is_laser_unlocked)
    
        if not self._token_reader.medium_valid:
            self._logger.warning("Token medium vanished. Aborting.")

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

