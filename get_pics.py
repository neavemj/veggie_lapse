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
    time.sleep(5)
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
    result = cam.command("power.JPG", "on")
    time.sleep(5)
    if result == False:
        print "could not wake gopro, this probably won't work"
    return result

def sleep_gopro(cam):
    """
    attempts to sleep the gopro
    """
    print "putting gopro to sleep"
    result = cam.command("power.JPG", "sleep")
    time.sleep(5)
    if result == False:
        print "could not sleep gopro"

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

unwanted_photos = set(["GOPR4308.JPG","GOPR4310.JPG","GOPR4311.JPG","GOPR4312.JPG","GOPR4313.JPG","GOPR4314.JPG","GOPR4315.JPG",\
"GOPR4316.JPG","GOPR4317.JPG","GOPR4318.JPG","GOPR4319.JPG","GOPR4320.JPG","GOPR4321.JPG","GOPR4378.JPG","GOPR4379.JPG","GOPR4164.JPG",\
"GOPR4180.JPG","GOPR4197.JPG","GOPR4214.JPG","GOPR4327.JPG","GOPR4310.JPG","GOPR4339.JPG","GOPR4352.JPG","GOPR4381.JPG","GOPR4383.JPG",\
"GOPR4397.JPG","GOPR4163.JPG","GOPR4167.JPG","GOPR4226.JPG","GOPR4239.JPG","GOPR4256.JPG","GOPR4269.JPG","GOPR4288.JPG","GOPR4325.JPG",\
"GOPR4327.JPG","GOPR4339.JPG","GOPR4352.JPG","GOPR4380.JPG","GOPR4165.JPG","GOPR4166.JPG","GOPR4183.JPG","GOPR4198.JPG","GOPR4199.JPG",\
"GOPR4200.JPG","GOPR4213.JPG","GOPR4215.JPG","GOPR4216.JPG","GOPR4223.JPG","GOPR4225.JPG","GOPR4240.JPG","GOPR4241.JPG","GOPR4258.JPG",\
"GOPR4259.JPG","GOPR4268.JPG","GOPR4270.JPG","GOPR4271.JPG","GOPR4286.JPG","GOPR4287.JPG","GOPR4303.JPG","GOPR4305.JPG","GOPR4309.JPG",\
"GOPR4324.JPG","GOPR4325.JPG","GOPR4326.JPG","GOPR4327.JPG","GOPR4340.JPG","GOPR4341.JPG","GOPR4350.JPG","GOPR4351.JPG","GOPR4363.JPG",\
"GOPR4364.JPG","GOPR4384.JPG","GOPR4396.JPG","GOPR4398.JPG","GOPR4405.JPG","GOPR4406.JPG","GOPR4407.JPG","GOPR4415.JPG","GOPR4416.JPG",\
"GOPR4417.JPG","GOPR4116.JPG","GOPR4147.JPG","GOPR4148.JPG","GOPR4182.JPG","GOPR4184.JPG","GOPR4185.JPG","GOPR4224.JPG","GOPR4242.JPG",\
"GOPR4257.JPG","GOPR4304.JPG","GOPR4146.JPG","GOPR4181.JPG","GOPR4309.THM","GOPR4309.MP4","GOPR4309.LRV","GOPR4632.JPG","GOPR4548.LRV",\
"GOPR4548.MP4","GOPR4548.THM","GOPR4549.LRV","GOPR4549.MP4","GOPR4549.THM","GOPR4550.LRV","GOPR4550.MP4","GOPR4550.THM","GOPR4551.JPG",\
"GOPR4555.JPG","GOPR4530.JPG","GOPR4531.JPG","GOPR4532.JPG","GOPR4533.JPG","GOPR4534.JPG","GOPR4535.JPG","GOPR4536.JPG","GOPR4537.JPG",\
"GOPR4497.JPG","GOPR4511.JPG"])

new_photos = new_photos - unwanted_photos

if len(new_photos) == 0:
    print("there are no new photos to download\nexiting\n")

else:
    print("you have {} new photos to download".format(len(new_photos)))
    ans = raw_input("Would you like to download them now (y/n)? ")

if ans == "y":
    photos_remaining = len(new_photos)
    for photo in new_photos:
        print("photos to download:.JPG", str(photos_remaining))
        print("downloading file:.JPG", photo)
        photo_url = go_pro_url + photo 
        wget.download(photo_url, "./photos/")
        photos_remaining -= 1
    print("\nfinished downloading photos")
    sleep_gopro(cam)      
else:
    print("ok, exiting..")
    #sleep_gopro(cam)



