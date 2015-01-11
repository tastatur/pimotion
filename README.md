# pimotion
This is simple program, which use your Raspberry PI camera to detect the motions.
The output data will be saved in the jpeg files and also displayed on [C-Berry](http://admatec.de/news/presse/c-berry-meets-raspberry) TFT display.

## Requirements:
- Python 2.7 (because the current stable version of OpenCV doesn't support python3, it will be upgraded as soon as OpenCV 3 is stable)
- [Picamera](http://picamera.readthedocs.org)
- OpenCV and python bindings
- [Python bindings for C-Berry](https://github.com/tastatur/cberry) - this is actually a copy of 
[Admatec official C-Berry examples](http://admatec.de/news/presse/c-berry-meets-raspberry), which is just compiled as 
shared library and have python bindings, generated with [ctypesgen](https://code.google.com/p/ctypesgen/)