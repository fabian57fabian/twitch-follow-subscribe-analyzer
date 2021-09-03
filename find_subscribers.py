import os
import argparse
import numpy as np
import cv2
import datetime
import pandas as pd
from image_matcher import check_subscribed


def find_subscribers(filename: str, template_fn: str, threshold: float = 0.5, bbox: list=None):
    template = cv2.imread(template_fn, cv2.IMREAD_COLOR)
    # Open video
    vidcap = cv2.VideoCapture(filename)
    # Start reading
    success, image = vidcap.read()
    if not success:
        print("Unable to open video")
        exit(5)
    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if box is None:
        ymin, ymax, xmin, xmax = 0, height, 0, width
    else:
        ymin, ymax, xmin, xmax = box

    # Data structure for results
    array_presence = [0]

    # Some helpers for print
    percent_10 = int(length / 100)  # each 1%
    # If our template stays for longer, no need to check each frame
    skip_each_frames = 27


    count, is_subscribe = 0, False
    while success:
        if count % percent_10 == 0: print("{}: {}%".format(datetime.datetime.now(), count / percent_10))
        # process image
        if count % skip_each_frames == 0:
            is_subscribe = array_presence[-1]
        else:
            # Check if template is matched
            search_area = image[ymin:ymax, xmin:xmax, :]
            is_subscribe = 1 if check_subscribed(search_area, template, threshold) else 0
        # Update list
        array_presence.append(is_subscribe)
        success, image = vidcap.read()
        count += 1
    count -= 1
    array_presence = array_presence[1:]
    # Save results to csv
    df = pd.DataFrame(array_presence)
    df.to_csv(filename + ".csv")
    return df


def parse_box(b):
    box = None
    parts = b.split('|')
    if len(parts) >= 4:
        try:
            box = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
            if not (box[1] > box[0] and box[3] > box[2]):
                box = None
        except:
            box = None
    return box


def plot(df):
    df.plot()


def filter_raw_detection(df):
    # TODO: filter large consecutive ones with only one one and others zero
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Video source path")
    parser.add_argument("--template", required=True, help="Video source path")
    parser.add_argument("--th", type=float, default=0.75, help="Threshold for detection")
    parser.add_argument("--box", type=str, help="Search area in frame as xmin|xmax|ymin|ymax")
    args = parser.parse_args()
    if not os.path.isfile(args.source):
        print("Source {} does not exist!".format(args.source))
        exit(1)
    if not os.path.isfile(args.template):
        print("Template {} does not exist!".format(args.template))
        exit(2)
    if args.th < 0:
        print("Given threshold have to be positive!")
        exit(3)
    box = None
    if args.box is not None and "|" in args.box:
        box = parse_box(args.box)
    df = find_subscribers(args.source, args.template, args.th, box)
    df = filter_raw_detection(df)
    plot(df)