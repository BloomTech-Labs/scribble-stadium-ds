import numpy as np
import os.path as path
import cv2
import tkinter as tk
from tkinter import filedialog as fd
import os


def np_photo_image(image: np.ndarray):
    # This function creates the header information for PPM file format
    # grayscale / RGB images have a differing "magic number" p5/p6

    if len(image.shape) == 3:
        height, width, channels = image.shape
        data = f'P6 {width} {height} 255 '.encode() + image.astype(np.uint8).tobytes()
    elif len(image.shape) == 2:
        height, width = image.shape
        data = f'P5 {width} {height} 255 '.encode() + image.astype(np.uint8).tobytes()
    return tk.PhotoImage(width=width, height=height, data=data, format='PPM')


class PipelinePhase(tk.Frame):
    def __init__(self, next_phase, master=None, prev_phase: tk.Frame = None):
        super().__init__(master)
        self.next_phase = next_phase
        self.master = master
        self.pack()

        if prev_phase is None:
            self.filename = fd.askopenfilename(
                initialdir=path.join(path.dirname(__file__), "..", "data", "transcribed_stories", "51--", "5101"))

            # correct path specifier
            self.filename = os.path.join(*self.filename.split("/"))
            self.filename = self.filename.replace(":", ":\\")
            self.photo_folder = os.path.dirname(self.filename)
            self.np_img = cv2.imread(self.filename, cv2.IMREAD_UNCHANGED - cv2.IMREAD_IGNORE_ORIENTATION)

            if len(self.np_img.shape) == 3:  # Color Image
                self.np_img = np.array(cv2.cvtColor(self.np_img, cv2.COLOR_RGB2BGR))
            elif len(self.np_img.shape) == 2:  # Gray Scale
                pass

        else:
            self.np_img = prev_phase.np_img
            self.photo_folder = prev_phase.photo_folder
            self.filename = prev_phase.filename

        self.photo_image = np_photo_image(self.np_img)
        self.goto_next_phase_flag = None
