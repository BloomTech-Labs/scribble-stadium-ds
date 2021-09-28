"""
This module's purpose is to allow for color manipulation of the image to produce clearer images for the dataset. This
is achieved by changing the color data to remove lines and improve contrast.

image will be saved with -colored appended before the file extension
"""

import numpy as np
import os.path as path
import tkinter as tk
from tkinter import filedialog as fd
import cv2
from phase_tkinter_class import PipelinePhase
from phase_tkinter_class import np_photo_image
from custom_tk_widgets import Slider


class Application(PipelinePhase):
    def __init__(self, next_phase, master=None, prev_phase: PipelinePhase = None):
        super().__init__(next_phase, master=master, prev_phase=prev_phase)
        self.points = []
        self.cursor_oval_handles = []
        self.line_handles = []

        self.newest_pt_idx = -1
        self.np_img_orig = self.np_img.copy()
        self.invert_output = False
        self.invert_red = tk.IntVar()
        self.invert_green = tk.IntVar()
        self.invert_blue = tk.IntVar()

        self.create_widgets()
        # self.cursor

        print(self.filename)

    def create_widgets(self):
        # self.transform_btn = tk.Button(self)
        # self.transform_btn["text"] = "Transform"
        # self.transform_btn["command"] = self.transform_button
        # self.transform_btn.pack(side="top")

        # red channel
        self.red_frame = tk.Frame(self, borderwidth=1, relief=tk.SOLID);
        self.red_frame.pack()
        self.red_frame_label = tk.Label(self, borderwidth=1, relief=tk.SOLID, text='newlabel');
        self.red_frame_label.pack()
        self.red_invert_check = tk.Checkbutton(self.red_frame, text="invert", variable=self.invert_red)
        self.red_invert_check.pack(side="left")

        self.red_slider = Slider(self.red_frame, handles=2, min=0, max=255, width=400, height=40,
                                 command=lambda x: self.update_image("red", x))
        #self.red_slider.set(0)
        self.red_slider.pack(fill="none", expand="false")
        #self.red_slider = tk.PanedWindow(handlepad=0)


        # green channel
        self.green_frame = tk.Frame(self, borderwidth=1, relief=tk.SOLID)
        self.green_frame.pack()
        self.green_frame_label = tk.Label(self, borderwidth=1, relief=tk.SOLID, text='new_new_label');
        self.green_frame_label.pack()

        self.green_invert_check = tk.Checkbutton(self.green_frame, text="invert", variable=self.invert_green)
        self.green_invert_check.pack(side="left")

        self.green_slider = Slider(self.green_frame, handles=2, min=0, max=255, width=400, height=40,
                                   command=lambda x: self.update_image("green", x))
        self.green_slider.pack(fill="none", expand="false")

        self.blue_frame = tk.Frame(self, borderwidth=1, relief=tk.SOLID)
        self.blue_frame.pack(anchor="w")
        self.blue_frame_label = tk.Label(self, borderwidth=1, relief=tk.SOLID, text='new_new_label');
        self.blue_frame_label.pack()

        self.blue_invert_check = tk.Checkbutton(self.blue_frame, text="invert", variable=self.invert_blue)
        self.blue_invert_check.pack(side="left")

        self.blue_slider = Slider(self.blue_frame, handles=2, min=0, max=255, width=400, height=40,
                                  command=lambda x: self.update_image("blue", x))
        self.blue_slider.pack(fill="none", expand="false")

        self.invert_output = tk.Checkbutton(self, text="invert output")
        self.invert_output.pack()
        self.invert_output["command"] = self.invert_check_box
        self.save_btn = tk.Button(self)
        self.save_btn["text"] = "save"
        self.save_btn["command"] = self.save_button
        self.save_btn.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.image_handle = None

    def invert_check_box(self):
        self.invert_output = not self.invert_output
        self.update_image('red', self.red_slider.current_sorted_values)

    def update_image(self, channel, values):

        def normalize(C):
            C = C - C.min()
            C = C / C.max()
            C = C * 255
            return C

        if channel == 'red':
            position = 0

        if channel == 'green':
            position = 1

        if channel == 'blue':
            position = 2

        r1, r2 = self.red_slider.current_sorted_values
        g1, g2 = self.green_slider.current_sorted_values
        b1, b2 = self.blue_slider.current_sorted_values

        print(r1, r2, g1, g2, b1, b2)

        selectionR = (self.np_img_orig[:, :, position] >= r1) * (self.np_img_orig[:, :, position] <= r2)
        selectionG = (self.np_img_orig[:, :, position] >= g1) * (self.np_img_orig[:, :, position] <= g2)
        selectionB = (self.np_img_orig[:, :, position] >= b1) * (self.np_img_orig[:, :, position] <= b2)

        if self.invert_red == True:
            selectionR = np.invert(selectionR                                  )
        selection = selectionR * selectionG * selectionB

        selection = np.reshape(selection, (self.np_img.shape[0], self.np_img.shape[1], 1)).astype('uint8')

        if self.invert_output == True:
            self.np_img = normalize(255 - np.multiply(self.np_img_orig, selection, dtype="uint8"))
        else:
            self.np_img = np.multiply(self.np_img_orig, selection, dtype="uint8")

        self.redraw()

    def save_button(self):
        directory = path.dirname(self.filename)
        filename, extension = path.basename(self.filename).split(".")
        new_file_name = path.join(directory, filename + "-_colored" + "." + extension)
        # convert before saving
        self.np_img = np.array(cv2.cvtColor(self.np_img, cv2.COLOR_BGR2RGB))
        cv2.imwrite(new_file_name, self.np_img)
        # convert after saving so next phase gets correct image
        self.np_img = np.array(cv2.cvtColor(self.np_img, cv2.COLOR_RGB2BGR))
        self.filename = new_file_name
        print(new_file_name)

    # def transform_button(self):
    #     can_h = self.canvas.winfo_height()
    #     can_w = self.canvas.winfo_width()
    #     img_w = self.np_img.shape[1]
    #     img_h = self.np_img.shape[0]
    #     print(self.np_img.shape, ":", img_w, img_h, can_w, can_h)
    #
    #     pts1 = np.float32(self.points)
    #     pts2 = np.float32([[0, 0], [img_w, 0], [img_w, img_h], [0, img_h]])
    #
    #     matrix = cv2.getPerspectiveTransform(pts1, pts2)
    #     warped = cv2.warpPerspective(self.np_img, matrix, (img_w, img_h))
    #     resized = cv2.resize(warped, (int(can_w), int(can_h)))
    #     resized_photoimage = np_photo_image(resized)
    #
    #     self.np_img = resized
    #     self.photo_image = resized_photoimage
    #     self.canvas.create_image(0, 0, anchor=tk.NW, image=resized_photoimage)
    #     print(self.master.winfo_height())
    #
    #     self.points = []
    #     self.cursor_oval_handles = []
    #     self.line_handles = []

    # def canvas_2_img_pt(self, canvas_pt: list):
    #     img_x = canvas_pt[0] / self.canvas.winfo_width() * self.np_img.shape[1]
    #     img_y = canvas_pt[1] / self.canvas.winfo_height() * self.np_img.shape[0]
    #     return [img_x, img_y]

    # def record_pt(self, canvas_pt: list):
    #     img_x, img_y = self.canvas_2_img_pt(canvas_pt)
    #     if self.points.__len__() != 4:
    #         self.points.append([img_x, img_y])
    #     else:
    #         self.points = []
    #         self.points.append([img_x, img_y])

    # def canvas_click(self, event):
    #     self.record_pt([event.x, event.y])
    #     self.newest_pt_idx = len(self.points) - 1
    #     self.line_handles.append(None)
    #
    #     # will happen when len(self.points) >= 2
    #     if self.newest_pt_idx >= 0:
    #         pt1 = self.photo_image_2_canvas_pt(self.points[self.newest_pt_idx])
    #         pt2 = self.photo_image_2_canvas_pt(self.points[self.newest_pt_idx - 1])
    #         if self.line_handles[self.newest_pt_idx] is None:
    #             # b,c,d,e =
    #             self.line_handles[self.newest_pt_idx] = self.canvas.create_line([pt1[0], pt1[1], pt2[0], pt2[1]],
    #                                                                             fill="#ffff00")
    #             if self.newest_pt_idx == 2:
    #                 pt3 = self.photo_image_2_canvas_pt(self.points[0])
    #                 self.line_handles.append(self.canvas.create_line([pt1[0], pt1[1], pt3[0], pt3[1]], fill="#ffff00"))

    #def canvas_mouseover(self, event):
         ## create elements needed
     #    if len(self.cursor_oval_handles) < len(self.points) + 1:
      #       o_size = 5
       #      x = event.x
        #     y = event.y
         #    oval = [x - o_size, y - o_size, x + o_size, y + o_size]
          #   self.cursor_oval_handles.append(self.canvas.create_oval(*oval))

         ## move oval to cursor if needed
         #if self.newest_pt_idx < 3:
          #   pt1 = [event.x, event.y]
           #  o_size = 5
            # oval = [pt1[0] - o_size, pt1[1] - o_size, pt1[0] + o_size, pt1[1] + o_size]
             #self.canvas.coords(self.cursor_oval_handles[-1], oval)

         ## draw line to cursor if needed
         #if (self.newest_pt_idx >= 0) and (self.newest_pt_idx < 2):
             # pt1 = self.photo_image_2_canvas_pt(self.points[self.newest_pt_idx])
             # pt2 = [event.x, event.y]
             # o_size = 5
             # x = event.x
             # y = event.y
             # oval = [x - o_size, y - o_size, x + o_size, y + o_size]
         #     self.canvas.coords(self.line_handles[self.newest_pt_idx], [pt1[0], pt1[1], pt2[0], pt2[1]])
         #
         # elif self.newest_pt_idx == 2:
         #     pt1 = self.photo_image_2_canvas_pt(self.points[2])
         #     pt2 = [event.x, event.y]
         #     pt3 = self.photo_image_2_canvas_pt(self.points[0])
         #     o_size = 5
         #     x = event.x
         #     y = event.y
         #     oval = [x - o_size, y - o_size, x + o_size, y + o_size]
         #     self.canvas.coords(self.line_handles[2], [pt1[0], pt1[1], pt2[0], pt2[1]])
         #     self.canvas.coords(self.line_handles[3], [pt3[0], pt3[1], pt2[0], pt2[1]])

    # def update_lines(self, cursor_x, cursor_y):
    #     last_point = self.points[-1]
    #
    #     if len(self.points) == 0:
    #         pass
    #
    #     if len(self.points) == 1:
    #         pass
    #         pt1 = self.photo_image_2_canvas_pt(self.points[0])
    #         pt2 = [curosor_x, curosor_y]
    #         if self.line_handles.__len__() < 1:
    #             self.line_handles.append(self.canvas.create_line(pt1, pt2, fill="#ffff00"))
    #         self.canvas.coords(self.line_handles[0], [pt1[0], pt1[1], pt2[0], pt2[1]])
    #
    #     if len(self.points) == 2:
    #         pt1 = self.photo_image_2_canvas_pt(self.points[1])
    #         pt2 = [curosor_x, curosor_y]
    #         if self.line_handles.__len__() < 2:
    #             self.line_handles.append(self.canvas.create_line(pt1, pt2, fill="#ffff00"))
    #
    #         self.canvas.coords(self.line_handles[0], [pt1[0], pt1[1], pt2[0], pt2[1]])
    #
    #     if len(self.points) == 3:
    #         pt1 = self.photo_image_2_canvas_pt(self.points[2])
    #         pt2 = [curosor_x, curosor_y]
    #         if self.line_handles.__len__() < 3:
    #             self.line_handles.append(self.canvas.create_line(pt1, pt2, fill="#ffff00"))
    #
    #         self.canvas.coords(self.line_handles[0], [pt1[0], pt1[1], pt2[0], pt2[1]])
    #
    #     if len(self.points) == 4:
    #         for i, pt in enumerate(self.points):
    #             pt = self.photo_image_2_canvas_pt()
    #             self.canvas.coords(self.line_handles[i - 1], [pt1[i - 1], pt1[i], pt[i], pt[i]])

    # def img_2_canvas_pt(self, pt: list):
    #     x = (pt[0] / self.np_img.shape[1]) * self.canvas.winfo_width()
    #     y = (pt[1] / self.np_img.shape[0]) * self.canvas.winfo_height()
    #     return ([x, y])


if __name__ == "__main__":
    root = tk.Tk()
    # Resize the display window
    root.geometry("800x1000")
    app = Application(master=root, next_phase=None)
    app.mainloop()
