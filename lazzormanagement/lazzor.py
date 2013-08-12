try:
    import pifacedigitalio
    simulation = False
except ImportError:
    print(__name__ + ": Running in simulation mode")
    simulation = True

import logging

LASER_UNLOCK_PIN = 0
LASER_SWITCH_PIN = 0

class Lazzor:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        
        if not simulation:
            pifacedigitalio.init()
            self._io = pifacedigitalio.PiFaceDigital()
        self.lock_laser()

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
        if not self._simulation:
            return self._io.output_pins[LASER_UNLOCK_PIN].value == 1
        else:
            return self._laser_unlocked
