import os, shutil
from os.path import join, exists
from datetime import datetime

def plot_files():
    # Prepare html_out dir.  Plot all files in raw_out dir.

    if exists('html_out'):
        shutil.rmtree('html_out')
    os.mkdir('html_out')

    for filename in os.listdir('raw_out'):
        plot(filename)


def plot(filename):

    # Read file.  Build timeline, eg:

    # [(start=0, status='up'), (start=10, status='down'),
    #  (start=11, status='up')]

    with open(join('raw_out', filename)) as f:
        text = f.read()

    def parse_line(line):
        dt_str, status = line.rsplit(' ', 1)
        dt_str = dt_str.replace(' 0:', ' 12:')
        return datetime.strptime(dt_str, '%m/%d/%Y %I:%M %p'), status

    def store_flip(dt, status):
        minutes = (dt - start_dt).seconds / 60
        timeline.append(Shift(start_mins=minutes, status=status))

    timeline = []
    lines = text.strip().splitlines()
    if len(lines) <= 1:
        return
    start_dt, status = parse_line(lines[0])
    store_flip(start_dt, status)
    prev_status = status
    for line in lines[1:]:
        dt, status = parse_line(line)
        if status != prev_status:
            prev_status = status
            store_flip(dt, status)
    end_dt = dt

    # Normalize status shift times for use as rects.  Write html template.

    print 'timeline:', timeline
    total_minutes = (end_dt - start_dt).seconds / 60.
    rel_slices = []
    for i in range(len(timeline)):
        shift = timeline[i]
        if i == len(timeline) - 1:
            shift_end = total_minutes
        else:
            shift_end = timeline[i + 1].start_mins
        rect_left = shift.start_mins / total_minutes
        rect_width = (shift_end - shift.start_mins) / total_minutes
        rel_slices.append([rect_left, rect_width])

    with open('template.html') as f:
        template_str = f.read()
    out_path = join('html_out', filename.rsplit('.', 1)[0] + '.html')
    with open(out_path, 'w') as f:
        print 'str(rel_slices):', str(rel_slices)
        f.write(template_str.format(timeline[0].status, str(rel_slices)))

class Shift:
    def __init__(self, **kw):
        self.__dict__.update(kw)
    def __repr__(self):
        return '(%s, %s)' % (self.start_mins, self.status)

if __name__ == '__main__':
    plot_files()