#!/usr/bin/env python

# take the photos in ./photos/ and create a timelapse
# I'll use ffmpeg for this
# Matthew J. Neave 28.10.16

import subprocess

# -f = frame rate; -start_number = first photo number; -i = where integer is in the filename
# -s = resolution; -vcodec = not sure; last bit is video name

#ffmpeg -f 15 -start_number 4146 -i GOPR%d.JPG -s 1280x720 -vcodec libx264 veggie_lapse.mp4

subprocess.run(["ffmpeg", "-f", "15", "-start_number", "4146", "-i", "./photos/GOPR%d.JPG", "-s", "1280x720", "-vcodec", "libx264", "veggie_lapse.mp4"], shell=True)
