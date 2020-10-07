import icalendar
import pytz
import recurring_ical_events
from datetime import datetime, date
import re
import os
from rofi import rofi
import requests
import sys
from config import CALENDAR_URL

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

TZ = pytz.timezone("Europe/Lisbon")
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
    urireg = re.compile("(http[s]?|zoommtg)://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    if urireg.match(text):
        if text.startswith("http"):
            is_uri = "Browser"
        elif text.startswith("zoommtg"):
            is_uri = "Zoom"

    return text,is_uri


classes = []
has_class = False

events = recurring_ical_events.of(cal).at(datetime.now(TZ))
for event in events:
    desc, uri_type = parse_desc(event["DESCRIPTION"])
    has_class = True
    if uri_type:
        classes.append([event["SUMMARY"] , uri_type, desc])


if len(classes) > 0:
    k,i,toopen = rofi("Go to",list(map(lambda a: " ".join(a[:-1]) + " " + a[-1].split("://")[1],classes)))
    if i >= 0:
        os.system("xdg-open \""+ classes[i][2] + "\"")
else:
    if has_class:
        os.system("notify-send \"No link available for current class\"")
    else:
        os.system("notify-send \"No class right now \"")
open("./calendar.ics","w").write(cal_text)
