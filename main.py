import pyautogui, time
import cv2 as cv
import numpy as np

from PIL import ImageGrab, Image
pyautogui.FAILSAFE = False
# game_region = (200, 180, 580, 480)
# game_region = (200, 100, 900, 900)
game_region = (200, 100, 700, 800)
click_post_delay = 0.07 # 0.008
go_idle_after = 4

GREEN_PIL = Image.open("./green.png")
YELLOW_PIL = Image.open("./yellow.png")
RED_PIL = Image.open("./red.png")

GREEN_CV = cv.imread("./green.png")
YELLOW_CV = cv.imread("./yellow.png")
RED_CV = cv.imread("./red.png")
PRESS_START_CV = cv.imread("./press-start.png")
START_CV = cv.imread("./start.png")
method = "cv.TM_CCOEFF_NORMED" # 'cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED'

confidence = 0.7
def opencv_pil(image, method, region, threshold):
    img = ImageGrab.grab(bbox=region)
    img_cv = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
    res = cv.matchTemplate(img_cv, image, eval(method))
    
    # Get coordinates of the best match
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    
    # Check if the image was found
    if max_val > threshold:
        h, w = image.shape[:-1]
        center_x = int(max_loc[0] + w / 2 + region[0])
        center_y = int(max_loc[1] + h / 2 + region[1])
        return (center_x, center_y)
    else:
        return None

badcounter = 0
counter = 0
clickcounter = 0
tournament = True
lastclick = time.time()

button_pos = opencv_pil(PRESS_START_CV, method, game_region, confidence)
if(button_pos != None):
    button_pos = opencv_pil(START_CV, method, game_region, confidence)
    if(button_pos != None):
        tournament = False

print(f"ready to rock! in tournament? " + str(tournament) + " click_post_delay: " + str(click_post_delay))
while (True):
    if(tournament):
        if lastclick + go_idle_after < time.time():
            print(f"No click for {go_idle_after} seconds, Whack a Potato reset")
            tournament = False
        counter = counter + 1
        # button_pos = pyautogui.locateOnScreen(GREEN_PIL, confidence=confidence, region=game_region)
        button_pos = opencv_pil(GREEN_CV, method, game_region, confidence)
        if button_pos != None:
            clickcounter = clickcounter + 1
            lastclick = time.time()
            print("Click green clicks: " + str(clickcounter) + " red: " + str(badcounter))
            pyautogui.click(button_pos[0], button_pos[1])
            time.sleep(click_post_delay)
        # button_pos = pyautogui.locateOnScreen(YELLOW_PIL, confidence=confidence, region=game_region)
        button_pos = opencv_pil(YELLOW_CV, method, game_region, confidence)
        if button_pos != None:
            clickcounter = clickcounter + 1
            lastclick = time.time()
            print("Click yellow clicks: " + str(clickcounter) + " red: " + str(badcounter))
            pyautogui.click(button_pos[0], button_pos[1])
            time.sleep(click_post_delay)
        if badcounter < 5:
            # button_pos = pyautogui.locateOnScreen(RED_PIL, confidence=confidence, region=game_region)
            button_pos = opencv_pil(RED_CV, method, game_region, confidence)
            if button_pos != None:
                badcounter = badcounter + 1
                lastclick = time.time()
                print("Click red clicks: " + str(clickcounter) + " red: " + str(badcounter))
                pyautogui.click(button_pos[0], button_pos[1])
                time.sleep(click_post_delay)
    else:
        button_pos = opencv_pil(PRESS_START_CV, method, game_region, confidence)
        if(button_pos != None):
            button_pos = opencv_pil(START_CV, method, game_region, confidence)
            if(button_pos != None):
                tournament = True
                counter = 0
                clickcounter = 0
                badcounter = 0
                lastclick = time.time()
                print("Whack a Potato started")
                pyautogui.click(button_pos[0], button_pos[1])
        

# sudo apt-get install python3-tk python3-dev scrot
# pip3 install opencv-python

