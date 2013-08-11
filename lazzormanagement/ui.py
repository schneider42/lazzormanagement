try:
    from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
    simulation = False
except ImportError:
    print(__name__ + ": Running in simulation mode")
    simulation = True

class UI:
    def __init__(self):
        pass
