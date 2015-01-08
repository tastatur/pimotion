import picamera
import picamera.array
import threading
import analyze.simplediff
import ConfigParser

analyzer = analyze.simplediff.SimpleDiffAnalyze()
worker = threading.Thread(target=analyzer.process)
worker.start()

with picamera.PiCamera() as camera:
    config = ConfigParser.RawConfigParser()
    config.read('motion.properties')

    camera_width = config.getint("Camera", "realwidth")
    camera_height = config.getint("Camera", "realheight")
    camera_fps = config.getint("Camera", "fps")
    scaled_width = config.getint("Camera", "scaledwidth")
    scaled_height = config.getint("Camera", "scaledheight")
    scale = (scaled_width, scaled_height)
    use_videoport = config.getboolean("Camera", "usevideo")

    camera.resolution = (camera_width, camera_height)
    camera.framerate = camera_fps
    with picamera.array.PiRGBArray(camera, size=scale) as image:
        for frame in camera.capture_continuous(image, format('bgr'), use_video_port=use_videoport, resize=scale):
            analyzer.frames.put_nowait(image.array)
            image.seek(0)
            image.truncate()
            print("DEBUG: size of frames queue={0}".format(analyzer.frames.qsize()))