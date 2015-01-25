import picamera
import picamera.array
import tft


class Recordvideo:
    TFTW = 320
    TFTH = 240

    def __init__(self, camera):
        self.imgsize = (self.TFTW, self.TFTH)
        self.camera = camera
        self.tft = tft.Tft()

    def draw(self):
        with picamera.array.PiRGBArray(self.camera, size=self.imgsize) as image:
            for frame in self.camera.capture_continuous(image, format('bgr'), use_video_port=True, resize=self.imgsize,
                                                        splitter_port=2):

                self.tft.drawqueue.put_nowait(image.array)
                image.seek(0)
                image.truncate()