import icalendar
import recurring_ical_events as recurring
import os
import sys
from datetime import date, datetime, timedelta

from config import CALENDAR_URL, TZ

# Change to current file's folder
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Just an alias
now = TZ.localize(datetime.now(), is_dst=False)

def pretty_print_time_until(time):
    delta = time - now
    hours = int(delta.total_seconds() / 3600)
    minutes = int((delta.total_seconds() % 3600) / 60)
    if delta < timedelta(hours=1):
        return str(minutes) + "m"
    elif delta < timedelta(hours=3):
        return str(hours) + "h" + str(minutes) + "m"
    else:
        return str(hours) + " hours"


def pretty_print_current_class(cclass):
    return cclass.decoded("summary").decode() + " ends in " + pretty_print_time_until(cclass.decoded("dtend")) + "."


# Grab calendar from file
cal_text = open("./calendar.ics").read()
cal = icalendar.Calendar.from_ical(cal_text)

today_events = recurring.of(cal).at(date.today())
events = []
for event in today_events:
    if event.decoded("dtend") > now:
        events.append(event)

events.sort(key=lambda x: x.decoded("dtstart"))

# Types of prints
if len(events) == 0:
    sys.exit(1)
if events[0].decoded("dtstart") > now:
    print(events[0].decoded("summary").decode() + " in " +
          pretty_print_time_until(events[0].decoded("dtstart")))
elif len(events) >= 2:
    if events[1].decoded("dtstart")-events[0].decoded("dtend") == 0:
        print(pretty_print_current_class(
            events[0]) + events[1].decoded("summary").decode() + " afterwards.")
    else:
        print(pretty_print_current_class(events[0]) + events[1].decoded("summary").decode() + " after a " +
              pretty_print_time_until(events[1].decoded("dtstart") - events[0].decoded("dtend") + now) + " break.")
else:
    print(pretty_print_current_class(events[0]))
