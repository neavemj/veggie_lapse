#/usr/bin/env python

# timelapse of veg


from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import time


def print_time():
    print time.asctime()


# main scheduling calls

sched = BlockingScheduler()

trigger = CronTrigger(second="*")

sched.add_job(print_time, trigger)

sched.start()