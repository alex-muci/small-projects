import time
#from datetime import datetime as dt
from dateutil import tz
import datetime

dt = datetime.datetime


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                   SETUP-UP
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

""" CHOOSE YOUR OS (Windows OR Linux) """
my_OS = "Windows" # write either "Windows" or "Linux"

""" DEFINE _START_ & _END_ HOURS OF WORKING DAY """
_START_ =  9   # 8 in the morning
_END_   = 17   # 5 in the afternoon
# _tz_ = "Europe/London"


""" INSERT WEBSITES YOU WANT TO BLOCK during working hours """
blocked_websites=["www.facebook.com", "facebook.com",
                  "www.corriere.it", "www.repubblica.it"]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                   PROGRAM
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# local host
redirect ="127.0.0.1"

if my_OS == "Windows":     # 1. Windows: C:\\Windows\\System32\\drivers\\etc\\hosts
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
else:                    # 2. Linux: "/etc/hosts"
    hosts_path = "/etc/hosts"

# tz = tz.gettz(_tz_)

while True:

    _now = dt.now()  # use tznow(_tz_) rather than dt.now() for tz aware datetime

    beginning = dt(_now.year, _now.month, _now.day, _START_)  # ).replace(tzinfo=tz) # tz replaced
    ending = dt(_now.year, _now.month, _now.day, _END_)       # , tzinfo=tz)         # inside

    # WORKING HOURS
    if beginning < _now < ending:
        print("Time to work and study...")
        with open(hosts_path, 'r+') as file:
            content = file.read()        # read the whole file
            for website in blocked_websites:
                if website in content:   # already blocked, do nothing
                    pass
                else:                    # write the website to block at the end
                    file.write(redirect + " " + website + "\n")

    # FUN HOURS
    else:
        with open(hosts_path, 'r+') as file:
            content = file.readlines()   # read lines
            file.seek(0)                 # go to the top (avoid appending and overwrite)
            for line in content:         # write a line that does not contain a blocked website
                if not any(website in line for website in blocked_websites):
                    file.write(line)
            file.truncate()              # delete all remaining lines afterwards
        print("Fun hours...")

    # run it every 6 seconds
    time.sleep(6)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# auxiliary functions (MOVE UP) if they are to be used
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def utcnow():
    return datetime.datetime.now(tz=tz.tzutc())

def tznow(time_zone="Europe/London"):
    """
    # to get the list of time zones:
    #from dateutil.zoneinfo import get_zonefile_instance
    #print(list(get_zonefile_instance().zones))   # over 500 timezones
    """
    my_tz = tz.gettz(time_zone)  # or =tz.gettz() for local zone of computer
    return datetime.datetime.now(tz=my_tz)
