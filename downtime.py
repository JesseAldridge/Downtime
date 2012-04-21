
import urllib2, os, time, shutil, socket, sys
from datetime import datetime
from os.path import exists, join

# Run in background.  Store output in networks dir.  Ping google.

if os.fork():
    sys.exit()

if exists('networks'):
    shutil.rmtree('networks')
os.mkdir('networks')

while True:
    try:
        response = urllib2.urlopen('http://google.com', timeout=1)
        status = 'ok'
    except urllib2.URLError:
        status = 'down'

    # Append timestamped status to file named with current ip.

    now = datetime.now()
    minute = str(now.minute)
    if len(minute) == 1:
        minute = '0' + minute
    date_str = "%i/%i/%i %i:%s %s" % (
                now.month, now.day, now.year, now.hour % 12,
                minute, 'AM' if now.hour < 12 else 'PM')
    status_line = date_str + ' ' + status
    print status_line
    path = join('networks', socket.gethostbyname(socket.gethostname()))
    path += '.txt'
    with open(path, 'a') as f:
        f.write(status_line + '\n')
    time.sleep(60)

