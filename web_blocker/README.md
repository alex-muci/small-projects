# [Web blocker](https://github.com/alex-muci/small-projects/tree/master/web_blocker) 
A simple web blocker to increase the productivity of your day.

``web_blocker`` is a self-contained program - with no external dependencies (just Python) - that block websites by writing local redirection into the ``hosts`` file.

Use
------

**1**. You can simply download the [file](http://github.com/alex-muci/web_blocker/blob/master/web_blocker.py), and after a few changes in the file setup-area (see comments inside the file), run it; e.g. in Windows, open the command line or PowerShell ``as administrator``:
> python [file_path/]web_blocker.py

**2**. You may also want to run the file at startup/reboot (Windows or Linux):

#### *Windows*
============

- change the file extension from .py to .pyw (to run it via pythonw.exe rather than python.exe, i.e. to run the script in the background);
- in the Start Menu search for "Task Scheduler" and open it;
- in the opening form click on "create a task" on the right-hand side:
  - "General" tab: insert (i) a "Name" for the task and (ii) check the "Run with highest privileges" flag;
  - Triggers" tab: click on "New" and select "At startup" in the "Begin the task" validation window;
  - "Actions" tab: click on "New", then select "Start a program" in the "Action" validation window and browse/select the web_blocker.pyw file we want to execute (NB: extension of the file).


#### *Linux*
============

- sudo crontab -e
- then add the following to the end of the opening file (insert your [path]):
> @reboot python3 /home/[]/web_blocker.py

  and save it (ctrl+X) .
