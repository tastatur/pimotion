import ConfigParser
import Queue
import cv2
import time


class Savedata:
    def __init__(self):
        config = ConfigParser.RawConfigParser()
        config.read('motion.properties')
        self.motionsdir = config.get("Data", "motionsdir")
        self.images = Queue.Queue()

    def save(self):
        while True:
            (binary, picture) = self.images.get()
            current_time = time.time()
            cv2.imwrite("{0}/{1}-binary.png".format(self.motionsdir, current_time), binary)
            cv2.imwrite("{0}/{1}.png".format(self.motionsdir, current_time), picture)

