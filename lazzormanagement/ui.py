import time
import logging

try:
    from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
    simulation = False
except ImportError:
    from adafruit_lcd_simulation import Adafruit_CharLCDPlate
    simulation = True

class UI:
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    SELECT = 5

    def __init__(self, greeter):
        self._logger = logging.getLogger(__name__)
        self._lcd = Adafruit_CharLCDPlate()
        self._cols = 16
        self._lcd.begin(self._cols, 2)
        self._lcd.clear()
        self._lcd.message(greeter)
        if simulation:
            self._logger.warning("Running in simulation mode")

    def _fill_line(self, line):
        return line + ' ' * (self._cols - len(line))

    def _wait_for_button(self):
        while self._lcd.buttons() == 0:
            time.sleep(0.05)
        buttons = self._lcd.buttons()
        while self._lcd.buttons() != 0:
            time.sleep(0.05)

        if buttons & (1 << self._lcd.RIGHT):
            return self.RIGHT
        if buttons & (1 << self._lcd.LEFT):
            return self.LEFT
        if buttons & (1 << self._lcd.UP):
            return self.UP
        if buttons & (1 << self._lcd.DOWN):
            return self.DOWN
        if buttons & (1 << self._lcd.SELECT):
            return self.SELECT

    def check_button_pressed(self):
        if self._lcd.buttons() != 0:
            return True
    
    def wait_for_buttons(self):
        while self._lcd.buttons() != 0:
            time.sleep(0.05)
    
    def wait_for_ok(self):
        while self._wait_for_button() != self.SELECT:
            pass

    def choose_option(self, optionname, options):
        self._logger.info("Waiting for option %s: %s", optionname, str(options))
        self._lcd.clear()
        self._lcd.message(optionname)
        index = 0
        while True:
            self._lcd.setCursor(0,1)
            option = options[index]
            self._lcd.message(self._fill_line(option))
            button = self._wait_for_button()

            if button == self.RIGHT:
                index += 1
            elif button == self.LEFT:
                index -= 1
            elif button == self.SELECT:
                self._logger.info("Option %s selected" % option)
                return option

            index = index % len(options)


    def choose_user(self, users):
        usernames = users.keys()
        self._logger.debug("Waiting for username selection")
        username = self.choose_option("Choose user:", usernames)
        return users[username]

    def get_passcode(self, username):
        self._logger.debug("Waiting for passcode")
        passcode = ''
        self._lcd.clear()
        self._lcd.message(username+':\nPasscode?')
        while True:
            button = self._wait_for_button()
            if button == self.RIGHT:
                passcode += 'r'
            elif button == self.LEFT:
                passcode += 'l'
            elif button == self.UP:
                passcode += 'u'
            elif button == self.DOWN:
                passcode += 'd'
            elif button == self.SELECT:
                self._logger.debug("Passcode %s entered" % passcode)
                return passcode

    def notify_bad_passcode(self, timeout):
        self._logger.info("Notifying bad passcode. Timeout=%d s", timeout)
        self._lcd.clear()
        self._lcd.message("Bad Passcode")
        while timeout > 0:
            self._lcd.setCursor(0,1)
            self._lcd.message(self._fill_line("%d"%timeout))
            time.sleep(1)
            timeout-=1

    def notify_inactive_user(self, username):
        self._logger.info("Notifying inactive user")
        self._lcd.clear()
        self._lcd.message(username+":\nAccount inactive")
        self._wait_for_button()
    
    def notify_credit(self):
        self._lcd.clear()
        self._lcd.message("Your credit:")

    def update_credit(self, credit):
        self._lcd.setCursor(0,1)
        self._lcd.message("%.02f Eur" % credit)

    def notify_waiting_for_usb(self):
        self._lcd.clear()
        self._lcd.message("Please insert\nUSB drive.")
 
    def active_screen(self):
        self._active_t0 = 0
        self._active_state = 0
        self._last_ui_element = None

    def update_active_screen(self, now_on_time, total_on_time, sub_total, total, credit):
        now_on_time = int(now_on_time)
        total_on_time = int(total_on_time)

        def format_as_time(seconds):
            minutes = int(seconds / 60)
            seconds = seconds % 60
            return "%d:%02d"%(minutes, seconds)
        
        def check_update_needed(ui_element):
            if self._last_ui_element != ui_element:
                self._last_ui_element = ui_element
                self._lcd.clear()
                return True
            return False

        if time.time() - self._active_t0 > 5:
            self._active_state += 1
            self._active_state %= 5
            self._active_t0 = time.time()
            self._last_ui_element = None

        if self._active_state == 0:
            if check_update_needed(now_on_time):
                self._lcd.message("On Time:\n" + format_as_time(now_on_time))
        elif self._active_state == 1:
            if check_update_needed(total_on_time):
                self._lcd.message("Total On Time:\n" + format_as_time(total_on_time))
        elif self._active_state == 2:
            if check_update_needed(sub_total):
                self._lcd.message("Sub Total:\n%.02f Eur" % sub_total)
        elif self._active_state == 3:
            if check_update_needed(total):
                self._lcd.message("Total:\n%.02f Eur" % total)
        elif self._active_state == 4:
            if check_update_needed(credit):
                self._lcd.message("Credit Left:\n%.02f Eur" % credit)

    @property
    def is_turn_on_key_pressed(self):
        return (self._lcd.buttons() & (1 << self._lcd.UP) > 0)
 
    @property
    def is_turn_off_key_pressed(self):
        return (self._lcd.buttons() & (1 << self._lcd.DOWN)) > 0

    def warning_database_connection(self):
        self._lcd.clear()
        self._lcd.message("Payment Database\nNot Responding")

#1234567890123456
#12:30 24:23
#05.50 17.00 99.
