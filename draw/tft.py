__author__ = 'strah'
from cberry import cberry
import numpy
import cv2
import ctypes
import Queue
import threading


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
        self.drawqueue = Queue.Queue()
        self.worker = threading.Thread(target=self.draw)
        self.worker.start()

    def draw(self):
        while True:
            picture = self.drawqueue.get()
            # The picture needs to be resize for the TFT display first
            picture = cv2.resize(picture, (self.TFTW, self.TFTH))

            (blue, green, red) = cv2.split(picture)
            bmp = numpy.zeros(blue.shape, numpy.uint16)

            # We have 5 bits for red and blue, and 6 bits for green
            # See RA8770 datasheet for details
            blue = cv2.normalize(blue, alpha=0, beta=31, norm_type=cv2.NORM_MINMAX)
            green = cv2.normalize(green, alpha=0, beta=63, norm_type=cv2.NORM_MINMAX)
            red = cv2.normalize(red, alpha=0, beta=31, norm_type=cv2.NORM_MINMAX)
            for x, y in numpy.ndindex(blue.shape):
                bmp[x][y] = (red[x][y] << 11) + (green[x][y] << 5) + blue[x][y]

            cberry.RAIO_Write_Picture(bmp.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16)), bmp.shape[0] * bmp.shape[1])