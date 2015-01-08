import Queue
import cv2
import time
import ConfigParser


class SimpleDiffAnalyze:
    QUEUE_TIMEOUT = 2
    KERNEL_SIZE = (3, 3)
    THRESHOLD = 32
    MIN_MEAN = 5
    MAX_STDDEV = 100

    def __init__(self):
        self.frames = Queue.Queue()
        config = ConfigParser.RawConfigParser()
        config.read('motion.properties')
        self.motionsdir = config.get("SimpleDiff", "motionsdir")

    def prepare_image(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.GaussianBlur(gray_image, self.KERNEL_SIZE, 0)

    def calculate_threshold(self):
        diff_previous = cv2.absdiff(self.previous_frame_blurred, self.next_frame_blurred)
        diff_current = cv2.absdiff(self.current_frame_blurred, self.next_frame_blurred)
        conjunction = cv2.bitwise_and(diff_previous, diff_current)
        return cv2.threshold(conjunction, self.THRESHOLD, 255, cv2.THRESH_BINARY)[1]

    # noinspection PyAttributeOutsideInit
    def process(self):
        while True:
            self.previous_frame = self.frames.get(timeout=self.QUEUE_TIMEOUT)
            self.current_frame = self.frames.get(timeout=self.QUEUE_TIMEOUT)
            self.next_frame = self.frames.get(timeout=self.QUEUE_TIMEOUT)

            self.previous_frame_blurred = self.prepare_image(self.previous_frame)
            self.current_frame_blurred = self.prepare_image(self.current_frame)
            self.next_frame_blurred = self.prepare_image(self.next_frame)

            binary_result = self.calculate_threshold()
            (mean, stddev) = cv2.meanStdDev(binary_result)
            print "Mean: {0}, Std dev:{1}".format(mean[0][0], stddev[0][0])
            if mean[0][0] > self.MIN_MEAN and stddev[0][0] < self.MAX_STDDEV:
                cv2.imwrite("{0}/{1}.png".format(self.motionsdir, time.time()), binary_result)
