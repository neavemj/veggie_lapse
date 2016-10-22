#!/usr/bin/env python

# timelapse of veg
# imports required for gopro control and scheduling

from goprohero import GoProHero
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import time

# some globals
# how long to wait for camera to turn on, etc. 
sleep_time = 10

# little functions for controlling the camera

def print_time():
    print time.asctime()

def connect_gopro():
    """
    attempts to connect to the gopro through the 
    established wifi connection. 
    checks the status to see if successful or not.
    """
    cam = GoProHero(password="matts_gopro")
    time.sleep(sleep_time)
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
    result = cam.command("power", "on")
    time.sleep(sleep_time)
    if result == False:
        print "could not wake gopro"
    return result

def sleep_gopro(cam):
    """
    attempts to sleep the gopro
    """
    result = cam.command("power", "sleep")
    time.sleep(sleep_time)
    if result == False:
        print "could not sleep gopro"

def still_gopro(cam):
    """
    changes the camera mode to still / photo
    normally it will start up in video mode
    again the result will be boolean (true for successful)
    """
    result = cam.command("mode", "still")
    time.sleep(sleep_time)
    if result == False:
        print "could not put gopro in camera / still mode"
    return result
        
def take_photo(cam):
    """
    attempts to take a photo
    result is boolean
    """
    result = cam.command("record", "on")
    time.sleep(sleep_time)
    if result == False:
        print "could not take photo"
    else:
        print "successfully took a photo"
    return result

def check_status(cam):
    """
    check the camera status after each photo
    maybe the charger is not working or the memory is full?
    """
    status = cam.status()
    if status["summary"] == "notfound" or\
       status["summary"] == "sleeping":
        print "could not find camera to check status"
        return
    elif status["batt1"] < 50:
        print "warning: battery is remaining is:", str(status["batt1"])
    elif status["picsremaining"] < 100:
        print "warning: less than 100 pictures remaining"
    elif status["overheated"] == True:
        print "warning: cameria is overheating"
    elif status["charging"] == "no":
    	print "warning: camera has stopped charging!"

def write_log(cam, photo_taken):
    """
    
    """    
    with open("veggie.log", "a") as fl:
    	fl.write(time.asctime() + "\n")
    	if photo_taken == True:
    		fl.write("photo taken" + "\n")
    	else:
    		fl.write("Unable to take photo" + "\n")
    	status = cam.status() 
    	fl.write("Remaining Battery:" + str(status["batt1"]) + "\n")
    	fl.write("Remaining Pictures:" + str(status["picsremaining"]) + "\n")
    	fl.write("----------------------------------------------------------\n")    	


def main_activation():
    """ 
    this is where everything is coordinated
    decided to use "return" to break out of the funtion if an 
    error occurs. Each sub-function returns a boolean, so if it is
    false (i.e. it was unsuccessful) this main function will stop.
    Note that this does not affect the scheduler, which will just 
    try again at the next interval.
    """
    print_time()
    print "attemping to activate and take a photo.."
    
    cam = connect_gopro()
    #if cam == False:
    #    return
    
    awake = wake_gopro(cam)
    #if awake == False:
    #    return
    
    still_mode = still_gopro(cam)
    #if still_mode == False:
    #    return
    
    photo_taken = take_photo(cam)
    
    check_status(cam)
    write_log(cam, photo_taken)
    sleep_gopro(cam)

# main scheduling calls
# decided to use "apscheduler" for this
# needed to import logging to avoid an error with the scheduler
# the "CronTrigger" can be changed to alter how often a photo is taken
# for example, every hour "hour='*'", every half hour "minute=30"
# every 5th second of every minute, "second=5"

logging.basicConfig()

sched = BlockingScheduler()

#trigger = CronTrigger(second="30")
trigger = CronTrigger(hour="5-22")

sched.add_job(main_activation, trigger)

sched.start()