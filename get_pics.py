#!/usr/bin/env python

import os
import wget
import requests
import time
from goprohero import GoProHero
from bs4 import BeautifulSoup

# first need some functions to connect and wake gopro
# need to do this before accessing server

def connect_gopro():
    """
    attempts to connect to the gopro through the 
    established wifi connection. 
    checks the status to see if successful or not.
    """
    print "connecting to gopro"
    cam = GoProHero(password="matts_gopro")
    time.sleep(10)
    status = cam.status()
    if status["summary"] == "notfound":
        print "could not connect to camera"
        return False
    else:    
        return cam
        
def wake_gopro(cam):
    """
    attempts to wake up the gopro
    the result is boolean (true if successful)
    time.sleep is used to ensure time for the camera to wake
    """
    print "waking gopro"
    result = cam.command("power", "on")
    time.sleep(10)
    if result == False:
        print "could not wake gopro, this probably won't work"
    return result

# connect and wake gopro

cam = connect_gopro()
wake_gopro(cam)
    		
# connect to gopro server

go_pro_url = "http://10.5.5.9:8080/videos/DCIM/102GOPRO/"
site = requests.get(go_pro_url)

# use beautifulsoup to parse output from server

soup = BeautifulSoup(site.text, 'html.parser')

# want to extract out all 'a' tags, then the href links
# these correspond to the photo names

a_tags = soup.find_all('a')

photo_list = [tag['href'] for tag in a_tags if tag['href'].startswith("GOPR")]

# turn list into a set so I can do set operations
# also check that there are no duplicates

photo_set = set(photo_list)

if len(photo_set) != len(photo_list):
    print("warning: there appears to be duplicates in the photos")

# now see if any photos on the camera are not on the computer

computer_photo_set = set(os.listdir("./photos/"))

new_photos = photo_set - computer_photo_set

if len(new_photos) == 0:
    print("there are no new photos to download\nexiting\n")

else:
    print("you have {} new photos to download".format(len(new_photos)))
    ans = raw_input("Would you like to download them now (y/n)? ")

# 4308 is up-side down, 4310, 4311, 4312 wrong spot

if ans == "y":
	photos_remaining = len(new_photos)
    for photo in new_photos:
    	print("photos to download:", str(photos_remaining))
        print("downloading file:", photo)
        photo_url = go_pro_url + photo 
        wget.download(photo_url, "./photos/")
        photos_remaining -= 1
    print("\nfinished downloading photos")      
else:
    print("ok, exiting..")



