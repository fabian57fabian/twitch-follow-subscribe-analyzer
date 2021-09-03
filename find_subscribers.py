import os
import argparse
import numpy as np
import cv2
import datetime
import pandas as pd
from image_matcher import check_subscribed


def find_subscribers(filename: str, template_fn: str):
    template = cv2.imread(template_fn, cv2.IMREAD_COLOR)
    # Open video
    vidcap = cv2.VideoCapture(filename)
    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    array_presence = [0]

    # Some helpers for print
    percent_10 = int(length / 100)  # each 1%
    # If our template stays for longer, no need to check each frame
    skip_each_frames = 27

    # Start reading
    success, image = vidcap.read()
    count, is_subscribe = 0, False
    while success:
        if count % percent_10 == 0: print("{}: {}%".format(datetime.datetime.now(), count / percent_10))
        # process image
        if count % skip_each_frames == 0:
            is_subscribe = array_presence[-1]
        else:
            # Check if template is matched
            is_subscribe = 1 if check_subscribed(image, template) else 0
        # Update list
        array_presence.append(is_subscribe)
        success, image = vidcap.read()
        count += 1
    count -= 1
    array_presence = array_presence[1:]
    # Save results to csv
    df = pd.DataFrame(array_presence)
    df.to_csv(filename + ".csv")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Video source path")
    parser.add_argument("--template", required=True, help="Video source path")
    args = parser.parse_args()
    if not os.path.isfile(args.source):
        print("Source {} does not exist!".format(args.source))
        exit(1)
    if not os.path.isfile(args.template):
        print("Template {} does not exist!".format(args.template))
        exit(2)
    find_subscribers(args.source, args.template)
