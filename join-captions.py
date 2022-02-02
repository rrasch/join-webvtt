#!/usr/bin/env python3

import argparse
import datetime
import decimal
import os
import re
import sys


def get_secs(tstamp):
    return str((conv_tstamp(tstamp) - conv_tstamp("00:00:00.000")).total_seconds())

def conv_tstamp(tstamp):
    return datetime.datetime.strptime(tstamp, "%H:%M:%S.%f")

def add_delta(t, delta):
    return (conv_tstamp(t)
        + datetime.timedelta(seconds=delta)).strftime('%H:%M:%S.%f')[:-3]


parser = argparse.ArgumentParser(
    description="Join caption files.")
parser.add_argument("input", metavar="INPUT FILE",
    nargs='+',
    help="Input caption files")
# parser.add_argument("-o", "--output", metavar="OUTPUT_FILE",
#     required=True,
#     help="Output caption file")
parser.add_argument("-d", "--debug",
    help="Enable debugging messages", action="store_true")
args = parser.parse_args()

# if os.path.exists(args.output):
#     print("Output file already exists.", file=sys.stderr)
#     exit(1)

delta = '0.0'

for i in args.input:
    print("reading %s" % i, file=sys.stderr)

    with open(i) as f:
        tstamp = ""
        new_timestamp = ""
        lines = f.readlines()
        for line in lines:
            match = re.search(
                r'Speaker (\d+) (\d{2}:\d{2}:\d{2}\.\d+)(?:\.(\d+))?$',
                line)
            if match:
                speaker_num = match.group(1)
                tstamp = match.group(2)
                if match.group(3):
                    tstamp = tstamp + match.group(3)[0:3]
                #print(f"speaker: {speaker_num}", file=sys.stderr)
                #print(f"timestamp: {tstamp}", file=sys.stderr)
                new_timestamp = add_delta(tstamp, float(delta))
                #print(f"new timestamp: {new_timestamp}", file=sys.stderr)
                print(f"Speaker {speaker_num} {new_timestamp}")
            else:
                print(line, end='')
        print(f"old={tstamp}", file=sys.stderr)
        print(f"new={new_timestamp}", file=sys.stderr)
        #print(delta, file=sys.stderr)
        #print(get_secs(tstamp), file=sys.stderr)
        delta = str(decimal.Decimal(delta) +
            decimal.Decimal(get_secs(tstamp)))
        print(f"delta={delta}", file=sys.stderr)


