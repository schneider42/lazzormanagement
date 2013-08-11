import time

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
        if not simulation:
            self._lcd = Adafruit_CharLCDPlate.Adafruit_CharLCDPlate()
            self._cols = 16
            self._lcd.begin(self._cols, 2)
            self._lcd.clear()
            self._lcd.message(greeter)

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

    def choose_option(self, optionname, options):
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
                    return option

                index = index % len(options)
        else:
            return options[0]


    def choose_user(self, users):
        usernames = users.keys()
        username = self.choose_option("Choose user:", usernames)
        return users[username]

    def get_passcode(self, username):
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
                    return passcode
        else:
            return "rlrl"

    def notify_bad_passcode(self, timeout):
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
        if not simulation:
            self._lcd.clear()
            self._lcd.message(username+":\nAccount inactive")

