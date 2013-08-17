try:
    import pifacedigitalio
    simulation = False
except ImportError:
    print(__name__ + ": Running in simulation mode")
    simulation = True

import logging
import threading
import time

LASER_UNLOCK_PIN = 0
LASER_SWITCH_PIN = 0
ALARM_PIN = 1

class Lazzor:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        
        if not simulation:
            pifacedigitalio.init()
            self._io = pifacedigitalio.PiFaceDigital()
        self.lock_laser()
        
        self._sound_alarm = False
        self._alarmthread = threading.Thread(target=self._alarm_handler)
        self._alarmthread.setDaemon(True)
        self._alarmthread.start()

        self._consumption_timer = 0
        self._consumptionthread = threading.Thread(target=self._consumption_handler)
        self._consumptionthread.setDaemon(True)
        self._consumptionthread.start()

    def _alarm_handler(self):
        while True:
            if not simulation:
                if self._sound_alarm == True:
                    self._io.output_pins[ALARM_PIN].toggle()
                else:
                    self._io.output_pins[ALARM_PIN].turn_off()
            time.sleep(1)

    def _consumption_handler(self):
        while True:
            if not simulation:
                pass
            else:
                self._consumption_timer += .1
            time.sleep(.1)

    def lock_laser(self):
        self._logger.info("Locking the laser")
        if not simulation:
            self._io.output_pins[LASER_UNLOCK_PIN].turn_off()
        else:
            self._laser_unlocked = False

    def unlock_laser(self):
        self._logger.info("Unlocking the laser")
        if not simulation:
            self._io.output_pins[LASER_UNLOCK_PIN].turn_on()
        else:
            self._laser_unlocked = True

    @property
    def is_switch_turned_on(self):
        if not simulation:
            return self._io.input_pins[LASER_SWITCH_PIN].value == 1
        else:
            return False
    
    @property
    def is_laser_unlocked(self):
        if not simulation:
            return self._io.output_pins[LASER_UNLOCK_PIN].value == 1
        else:
            return self._laser_unlocked

    def sound_alarm_tone(self):
        self._logger.info("Sounding the alarm")
        self._sound_alarm = True

    def silence_alarm_tone(self):
        self._logger.info("Silencing the alarm")
        self._sound_alarm = False

    def reset_consumption_timer(self):
        self._consumption_timer = 0

    def get_consumption_timer(self):
        return self._consumption_timer
