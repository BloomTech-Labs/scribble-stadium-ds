import time

import numpy as np
import os.path as path
import cv2
import tkinter as tk
from tkinter import filedialog as fd
import numpy as np
import os.path as path
import tkinter as tk
import cv2
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
    def __init__(self, next_phase, master=None, prev_phase: tk.Frame = None, test: bool = False, *args, **kwargs):
        import cv2

        super().__init__(master, *args, **kwargs)
        self.next_phase = next_phase
        self.master = master
        self.pack()

        # set this to none so we know the photo image handle has not been initialized
        self.image_handle = None

        # if ran in stand-alone mode
        if prev_phase is None:

            master.update_idletasks()
            # ask the user to specify a file
            self.os_filename = fd.askopenfilename(
                initialdir=path.join(path.dirname(__file__), "..", "data", "transcribed_stories", "51--", "5101"))

            # Check if the OS is Windows or Linux based
            if ':' in self.os_filename: # Windows
                # correct path specifier
                self.os_filename = os.path.join(*self.os_filename.split("/"))
                self.os_filename = self.os_filename.replace(":", ":\\")

            self.os_story_folder = os.path.dirname(self.os_filename)
            # check if user opened a file in a "phase" folder
            while "phase" in self.os_story_folder:
                self.os_story_folder = path.realpath(path.join(self.os_story_folder, ".."))

            self.np_img = cv2.imread(self.os_filename, cv2.IMREAD_UNCHANGED - cv2.IMREAD_IGNORE_ORIENTATION)

            # do needed color conversion
            if len(self.np_img.shape) == 3:  # Color Image
                self.np_img = np.array(cv2.cvtColor(self.np_img, cv2.COLOR_RGB2BGR))
            elif len(self.np_img.shape) == 2:  # Gray Scale
                pass

        else:  # there is a previous phase
            self.np_img = prev_phase.np_img
            self.os_story_folder = prev_phase.story_folder
            self.os_filename = prev_phase.filename

        self.os_photo_image_filename_only = path.basename(self.os_filename)
        self.os_photo_image_folder = path.dirname(self.os_filename)

        text_full_path = path.join(self.os_story_folder, self.os_photo_image_filename_only.split(".")[0])
        text_full_path=text_full_path.replace("Photo","Story")

        for _ in range(10):
            try:
                with open(text_full_path) as f:
                    self.story_text =f.read()
                    break
            except FileNotFoundError as e:
                pass
            split = text_full_path.split("-")
            text_full_path= "-".join(split[:-1])


        self.photo_image = np_photo_image(self.np_img)
        self.goto_next_phase_flag = None

        self.controls_frame = tk.Frame(master=self, borderwidth="2", relief="groove")
        self.controls_frame.pack(side="left")

        self.canvas_frame = tk.Frame(master=self, borderwidth="0", relief="groove")
        self.canvas_frame.pack(expand=1, fill=tk.BOTH)

        self.canvas = tk.Canvas(master=self.canvas_frame, borderwidth="0")
        self.canvas.pack()

        self.canvas.create_image(8, 8, anchor=tk.NW, image=self.photo_image)

        self.canvas_frame.bind('<Configure>', self.resize)

        if "canvas_click" in self.__dir__():
            self.canvas.bind("<Button-1>", self.canvas_click)

        if "motion_event" in self.__dir__():
            self.canvas.bind("<Motion>", self.motion_event)
        self.np_img_orig = self.np_img.copy()

    def img_2_canvas_pt(self, pt: list):
        x = (pt[0] / self.np_img.shape[1]) * self.canvas.winfo_width()
        y = (pt[1] / self.np_img.shape[0]) * self.canvas.winfo_height()
        return ([x, y])

    def canvas_2_img_pt(self, canvas_pt: list):
        img_x = (canvas_pt[0] / self.canvas.winfo_width()) * self.np_img.shape[1]
        img_y = (canvas_pt[1] / self.canvas.winfo_height()) * self.np_img.shape[0]
        return [img_x, img_y]

    def motion_event(self, event):
        self.redraw_canvas_objects()

        if "canvas_mouseover" in self.__dir__():
            self.canvas_mouseover(event)


    def _find_new_canvas_size(self, event):
        max_w = self.canvas_frame.winfo_width()
        max_h = self.canvas_frame.winfo_height()
        aspect = self.np_img.shape[0] / self.np_img.shape[1]

        desired_w = max_h / aspect
        desired_h = max_w * aspect

        if desired_w > max_w:
            desired_w = max_w

        if desired_h > max_h:
            desired_h = max_h

        if (self.canvas.winfo_height() != desired_h) or (self.canvas.winfo_width() != desired_w):
            self.canvas.config(width=desired_w, height=desired_h, )

        return ([int(desired_w), int(desired_h)])

    def redraw(self):
        """
        redraw the current canvas image based on self.np_img, use this for when self.np_img has changed and the view
        should be updated.
        """
        print("redraw")
        if self.image_handle:
            # canvas_size = self._find_new_canvas_size()
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()
            self.photo_image = np_photo_image(cv2.resize(self.np_img, (w, h)))

            if not self.image_handle:
                self.image_handle = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
            else:
                self.canvas.itemconfig(self.image_handle, image=self.photo_image)

            self.canvas.tag_lower(self.image_handle)

    def redraw_canvas_objects(self):
        """
        redraw object that are on the canvas besides the base photoimage, use this when you have changed things that are
        drawn on the canvas, like lines ovals etc
        """
        if self.image_handle:
            self.canvas.tag_lower(self.image_handle)

        if "current_np_img_point_idx" in locals():
            pairs = [[0, 1], [1, 2], [2, 3], [3, 0]]
            for pt1_idx, pt2_idx in pairs:
                if (pt1_idx < self.current_np_img_point_idx) & (pt2_idx < self.current_np_img_point_idx):
                    pt1 = self.img_2_canvas_pt(self.np_img_points[pt1_idx])
                    pt2 = self.img_2_canvas_pt(self.np_img_points[pt2_idx])
                    self.canvas.coords(self.line_handles[pt1_idx], *(pt1 + pt2))
                    o_size = 5
                    oval = [pt1[0] - o_size, pt1[1] - o_size, pt1[0] + o_size, pt1[1] + o_size]
                    self.canvas.coords(self.cursor_oval_handles[pt1_idx], oval)
            self.canvas.update()

    def resize(self, event):
        """
        handles the fact that the window has been resized or that some other thing has caused the canvas to change
        diminsions. Use this when the shape of the canvas/window/client area has changed
        """
        self.last_redraw = time.time()
        canvas_size = self._find_new_canvas_size(event)
        w = canvas_size[0]
        h = canvas_size[1]
        self.photo_image = np_photo_image(cv2.resize(self.np_img, (w, h)))

        if not self.image_handle:
            self.image_handle = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

        self.canvas.itemconfig(self.image_handle, image=self.photo_image)

        if len(self.canvas.children) > 0:
            self.redraw()

    def save_button(self):
        try:
            os.mkdir(path.join(self.os_story_folder, self.phase))
        except FileExistsError as e:
            self.phase_data_exists = True

        directory = self.os_story_folder
        filename, extension = path.basename(self.os_filename).split(".")
        new_file_name = path.join(directory, self.phase, filename + "." + extension)

        # convert before saving
        self.np_img = self.np_img.astype("uint8")

        if len(self.np_img.shape) == 3:
            self.np_img = np.array(cv2.cvtColor(self.np_img, cv2.COLOR_BGR2RGB))

        print(new_file_name)
        cv2.imwrite(new_file_name, self.np_img)

        # convert after saving so next phase gets correct image
        if len(self.np_img.shape) == 3:
            self.np_img = np.array(cv2.cvtColor(self.np_img, cv2.COLOR_RGB2BGR))

        self.os_filename = new_file_name
