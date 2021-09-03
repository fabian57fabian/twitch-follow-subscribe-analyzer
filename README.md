# Find twitch subscribers on video
Twitch gives a total number of subscribers per video but does not provide the **entire graph of subscribers in-video**.

This tool will analyze a fideo with a template and **create a plot with subscribers** during video time
## Installation

This softare requires python3 with:
- **OpenCv** (install with `python3 -m pip install opencv-python` or separately)
- Other necessary **libs** with `python3 -m pip install numpy pandas`

(With windows use the same command in Command Prompt using python3.exe instead of python3, or full python3.exe path)

## Usage

Download a video, take a frame and crop out a template for the subscribe message.

Call find_subscribers script with given args:

```bash
python3 find_subscribers.py 
          --source="path_to_video"
          --template="path_to_template"
          --th=0.75
```

if the area where template comes out is the same, use an additional `--box="xmin|xmax|ymin|ymax"` parameter.

You can also lower the threshold if results do not match.

## Description

The script will open the video and check one each 27 frames (configurable parameter) if the template is inside the image with given threshold.

The check is performed with `cv2.matchTemplate` method (acting like an object detector) and filtering only results above threshold.

IF at least one match is found, then the template was detected on image.

## Test

The repo contains 2 images with and without the subscription banner and the banner template as example.

Run following code to check the results:

```bash
python3 test_match.py
```