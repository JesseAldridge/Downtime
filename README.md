
[Demo output](http://dl.dropbox.com/u/135901/downtime/html_out/192.168.0.html) -- this is live output from my wifi connection at home.  As you can see, I've got a pretty shitty connection (plenty of red).

To run the application, launch downtime.py from your terminal.  It will run in the background and continue running even after you close the terminal (you'll need to kill the python process in order to stop it).

The script will ping google once a minute and write some log files reporting success or failure.  These log files are then parsed and turned into html files containing timeline graphs.

The primary purpose of the script is to visualize network reliability for the networks you use.  (Well, the actual purpose is to learn and experiment, but I mean besides that...)