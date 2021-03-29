# auto-uni
I'll put all my university related automation scripts here.

Instructions:
Make a calendar where the description of each event is a link for a class, be it http or Zoom.  
IMPORTANT, make sure to set the proper timezone, or DST will mess you up.  
Copy "config.example.py" to "config.py" and add a link to your .ics calendar and change the timezone.  
Run pip3 install -r requirements.txt, if there are errors report them to me and try installing them manually.  

Install rofi on your distro.  
Arch: `pacman -S rofi`  
Ubuntu: `apt install rofi`  

Do `python3 openlink.py -u` to update the calendar, from now on you can run it without the -u flag, until you want to update the calendar again.

Optionally set a keybind for the script with your window manager, and once its class time, just run it.

Do `python3 countdown.py` to display time info for your next class. Currently overlapping classes are UB.
