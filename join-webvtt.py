#!/usr/bin/env python3

import argparse
import datetime
import os
import sys
import webvtt


# def fmt_tstamp(secs):
#     return (datetime.datetime(1900, 1, 1) + 
#         datetime.timedelta(seconds=secs)).strftime('%H:%M:%S.%f')[:-3]
# 
# def add_tstamps(t1, t2):
#     t0 = conv_tstamp("00:00:00.000")
#     return (conv_tstamp(t1) - t0 + conv_tstamp(t2)).strftime('%H:%M:%S.%f')[:-3]
# 

def conv_tstamp(tstamp):
    return datetime.datetime.strptime(tstamp, "%H:%M:%S.%f")

def add_delta(t, delta):
    return (conv_tstamp(t)
        + datetime.timedelta(seconds=delta)).strftime('%H:%M:%S.%f')[:-3]


parser = argparse.ArgumentParser(
    description="Join WebVTT files.")
parser.add_argument("input", metavar="INPUT FILE",
    nargs='+',
    help="Input WebVTT files")
parser.add_argument("-o", "--output", metavar="OUTPUT_FILE",
    required=True,
    help="Output WebVTT file")
parser.add_argument("-d", "--debug",
    help="Enable debugging messages", action="store_true")
args = parser.parse_args()

if os.path.exists(args.output):
    print("Output file already exists.", file=sys.stderr)
    exit(1)

joined_vtt = webvtt.WebVTT()

delta = 0.0

id = 1

for i in args.input:
    print("reading %s" % i, file=sys.stderr)

    vtt = webvtt.read(i)
    print(f"vtt[0].start: {vtt[0].start}", file=sys.stderr)
    print(f"vtt[-1].end: {vtt[-1].end}", file=sys.stderr)

    last_tstamp = vtt[-1].end_in_seconds

    for caption in vtt:
        caption.identifier = str(id)
        caption.start = add_delta(caption.start, delta)
        caption.end = add_delta(caption.end, delta)
        joined_vtt.captions.append(caption)
        id = id + 1

    delta = delta + last_tstamp
    print(f"detla: {delta}", file=sys.stderr)

joined_vtt.save(args.output)

