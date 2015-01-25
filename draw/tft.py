__author__ = 'strah'
from cberry import cberry
import cv2
import ctypes
import Queue
import threading
import ConfigParser


class Tft:
    # Initialize C-Berry controller, use the same procedure, as in C example sources
    def __init__(self):
        config = ConfigParser.RawConfigParser()
        config.read('motion.properties')

        cberry.bcm2835_init()
        cberry.TFT_init_board()
        cberry.TFT_hard_reset()
        cberry.RAIO_init()
        cberry.RAIO_clear_screen()
        cberry.RAIO_SetBacklightPWMValue(config.getint("Tft", "backlight"))

        self.timeout = config.getint("Tft", "screensaver")
        self.on = True
        self.drawqueue = Queue.Queue()
        self.worker = threading.Thread(target=self.draw)
        self.worker.start()

    def draw(self):
        while True:
            try:
                picture = self.drawqueue.get(timeout=self.timeout)
                bmp = cv2.cvtColor(picture, cv2.COLOR_BGR2BGR565, dstCn=1)
                if not self.on:
                    self.stop_screensaver()
                cberry.RAIO_Write_Picture(bmp.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16)), bmp.shape[0] * bmp.shape[1])
            except Queue.Empty:
                if self.on:
                    self.screensaver()

    def screensaver(self):
        cberry.RAIO_power_off()
        self.on = False

    def stop_screensaver(self):
        cberry.RAIO_power_on()
        self.on = True