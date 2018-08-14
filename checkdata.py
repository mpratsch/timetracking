#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 [] Import args
 [x] Check if all actions are available in the other file like WORKSTART, BREAKSTART,....
 [x] If you worked more than 10 hours show the remain mintues by 10 hours to put it somewhere else
 [] Also make sure to work not longer than 6 hours before you have your first break even with only one break. 
"""

"""
Application - The way to make things right.
Usage:
  application.py arg1 [--arg2 <key>]
  application.py (-h | --help)
  application.py --version
Options:
  -h, --help    Show this screen.
  --version     Show version.
  --arg2 <key>  Another argument [default: 42].
"""

__author__ = 'Martina Rath'
__copyright__ = 'Copyright 2018, Cisco Systems Inc.'
__credits__ = ['Road Runner', 'Road Runners best friend Harrold']
__license__ = 'MIT'
__version__ = '0.0.1'
__maintainer__ = 'Martina Rath'
__email__ = 'mpratsch@cisco.com'
__status__ = 'Development'

import time
from datetime import datetime, timedelta
from sys import argv
from re import search
import docopt
import random


class MainClass:
    """
    Main class which holds this and that and does this and that.
    """

    with open(argv[1]) as f:
        sumbreak = []
        sumwork = []
        breakstop = ''
        count_break = int(0)

        for line in f:
            # Get the date from file
            matchDate = search('DAY (.*) ----', line)
            if matchDate:
                print(matchDate.group(1))

            # Get the start line and print the date
            matchBegin = search('.*(\d{10}).*WORKSTART', line)
            if matchBegin:
                workstart = matchBegin.group(1)
                print("  Work begin    :\t%s" % time.strftime('%H:%M', time.localtime(int(workstart))))

            # Get the break start
            matchBreakStart = search('.*(\d{10}).*BREAKSTART', line)
            if matchBreakStart:
                breakstart = matchBreakStart.group(1)
                # Counts how many breaks you had
                count_break += 1

            # Get the break end
            matchBreakStop = search('.*(\d{10}).*BREAKEND', line)
            if matchBreakStop:
                breakstop = matchBreakStop.group(1)
                # Calculate the break time
                sumbreak1 = (int(breakstop) - int(breakstart))
                # Append the time in case you did more than one break
                sumbreak.append(int(sumbreak1))

            # Get the end
            matchEnd = search('.*(\d{10}).*WORKEND', line)
            if matchEnd:
                workend = matchEnd.group(1)
                # Calculate only working hours and substract the breaks
                sumwork = int(workend) - int(workstart) - int(sum(sumbreak))
                if count_break != 1:
                    # Plus 3 - 5 hours from the work start time (Makes sure to do your lunch break before 6 hours)
                    breakstart = int(workstart) + int(random.randrange(14400, 18000, 5))
                print("  Break start   :\t%s" % time.strftime(
                    '%H:%M', time.localtime(int(breakstart))))
                # Calculate the work start plus the breakstart.
                # That makes sure to book your first break not longer than 6 hours before you started to work
                diff_break_end = int(breakstart) + int(sum(sumbreak))
                print("  Break stop    :\t%s" % time.strftime(
                    '%H:%M', time.localtime(int(diff_break_end))))
                print("  Work end      :\t%s" % time.strftime(
                    '%H:%M', time.localtime(int(workend))))
                print("  Work summary  :\t(%s)   # Time without any breaks" %
                      (timedelta(seconds=sumwork)))
                # Check if you worked more than 10 hours
                if sumwork > 36000:
                    print("\t\t\t#### Warning!!! You worked more than 10 hours in a row! ####")
                    print("\t\t\tConsider to book the remaining time of '%s' to an other day!" % timedelta(seconds=(sumwork - 36000)))
                print("  Break summary :\t(%s)   # %s break(s)\n" %
                      (timedelta(seconds=sum(sumbreak)), count_break))

                # Reset variables to avoid further calculation on the current values
                sumbreak = []
                breakstop = ''
                count_break = int(0)
    f.closed
    True

if __name__ == '__main__':
    #ARGS=docopt.docopt(__doc__, version='Application %s' % __version__)
    MainClass()