import pyautogui, time
import cv2 as cv
import numpy as np
import pygetwindow as gw
import tkinter as tk

from PIL import ImageGrab, Image
pyautogui.FAILSAFE = False
# game_region = (200, 180, 580, 480)
game_region = (200, 100, 900, 900)
click_post_delay = 0.006

# Create the overlay window
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-alpha", 0.5)  # Set the transparency level
root.geometry(f"{game_region.width}x{game_region.height}+{game_region.left}+{game_region.top}")

x, y, w, h = game_region
canvas = tk.Canvas(root, bg="blue", highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)
canvas.create_rectangle(x, y, x+w, y+h, outline="red", width=2)