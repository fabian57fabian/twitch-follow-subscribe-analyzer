from find_subscribers import check_subscribed
import cv2

if __name__ == '__main__':
    template = cv2.imread("test_images/template.png", cv2.IMREAD_COLOR)
    res1 = check_subscribed(cv2.imread("test_images/frame.png", cv2.IMREAD_COLOR), template)
    print("Template found in frame.png: {}".format(res1))
    res2 = check_subscribed(cv2.imread("test_images/frame_nopic.png", cv2.IMREAD_COLOR), template)
    print("Template found in frame_nopic.png: {}".format(res2))