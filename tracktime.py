#!/usr/bin/env python3
"""
  Todos:
    [] Check if you are working with a Mac
    [] Make sure you can also use the file name you want to modify in case you missed the current month
    [x] Calculate the times between s and bs, bs and be, bs and e.
    [] Integrate WebEx Team
"""

from os import environ, mkdir, path
from sys import argv as param
from sys import exit
from datetime import datetime, timedelta
import calendar
import time
import argparse
import calendar

VERSION = '0.1.0'

dir_to_write = environ['HOME'] + '/' + 'timetracking_test'
# Create directory for all the timetracking stuff
if not path.exists(dir_to_write):
    try:
        mkdir(dir_to_write)
    except OSError:
        print("Creation of the directory %s failed" % dir_to_write)
    else:
        print("Successfully created the directory %s " % dir_to_write)

file_name = time.strftime('%Y-%m', time.localtime())
write_to = dir_to_write + '/' + file_name
current_time = time.strftime('%H:%M', time.localtime())
current_date = time.strftime('%Y-%d-%m', time.localtime())
global current_epoch
current_epoch = time.strftime('%s', time.localtime())
date_with_day = time.strftime('%a, %d-%m', time.localtime())
last_state = ''
override_time = ''
override_date = ''

########################
# Define functions

def open_file_to_read():
    if path.isfile(write_to):
        with open(write_to) as f:
            # get only the last booked line of the sheet and remove the last newline
            return list(f)[-1].rstrip('\n')
        f.closed

def convert_to_epoch(date, time):
    fulldate = int(date + ' ' + time)
    print(fulldate)
    #return datetime.strptime(fulldate, '%Y-%m-%d %H:%M:%S')
    return calendar.timegm(fulldate.utctimetuple())

def write_text(fhandler, state):
    global current_time
    #override_time = '13:00'
    if override_time:
        print("Override time")
        if override_date:
            #current_time = override_date + ' ' + override_time
            #current_time = override_time
            current_date = override_date
        #else:
            #current_time = current_date + ' ' + override_time
        current_time = override_time
    #override_date = '2018-07-15'
    if override_date:
        if override_time:
            #        #current_time = override_date + ' ' + override_time
            current_time = override_time
        #else:
            #current_time = override_date + ' ' + current_time
        #    current_time = current_time
        current_date = override_date
        current_epoch1 = convert_to_epoch(current_date, current_time)
        print(current_epoch1)

    if state == 'WORKSTART':
        calc_time = 0
    else:
        last_timestamp = open_file_to_read().split(' ')[1]

        print(datetime.strptime("2018-07-15 13:00:00", '%Y-%m-%d %H:%M:%S')) #%s', time.localtime("2018-07-15 13:00:00")))
              #current_time =
        #pattern = '%Y-%m-%d %H:%M'
        #epoch = int(calendar.timegm(time.strptime(current_time, pattern)))
        #print(epoch)
        #datetime.strptime
        #print(date_parse("2009-03-08T00:27:31.807Z"))
        #print(time.strftime('%s', "2018-07-15 13:00:00"))
        calc_time = (timedelta(seconds=int(
            current_epoch) - int(last_timestamp)))
    fhandler(current_time + ' ' + current_epoch + ' ' +
            state + ' (' + str(calc_time) + ')\n')
    print("Booked %s. Duration from last state to now: %s" % (state, str(calc_time)))

def default_text(state, text):
    return 'Your last booked state is "' + str(state) + '". ' + text + ' If the last state is wrong please correct your sheet before trying again!'


def main():
    parser = argparse.ArgumentParser(
        __file__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='A foo that bars', epilog="And that's how you'd foo a bar")
    modes = parser.add_mutually_exclusive_group(required=False)
    parser.add_argument("-a", "--action",  help="start of your work shift",
                        required=True, type=str, choices=['s', 'bs', 'be', 'e'])
    parser.add_argument("-t", "--time", help="Format: HH:MM. (For correction)")
    parser.add_argument("-d", "--date", help="Format: DD-mm. (For correction)")
    modes.add_argument('--version',
                       action='store_true',
                       help='print version and exit')

    args = parser.parse_args()

    #if args.version:
    #  print('%s %s' % (__file__, VERSION))
    #parser.exit()


    ########################
    # Start the main part
    ########################

    with open(write_to, 'a') as f:
        # Fix for issues if that is the first entry for a new file (months wise)
        # Since it checks the last state of a file and there is no state in a new file it would throw an error.
        if path.getsize(write_to) == 0:
            last_state = ''
        else:
            # Gets the name of the last booked state
            last_state = open_file_to_read().split(' ')[2]
        
        if args.time:
            # Check if the pattern matches
            global override_time
            # Add the missing seconds to fullfill the format standard
            override_time = args.time + ':00'

        if args.date:
            global override_date
            override_date = args.date

        # Book the start of your work shift
        if args.action == 's':
            if last_state == '' or last_state == 'WORKEND':
                f.write('---- DAY ' + date_with_day + ' ----\n')
                write_text(f.write, 'WORKSTART')
            else:
                print(default_text(
                    last_state, 'You can use "bs" (BREAKSTART) or "e" (WORKEND) next to continue.'))
                exit(1)

        # Book the start of the break
        elif args.action == 'bs':
            if last_state == 'WORKSTART' or last_state == 'BREAKEND':
                write_text(f.write, 'BREAKSTART')
            else:
                print(default_text(last_state, 'You must use "be" (BREAKEND) next!'))
                exit(1)

        # Book the end of the break
        elif args.action == 'be':
            if last_state == 'BREAKSTART':
                write_text(f.write, 'BREAKEND')
            else:
                print(default_text(
                    last_state, 'You can use "e" (WORKEND) or "bs" (BREAKSTART) next to continue.'))
                exit(1)

        # Book the end of the work shift
        elif args.action == 'e':
            # TODO: Calculate if you worked more than 6 hours already.
            if last_state == 'WORKSTART' or last_state == 'BREAKEND':
                write_text(f.write, 'WORKEND')
            else:
                print(default_text(
                    last_state, 'You must use "s" (WORKSTART) next or "be" (BREAKEND) to end the break!'))
                exit(1)
    f.closed
    parser.exit()


if __name__ == '__main__':
    main()