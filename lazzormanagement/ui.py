import time
import logging

try:
    import Adafruit_CharLCDPlate
    simulation = False
except ImportError:
    print(__name__ + ": Running in simulation mode")
    simulation = True

class UI:
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    SELECT = 5

    def __init__(self, greeter):
        self._logger = logging.getLogger(__name__)
        if not simulation:
            self._lcd = Adafruit_CharLCDPlate.Adafruit_CharLCDPlate()
            self._cols = 16
            self._lcd.begin(self._cols, 2)
            self._lcd.clear()
            self._lcd.message(greeter)
        else:
            self._logger.warning("Running in simulation mode")

    def _fill_line(self, line):
        return line + ' ' * (self._cols - len(line))

    def _wait_for_button(self):
        if not simulation:
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

        else:
            return self.LEFT

    def check_button_pressed(self):
        if not simulation:
            if self._lcd.buttons() != 0:
                return True
        return False
    
    def wait_for_buttons(self):
        if not simulation:
            while self._lcd.buttons() != 0:
                time.sleep(0.05)
    
    def wait_for_ok(self):
        while self._wait_for_button() != self.SELECT:
            pass

    def choose_option(self, optionname, options):
        self._logger.info("Waiting for option %s: %s", optionname, str(options))
        if not simulation:
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
        else:
            self._logger.info("Option %s selected" % options[0])
            return options[0]


    def choose_user(self, users):
        usernames = users.keys()
        self._logger.debug("Waiting for username selection")
        username = self.choose_option("Choose user:", usernames)
        return users[username]

    def get_passcode(self, username):
        self._logger.debug("Waiting for passcode")
        if not simulation:
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
        else:
            self._logger.debug("Passcode rlrl entered")
            return "rlrl"

    def notify_bad_passcode(self, timeout):
        self._logger.info("Notifying bad passcode. Timeout=%d s", timeout)
        if not simulation:
            self._lcd.clear()
            self._lcd.message("Bad Passcode")
            while timeout > 0:
                self._lcd.setCursor(0,1)
                self._lcd.message(self._fill_line("%d"%timeout))
                time.sleep(1)
                timeout-=1
        else:
            time.sleep(timeout)

    def notify_inactive_user(self, username):
        self._logger.info("Notifying inactive user")
        if not simulation:
            self._lcd.clear()
            self._lcd.message(username+":\nAccount inactive")
            self._wait_for_button()
    
    def notify_credit(self):
        if not simulation:
            self._lcd.clear()
            self._lcd.message("Your credit:")

    def update_credit(self, credit):
        if not simulation:
            self._lcd.setCursor(0,1)
            self._lcd.message("%.02f Eur" % credit)

    def notify_waiting_for_usb(self):
        if not simulation:
            self._lcd.clear()
            self._lcd.message("Please insert\nUSB drive.")
 
#    def active_screen(self):
#        if not simulation:
#            self._lcd.clear()
#            self._lcd.message

#1234567890123456
#12:30 24:23
#05.50 17.00 99.
