#!/usr/bin/env python

# take the photos in ./photos/ and create a timelapse
# I'll use ffmpeg for this
# Matthew J. Neave 28.10.16

import subprocess

# -f = frame rate; -start_number = first photo number; -i = where integer is in the filename
# -s = resolution; -vcodec = not sure; last bit is video name

#./ffmpeg -r 25 -y -start_number 4146 -i ./photos/GOPR%*.JPG -vf "crop=h=2250" -c:v libx264 -pix_fmt yuv420p -crf 20 -s 1280x720 veggie_lapse.mp4

subprocess.run(["ffmpeg", "-f", "10", "-start_number", "4146", "-i", "./photos/GOPR%*.JPG", "-s", "1280x720", "-vcodec", "libx264", "veggie_lapse.mp4"], shell=True)
