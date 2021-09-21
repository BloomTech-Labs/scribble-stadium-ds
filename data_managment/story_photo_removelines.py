"""
This module's purpose is to provide a UI to help with creating/expanding the dataset
Specifically the story_photo_GUI_template.py script will allow the user to pick a photo and export a modified
version of the photo used for further processing. This template will also act as a base template for other
transformations required in the future.

image will be saved with _template appended before the file extension

#1 sharpen image
#2 change it image to black and white
#3 remove horizontal lines
#4 use denoising autoencoder to remove background noise

at the moment this phase is taking in a B&W image
"""

import numpy as np
import os.path as path
import tkinter as tk
from tkinter import filedialog as fd
import cv2


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


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.filename = fd.askopenfilename(
            initialdir=path.join(path.dirname(__file__), "..", "data", "transcribed_stories", "51--", "5101"))
        self.np_img = np.array(cv2.imread(self.filename,cv2.IMREAD_UNCHANGED)) #removed cv2.color #added cv2 imread_unchanged
        #self.np_img = np.array (cv2.cvtColor (cv2.imread (self.filename), cv2.COLOR_RGB2BGR))
        self.img = np_photo_image(self.np_img)
        self.points = []
        self.cursor_oval_handles = []
        self.line_handles = []
        self.create_widgets()
        self.newest_pt_idx = -1
        # self.cursor

        print(self.filename)

    def create_widgets(self):
        self.transform_btn = tk.Button(self)
        self.transform_btn["text"] = "lines_removed"
        self.transform_btn["command"] = self.removeLines_button
        self.transform_btn.pack(side="top")

        self.save_btn = tk.Button(self)
        self.save_btn["text"] = "save"
        self.save_btn["command"] = self.save_button
        self.save_btn.pack(side="top")

        # Next Phase button
        self.next_phase_btn = tk.Button(self)
        self.next_phase_btn["text"] = "Next Phase"
        self.next_phase_btn["command"] = self.next_phase_button
        self.next_phase_btn.pack(side="right")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.canvas = tk.Canvas()
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(8, 8, anchor=tk.NW, image=self.img)
        self.canvas.bind('<Configure>', self.resize)
        # self.canvas.bind("<Button-1>", self.canvas_click)
        # self.canvas.bind("<Motion>", self.canvas_mouseover)

        self.image_handle = None

    def next_phase_button(self):
        self.goto_next_phase_flag = True
        command = self.master.destroy()

    def save_button(self):
        directory = path.dirname(self.filename)
        filename, extension = path.basename(self.filename).split(".")
        new_file_name = path.join(directory, filename + "-template" + "." + extension)
        cv2.imwrite(new_file_name, self.np_img)
        print(new_file_name)

    def removeLines_button(self):
        can_h = self.canvas.winfo_height()
        can_w = self.canvas.winfo_width()
        img_w = self.np_img.shape[1]
        img_h = self.np_img.shape[0]
        print(self.np_img.shape, ":", img_w, img_h, can_w, can_h)

        #review grayscale and B&W scale parameters line 82, 85
        #if len(self.np_img.shape) == 3:
            #print("image not in right scale")
            #exit()

        print (self.np_img.shape)
        #self.np_img = cv2.cvtColor (self.np_img, cv2.COLOR_BGR2GRAY)


        self.np_img = cv2.threshold (self.np_img, 127, 255, cv2.THRESH_BINARY)[1]

        print(self.np_img.shape)

        #thresh
        thresh = cv2.threshold (self.np_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Remove horizontal
        horizontal_kernel = cv2.getStructuringElement (cv2.MORPH_RECT, (25, 1))
        print (self.np_img.shape)
        detected_lines = cv2.morphologyEx (thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        cnts = cv2.findContours (detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len (cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours (self.np_img, [c], -1, (255, 255, 255), 2)

        print (self.np_img.shape)

        # Repair image
        repair_kernel = cv2.getStructuringElement (cv2.MORPH_RECT, (1, 6))
        self.np_img = 255 - cv2.morphologyEx (255 - self.np_img, cv2.MORPH_CLOSE, repair_kernel, iterations=1)

        #cv2.imshow (thresh)
        #cv2.imshow (detected_lines)
        #cv2.imshow (self.np_img)
        #cv2.imshow (result)


        self.resize (None)

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
    #     self.img = resized_photoimage
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
    #         pt1 = self.img_2_canvas_pt(self.points[self.newest_pt_idx])
    #         pt2 = self.img_2_canvas_pt(self.points[self.newest_pt_idx - 1])
    #         if self.line_handles[self.newest_pt_idx] is None:
    #             # b,c,d,e =
    #             self.line_handles[self.newest_pt_idx] = self.canvas.create_line([pt1[0], pt1[1], pt2[0], pt2[1]],
    #                                                                             fill="#ffff00")
    #             if self.newest_pt_idx == 2:
    #                 pt3 = self.img_2_canvas_pt(self.points[0])
    #                 self.line_handles.append(self.canvas.create_line([pt1[0], pt1[1], pt3[0], pt3[1]], fill="#ffff00"))

    # def canvas_mouseover(self, event):
    #     ## create elements needed
    #     if len(self.cursor_oval_handles) < len(self.points) + 1:
    #         o_size = 5
    #         x = event.x
    #         y = event.y
    #         oval = [x - o_size, y - o_size, x + o_size, y + o_size]
    #         self.cursor_oval_handles.append(self.canvas.create_oval(*oval))
    #
    #     ## move oval to cursor if needed
    #     if self.newest_pt_idx < 3:
    #         pt1 = [event.x, event.y]
    #         o_size = 5
    #         oval = [pt1[0] - o_size, pt1[1] - o_size, pt1[0] + o_size, pt1[1] + o_size]
    #         self.canvas.coords(self.cursor_oval_handles[-1], oval)
    #
    #     ## draw line to cursor if needed
    #     if (self.newest_pt_idx >= 0) and (self.newest_pt_idx < 2):
    #         pt1 = self.img_2_canvas_pt(self.points[self.newest_pt_idx])
    #         pt2 = [event.x, event.y]
    #         o_size = 5
    #         x = event.x
    #         y = event.y
    #         oval = [x - o_size, y - o_size, x + o_size, y + o_size]
    #         self.canvas.coords(self.line_handles[self.newest_pt_idx], [pt1[0], pt1[1], pt2[0], pt2[1]])
    #
    #     elif self.newest_pt_idx == 2:
    #         pt1 = self.img_2_canvas_pt(self.points[2])
    #         pt2 = [event.x, event.y]
    #         pt3 = self.img_2_canvas_pt(self.points[0])
    #         o_size = 5
    #         x = event.x
    #         y = event.y
    #         oval = [x - o_size, y - o_size, x + o_size, y + o_size]
    #         self.canvas.coords(self.line_handles[2], [pt1[0], pt1[1], pt2[0], pt2[1]])
    #         self.canvas.coords(self.line_handles[3], [pt3[0], pt3[1], pt2[0], pt2[1]])

    # def update_lines(self, curosor_x, curosor_y):
    #     last_point = self.points[-1]
    #
    #     if len(self.points) == 0:
    #         pass
    #
    #     if len(self.points) == 1:
    #         pass
    #         pt1 = self.img_2_canvas_pt(self.points[0])
    #         pt2 = [curosor_x, curosor_y]
    #         if self.line_handles.__len__() < 1:
    #             self.line_handles.append(self.canvas.create_line(pt1, pt2, fill="#ffff00"))
    #         self.canvas.coords(self.line_handles[0], [pt1[0], pt1[1], pt2[0], pt2[1]])
    #
    #     if len(self.points) == 2:
    #         pt1 = self.img_2_canvas_pt(self.points[1])
    #         pt2 = [curosor_x, curosor_y]
    #         if self.line_handles.__len__() < 2:
    #             self.line_handles.append(self.canvas.create_line(pt1, pt2, fill="#ffff00"))
    #
    #         self.canvas.coords(self.line_handles[0], [pt1[0], pt1[1], pt2[0], pt2[1]])
    #
    #     if len(self.points) == 3:
    #         pt1 = self.img_2_canvas_pt(self.points[2])
    #         pt2 = [curosor_x, curosor_y]
    #         if self.line_handles.__len__() < 3:
    #             self.line_handles.append(self.canvas.create_line(pt1, pt2, fill="#ffff00"))
    #
    #         self.canvas.coords(self.line_handles[0], [pt1[0], pt1[1], pt2[0], pt2[1]])
    #
    #     if len(self.points) == 4:
    #         for i, pt in enumerate(self.points):
    #             pt = self.img_2_canvas_pt()
    #             self.canvas.coords(self.line_handles[i - 1], [pt1[i - 1], pt1[i], pt[i], pt[i]])

    # def img_2_canvas_pt(self, pt: list):
    #     x = (pt[0] / self.np_img.shape[1]) * self.canvas.winfo_width()
    #     y = (pt[1] / self.np_img.shape[0]) * self.canvas.winfo_height()
    #     return ([x, y])

    def resize(self, event):
        w = self.canvas.winfo_height()
        h = self.canvas.winfo_width()
        self.img = np_photo_image(cv2.resize(self.np_img, (h, w)))

        if not self.image_handle:
            self.image_handle = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
        else:
            # if (self.img.width() != w) or (self.img.height() != h):
            # self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
            self.canvas.itemconfig(self.image_handle, image=self.img)
        self.canvas.update()
        # self.paint()

if __name__ == "__main__":
    root = tk.Tk()
    # Resize the display window
    root.geometry("800x1000")
    app = Application(master=root, next_phase=None)
    app.mainloop()
