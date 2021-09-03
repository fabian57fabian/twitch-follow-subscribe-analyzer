import os
import argparse
import numpy as np
import cv2
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from image_matcher import check_subscribed


def find_subscribers(filename: str, template_fn: str, threshold: float = 0.5, bbox: list = None, save_each_print:bool=False):
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
        xmin, xmax, ymin, ymax = 0, width, 0, height
    else:
        xmin, xmax, ymin, ymax = box

    # Data structure for results
    array_presence = [0]

    # Some helpers for print
    percent_10 = int(length / 100)  # each 1%
    # If our template stays for longer, no need to check each frame
    skip_each_frames = 27

    count, is_subscribe = 0, False
    while success:
        if count % percent_10 == 0:
            print("{}: {}%".format(datetime.datetime.now(), count / percent_10))
            if save_each_print:
                df = pd.DataFrame(array_presence, columns=["state"])
                df.to_csv(filename + "_detect.csv")
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
    df = pd.DataFrame(array_presence, columns=["state"])
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
    df["state"].plot()
    plt.show()


def filter_raw_detection(df):
    # TODO: filter large consecutive ones with only one one and others zero
    last_el = 0
    first_el = True
    for index, row in df.iterrows():
        el = row["state"]
        if el != last_el:
            if el == 1:  # rising
                if first_el:
                    first_el = False
                    last_el = 1
                else:
                    row["state"] = 0
            else:  # falling
                first_el = True
                last_el = 0
        else:  # same
            if last_el == 1:
                row["state"] = 0
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Video source path")
    parser.add_argument("--template", required=True, help="Video source path")
    parser.add_argument("--th", type=float, default=0.75, help="Threshold for detection")
    parser.add_argument("--box", type=str, help="Search area in frame as xmin|xmax|ymin|ymax")
    parser.add_argument("--load", action="store_true",
                        help="Load output dataframe instead of compute a new one")
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
    # Load csv or execute detection
    execute_detection = True
    df = None
    if args.load:
        fn = args.source + "_detect.csv"
        if not os.path.isfile(fn):
            print("This video was not detected because {} does not exist!".format(fn))
            print("Executing detected first...")
        else:
            df = pd.read_csv(fn)
            execute_detection = False
    if execute_detection:
        df = find_subscribers(args.source, args.template, args.th, box)
        df.to_csv(args.source + "_detect.csv")
    df = filter_raw_detection(df)
    df.to_csv(args.source + "_detect_filtered.csv")
    plot(df)
