import os, shutil
from collections import defaultdict
from os.path import join, exists
from datetime import datetime

def plot_files():
    # From raw_out to html_out.  Group similar ips.

    if exists('html_out'):
        shutil.rmtree('html_out')
    os.mkdir('html_out')

    groups = defaultdict(list)
    for filename in os.listdir('raw_out'):
        with open(join('raw_out', filename)) as f:
            lines = f.read().strip().splitlines()
        groups[filename.rsplit('.', 2)[0]].extend(lines)

    def by_time(line):
        dt, _ = parse_line(line)
        return dt

    for key, lines in groups.iteritems():
        lines.sort(key=by_time)
        plot(key + '.txt', lines)


def plot(filename, lines):
    # Read file.  Write html template.

    slice_tuples = [make_slices(x) for x in
                    lines, lines[-60 * 24:], lines[-60:]]

    with open('template.html') as f:
        template_str = f.read()
    out_path = join('html_out', filename.rsplit('.', 1)[0] + '.html')
    with open(out_path, 'w') as f:
        f.write(template_str.format(slice_tuples))


def parse_line(line):
    dt_str, status = line.rsplit(' ', 1)
    dt_str = dt_str.replace(' 0:', ' 12:')
    return datetime.strptime(dt_str, '%m/%d/%Y %I:%M %p'), status


def make_slices(lines):
    #Build timeline, eg:

    # [(start=0, status='up'), (start=10, status='down'),
    #  (start=11, status='up')]

    if len(lines) <= 1:
        return

    def store_flip(dt, status):
        minutes = (dt - start_dt).seconds / 60
        timeline.append(Shift(start_mins=minutes, status=status))

    timeline = []
    start_dt, status = parse_line(lines[0])
    store_flip(start_dt, status)
    prev_status = status
    for line in lines[1:]:
        dt, status = parse_line(line)
        if status != prev_status:
            prev_status = status
            store_flip(dt, status)
    end_dt = dt

    # Normalize status shift times for use as rects.

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
    return {'slices':rel_slices, 'initial_status':timeline[0].status}


class Shift:
    def __init__(self, **kw):
        self.__dict__.update(kw)
    def __repr__(self):
        return '(%s, %s)' % (self.start_mins, self.status)

if __name__ == '__main__':
    plot_files()