# timetracking

Works and tested with Python 3.6.4




## Why do use
If you have booking tool in your company but that's to complex to fill out everyday and to calculate that tool is a good way to make it easier and shows you everything you need in a pretty format. That tool is developed for Austria. I mentioned that because it's not allowed to work longer than 10 hours per day. The tool will tell you that. Also we have to do our first break before 6 hours after we started to work.

* Shows the working time without breaks
* Show the break time without working time
* Points out when you worked longer than 10 hours and shows the remaining time
* If you do more than one break, it will calculate them and guesses when to set the first break. It's easier to book and makes the overview better.
* If makes sure to book your first break before 6 hours

## Usage
```
usage: /usr/local/bin/tracktime.py [-h] -a {s,bs,be,e} [-t TIME] [-d DATE]
                                   [--version]

optional arguments:
  -h, --help            show this help message and exit
  -a {s,bs,be,e}, --action {s,bs,be,e}
                        start of your work shift (default: None)
  -t TIME, --time TIME  Format: HH:MM. (For correction) (default: None)
  -d DATE, --date DATE  Format: DD-mm. (For correction) (default: None)
  --version             print version and exit (default: False)
```

## Examples
```

  # First entry of the day, the start flag
    tracktime.py -a s
  # Book your start of lunch time
    tracktime.py -a bs
  # Book your end of lunch time
    tracktime.py -a be
  # Book the end of your shift
    tracktime.py -a e
  # If you missed a state to book you can correct that but only for the last one
  # If the day is the same you don't need to use the -d flag
    tracktime.py -a be -t 13:45 -d 2018-08-14
```

## Get the result of your booked entries in a pretty format
### checkdata.py

