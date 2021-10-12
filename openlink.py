#!/bin/python3
import icalendar
import pytz
import recurring_ical_events
from datetime import datetime, date,timedelta
import re
import os
from rofi import rofi
import requests
import sys
from config import CALENDAR_URL,TZ

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

if "-u" in sys.argv:
    cal_text = requests.get(CALENDAR_URL).text
    print("Updated")
else:
    cal_text = open("./calendar.ics").read()


cal = icalendar.Calendar.from_ical(cal_text)

def parse_desc(text):
    text = text.strip()
    is_uri = None
    if text.startswith("<") and text[-1]==">":
        text = text.split("href=")[1]
        text = text.split("\"")[1]
    if text.startswith("https://videoconf-colibri.zoom.us"):
        text = text.replace("/j/","/join?action=join&confno=")
        text = text.replace("?pwd","&pwd")
        text = text.replace("https://","zoommtg://")
        text = text.split("#")[0]
    urireg = re.compile(r"(http[s]?|zoommtg)://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    if urireg.match(text):
        if text.startswith("http"):
            is_uri = "Browser"
        elif text.startswith("zoommtg"):
            is_uri = "Zoom"

    return text,is_uri


classes = []
has_class = False

events = recurring_ical_events.of(cal).at(datetime.now(TZ) + timedelta(minutes=5))
# events = recurring_ical_events.of(cal).at(datetime.now(TZ) + timedelta(hours=10,minutes=30,days=3))
for event in events:
    desc, uri_type = parse_desc(event["DESCRIPTION"])
    has_class = True
    print(event["LOCATION"])
    if uri_type:
        classes.append([event["SUMMARY"] , uri_type, desc])
    elif event["LOCATION"] != "":
        classes.append([event["LOCATION"] , "Location", ""])
        


if len(classes) > 0:
    k,i,toopen = rofi("Go to",[" ".join(a[:-1]) + " " + a[-1].split("://")[-1] for a in classes])
    if i >= 0 and classes[i][2] != "":
        os.system("xdg-open \""+ classes[i][2] + "\"")
else:
    if has_class:
        os.system("notify-send \"No link available for current class\"")
    else:
        os.system("notify-send \"No class right now \"")
open("./calendar.ics","w").write(cal_text)
