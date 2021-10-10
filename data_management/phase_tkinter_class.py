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
    def __init__(self, next_phase, master=None, prev_phase: tk.Frame = None, test: bool = False):
        import cv2

        super().__init__(master)
        self.next_phase = next_phase
        self.master = master
        self.pack()

        if prev_phase is None:

            # ask the user to specify a file
            self.filename = fd.askopenfilename(
                initialdir=path.join(path.dirname(__file__), "..", "data", "transcribed_stories", "51--", "5101"))

            # Check if the OS is Windows or Linux based
            if ':' in self.filename: # Windows
                # correct path specifier
                self.filename = os.path.join(*self.filename.split("/"))
                self.filename = self.filename.replace(":", ":\\")

            self.story_folder = os.path.dirname(self.filename)
            # check if user opened a file in a "phase" folder
            while "phase" in self.story_folder:
                self.story_folder = path.realpath(path.join(self.story_folder, ".."))

            self.np_img = cv2.imread(self.filename, cv2.IMREAD_UNCHANGED - cv2.IMREAD_IGNORE_ORIENTATION)

            # do needed color conversion
            if len(self.np_img.shape) == 3:  # Color Image
                self.np_img = np.array(cv2.cvtColor(self.np_img, cv2.COLOR_RGB2BGR))
            elif len(self.np_img.shape) == 2:  # Gray Scale
                pass

        else:  # there is a previous phase
            self.np_img = prev_phase.np_img
            self.story_folder = prev_phase.story_folder
            self.filename = prev_phase.filename

        self.photo_image_filename_only = path.basename(self.filename)
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

        try:
            self.canvas.bind("<Button-1>", self.canvas_click)
        except:
            print("no canvas_click")

        try:
            self.canvas.bind("<Motion>", self.motion_event)
        except:
            print("no canvas_mouseover")

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

        # need to find better way to resolve if the derived class has canvas_mouseover
        try:
            self.canvas_mouseover(event)
        except:
            pass

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
        if "image_handle" in self.__dir__():
            #canvas_size = self._find_new_canvas_size()
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
        print(self.image_handle)
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

        #print(self.canvas.winfo_width(),self.canvas.winfo_height()," --> ",event.width,event.height)
        self.last_redraw = time.time()
        canvas_size = self._find_new_canvas_size(event)
        w = canvas_size[0]
        h = canvas_size[1]
        #print("resize",w,h)
        self.photo_image = np_photo_image(cv2.resize(self.np_img, (w, h)))

        if "image_handle" in dir():
            if not self.image_handle:
                self.image_handle = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

        self.canvas.itemconfig(self.image_handle, image=self.photo_image)

        if len(self.canvas.children) > 0:
            self.redraw()

    def save_button(self):
        try:
            os.mkdir(path.join(self.story_folder, self.phase))
        except FileExistsError as e:
            self.phase_data_exists = True

        directory = self.story_folder
        filename, extension = path.basename(self.filename).split(".")
        new_file_name = path.join(directory, self.phase, filename + "." + extension)
        #path.relpath()


        # convert before saving
        self.np_img = self.np_img.astype("uint8")

        if len(self.np_img.shape) == 3:
            self.np_img = np.array(cv2.cvtColor(self.np_img, cv2.COLOR_BGR2RGB))

        print(new_file_name)
        cv2.imwrite(new_file_name, self.np_img)

        # convert after saving so next phase gets correct image
        if len(self.np_img.shape) == 3:
            self.np_img = np.array(cv2.cvtColor(self.np_img, cv2.COLOR_RGB2BGR))

        self.filename = new_file_name

