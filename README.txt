Launch downtime.py from the terminal.  It will run in the background and continue running even after you close the terminal (you'll need to kill the process in order to stop it).

The script will ping google once a minute and write some log files reporting success or failure.  These log files are then parsed and turned into html files containing timeline graphs.

The primary purpose of the script is to visualize network reliability for the networks you use.  (Well, the actual purpose is to learn and experiment, but I mean besides that...)