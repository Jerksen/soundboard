import logging
from RPi import GPIO
GPIO.setmode(GPIO.BOARD)
logging.info('loading dicetower.buttons')
import sys
import time

class ButtonException(Exception):
    pass

class Button(object):
    """
    this class represents a single button. it is a pretty simple wrapper class
    """
    VALID_PINS = [7, 8, 10, 11, 12, 13, 15, 16, 17, 19, 20, 21, 22, 23, 24, 26]
    def __init__(self, btn_id):
        logging.debug("Creating button on pin {}".format(btn_id))
        self.has_event = False
        self.btn_id = btn_id

        if self.btn_id not in self.VALID_PINS:
            raise ButtonException("Pin #{} is not a valid pin".format(self.btn_id))
        
        GPIO.setup(btn_id, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def setup_event(self, callback, bouncetime=200, press=True, release=False):
        """
        sets up an event handler for the button
        callback is a function to call when the event occurs
        bouncetime is the software debounce
        falling and raising indicate which event types will trigger the event
        """
        if self.has_event:
            self.remove_event()
        GPIO.add_event_detect(self.btn_id,
                              self.get_edge_type(press, release),
                              callback=callback,
                              bouncetime=bouncetime)
        self.has_event = True

    def remove_event(self):
        """
        remove the event handler from the button
        """
        if (self.has_event):
            GPIO.remove_event_detect(self.btn_id)
        self.has_event = False

    def wait_for_event(self, press=False, release=True, timeout=None):
        """
        for debug only, wait for an event
        """
        return GPIO.wait_for_edge(self.btn_id,
                                  self.get_edge_type(press, release),
                                  timeout=timeout)
    
    def get_edge_type(self, press, release):
        """
        using the press and release bools, get an edge type
        """
        edge_type = None

        if press and release:
            edge_type = GPIO.BOTH
        elif press:
            edge_type = GPIO.FALLING
        elif release:
            edge_type = GPIO.RAISING
        else:
            logging.info("you putz, you didn't select an edge")

        return edge_type


def test_print(x):
    print("button pressed")
if __name__ == "__main__":
    b = Button(int(sys.argv[1]))
    b.setup_event(test_print)
    count = 30
    while count > 0:
        time.sleep(1)
        count -= 1

