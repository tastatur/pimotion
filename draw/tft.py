__author__ = 'strah'
from cberry import cberry
import cv2
import ctypes
import Queue
import threading
import ConfigParser


class Tft:
    TFTW = 320
    TFTH = 240

    # Initialize C-Berry controller, use the same procedure, as in C example sources
    def __init__(self):
        cberry.bcm2835_init()
        cberry.TFT_init_board()
        cberry.TFT_hard_reset()
        cberry.RAIO_init()
        cberry.RAIO_clear_screen()
        config = ConfigParser.RawConfigParser()
        config.read('motion.properties')
        self.timeout = config.getint("Tft", "screensaver")
        self.on = True
        self.drawqueue = Queue.Queue()
        self.worker = threading.Thread(target=self.draw)
        self.worker.start()

    def draw(self):
        while True:
            try:
                picture = self.drawqueue.get(timeout=self.timeout)
                # The picture needs to be resize for the TFT display first
                picture = cv2.resize(picture, (self.TFTW, self.TFTH))
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