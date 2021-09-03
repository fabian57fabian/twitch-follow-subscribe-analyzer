import os
import argparse
import numpy as np
import cv2
import pandas as pd
from image_matcher import check_subscribed

def find_subscribers(filename: str, template_fn: str):
    template = cv2.imread(template_fn, cv2.IMREAD_COLOR)
    # Open video
    vidcap = cv2.VideoCapture(filename)
    array_presence = [0]
    # Start reading
    success, image = vidcap.read()
    count = 0
    while success:
        # Check if template is matched
        is_subscribe = 1 if check_subscribed(image, template) else 0
        #Update list
        array_presence.append(is_subscribe)
        success, image = vidcap.read()
        count += 1
    count -= 1
    array_presence = array_presence[1:]
    # SAve results to csv
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
