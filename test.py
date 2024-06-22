import pyautogui as pg
import numpy as np
import cv2 as cv
from PIL import ImageGrab, Image
import time

REGION = (0, 0, 400, 400)
GAME_OVER_PICTURE_PIL = Image.open("./green.png")
GAME_OVER_PICTURE_CV = cv.imread('./green.png')


def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(
            f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap


@timing
def benchmark_pyautogui():
    res = pg.locateOnScreen(GAME_OVER_PICTURE_PIL,
                            grayscale=True,  # should provied a speed up
                            confidence=0.8,
                            region=REGION)
    return res is not None


@timing
def benchmark_opencv_pil(method):
    img = ImageGrab.grab(bbox=REGION)
    img_cv = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
    res = cv.matchTemplate(img_cv, GAME_OVER_PICTURE_CV, method)
    # print(res)
    return (res >= 0.8).any()


if __name__ == "__main__":

    im_pyautogui = benchmark_pyautogui()
    print(im_pyautogui)

    methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
               'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']


    # cv.TM_CCOEFF_NORMED actually seems to be the most relevant method
    for method in methods:
        # print(method)
        im_opencv = benchmark_opencv_pil(eval(method))
        print(f"{method} {im_opencv}")
