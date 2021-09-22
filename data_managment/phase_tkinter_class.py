import numpy as np
import os.path as path
import cv2
import tkinter as tk
from tkinter import filedialog as fd
import os


def np_photo_image(image: np.ndarray):
    # This function creates the header information for PPM file format
    # grayscale / RGB images have a digiffering "magic number" p5/p6

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

            # Check if the OS is Windows or Linux based
            if ':' in self.filename:
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

        self.canvas = tk.Canvas()
        self.canvas.pack()
        self.canvas.create_image(8, 8, anchor=tk.NW, image=self.photo_image)

        self.canvas.bind('<Configure>', self.resize)

        try:
            self.canvas.bind("<Button-1>", self.canvas_click)
        except:
            print("no canvas_click")

        try:
            self.canvas.bind("<Motion>", self.canvas_mouseover)
        except:
            print("no canvas_mouseover")


    def find_new_canvas_size(self, event):
        # delta = abs(self.photo_image.width()* self.photo_image.height()) - (event.width *event.height)
        # if delta > 5:
        # print(event)
        if event is not None:
            max_w = event.width
            max_h = event.height
            aspect = self.np_img.shape[0] / self.np_img.shape[1]

            desired_w = max_h / aspect
            desired_h = max_w * aspect

            if desired_w > max_w:
                desired_w = max_w

            if desired_h > max_h:
                desired_h = max_h

            self.canvas.config(width=desired_w, height=desired_h)
            return ([int(desired_w), int(desired_h)])

    def resize(self, event):

        canvas_size = self.find_new_canvas_size(event)
        w = canvas_size[0]
        h = canvas_size[1]
        self.photo_image = np_photo_image(cv2.resize(self.np_img, (w, h)))

        if not self.image_handle:
            self.image_handle = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
            self.canvas.tag_lower(self.image_handle)
        else:
            self.canvas.itemconfig(self.image_handle, image=self.photo_image)
        if "current_np_img_point_idx" in locals().keys():
            pairs = [[0, 1], [1, 2], [2, 3], [3, 0]]
            for pt1_idx, pt2_idx in pairs:
                if (pt1_idx < self.current_np_img_point_idx) & (pt2_idx < self.current_np_img_point_idx):
                    pt1 = self.img_2_canvas_pt(self.np_img_points[pt1_idx])
                    pt2 = self.img_2_canvas_pt(self.np_img_points[pt2_idx])
                    self.canvas.coords(self.line_handles[pt1_idx], *(pt1 + pt2))
                    o_size = 5
                    oval = [pt1[0] - o_size, pt1[1] - o_size, pt1[0] + o_size, pt1[1] + o_size]
                    self.canvas.coords(self.cursor_oval_handles[pt1_idx], oval)


