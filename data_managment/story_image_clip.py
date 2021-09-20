"""
This modules purpose is to clip out inline images and other art surrounded by hand written text and save them
"""

import numpy as np
import os.path as path
import tkinter as tk
from tkinter import filedialog as fd
import cv2
import os
import glob
from enum import IntFlag,auto

def np_photo_image(image: np.ndarray):
    height, width, channels = image.shape
    data = f'P6 {width} {height} 255 '.encode() + image.astype(np.uint8).tobytes()
    return tk.PhotoImage(width=width, height=height, data=data, format='PPM')




class Application(tk.Frame):
    def __init__(self, next_phase,master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        class States(IntFlag):
            choose_file=auto()
            specify_points=auto()
            modify_points=auto()
            saved=auto()
            modified=auto()

        self.states = States
        self.state = States.choose_file

        self.filename = fd.askopenfilename(
            initialdir=path.join(path.dirname(__file__), "..", "data", "transcribed_stories", "51--","5101"))
        # correct path specifier
        self.filename = os.path.join(*self.filename.split("/"))
        self.filename = self.filename.replace(":", ":\\")
        self.photo_folder = os.path.dirname(self.filename)

        self.np_img = np.array(cv2.cvtColor(cv2.imread(self.filename), cv2.COLOR_RGB2BGR))
        self.img = np_photo_image(self.np_img)
        self.np_img_points = [[]] * 4
        self.current_np_img_point_idx = 0

        self.state = set()
        self.state.add(States.specify_points)
        self.state.add(States.saved)
        self.create_widgets()

    def create_widgets(self):
        self.transform_btn = tk.Button(self)
        self.transform_btn["text"] = "Clip"
        self.transform_btn["command"] = self.clip_button
        self.transform_btn.pack(side="top")

        self.save_btn = tk.Button(self)
        self.save_btn["text"] = "save"
        self.save_btn["command"] = self.save_button
        self.save_btn.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.canvas = tk.Canvas()
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(8, 8, anchor=tk.NW, image=self.img)

        self.canvas.bind('<Configure>', self.resize)
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<Motion>", self.canvas_mouseover)

        self.line_handles = [self.canvas.create_line([0,0,0,0], fill="#ffff00") for i in range(4)]
        self.cursor_oval_handles = [self.canvas.create_oval([-10,-10,10,10], fill="#ffff00") for i in range(4)]
        self.image_handle = None

    def save_button(self):
        directory = path.dirname(self.filename)
        filename, extension = path.basename(self.filename).split(".")
        new_file_name = path.join(directory, filename + "-clipped" + "." + extension)
        self.np_img = np.array(cv2.cvtColor(self.np_img, cv2.COLOR_BGR2RGB))
        cv2.imwrite(new_file_name, self.np_img)
        print(new_file_name)

    def get_next_clip_filename(self):
        tmp = os.path.join(self.photo_folder, "*-clip-*")
        clips = glob.glob(tmp)
        name, ext = os.path.splitext(os.path.basename(self.filename))

        if clips ==[]:
            ret_val =os.path.join(self.photo_folder,name+"-clip-00"+ext)
            print(ret_val)
            return ret_val
        else:
            clips.sort()
            path,ext = os.path.splitext(clips[-1])
            num = int(path[-2:])
            num=num+1
            if num <= 9 :
                num = "0"+str(num)
            else:
                num = str(num)


            retval = os.path.join(self.photo_folder,name+"-clip-"+num+ext)
            print(path, ext, num,retval)
            return retval

    def clip_button(self):

        def bounding_box(points):
            x_coordinates, y_coordinates = zip(*points)

            return [(
                    int(min(x_coordinates)),
                    int(min(y_coordinates))
                 ),(
                    int(max(x_coordinates)),
                    int(max(y_coordinates))
                )]
        box = bounding_box((self.np_img_points))

        # create a new np array for the mask, and for recieving the results of the masking
        new_img = 255 * np.zeros(shape=[box[1][1]-box[0][1], box[1][0]-box[0][0], 4], dtype=np.uint8)

        # cv2.fillPoly is particular about dtype
        pts = np.int32(np.array(self.np_img_points))

        # store the contents of the bounding box of the poly to clip
        clip = self.np_img[box[0][1]:box[1][1], box[0][0]:box[1][0]].copy()

        # remove the polygonal area where the image is from the working img of this phase
        cv2.fillPoly(self.np_img, [pts], (255, 255, 255))

        # translate the points to be relative to the new image
        pts = pts - [box[0][0],box[0][1]]

        clip = cv2.cvtColor(clip, cv2.COLOR_RGB2RGBA)
        clip = cv2.cvtColor(clip, cv2.COLOR_RGBA2BGRA)

        # create a mask in new_img
        cv2.fillPoly(new_img, [pts], (255, 255, 255,255))

        # mask and store result in new_img
        new_img=cv2.multiply(new_img/255.0,clip,dtype=8)

        file_name = self.get_next_clip_filename()
        cv2.imwrite(file_name,new_img)
        self.resize(None)

    def canvas_2_img_pt(self, canvas_pt: list):
        img_x = canvas_pt[0] / self.canvas.winfo_width() * self.np_img.shape[1]
        img_y = canvas_pt[1] / self.canvas.winfo_height() * self.np_img.shape[0]
        return [img_x, img_y]

    def record_pt(self, canvas_pt: list):
        """
        Record points the user has specified to the
        """

        print(self.np_img_points)
        img_x, img_y = self.canvas_2_img_pt(canvas_pt)
        self.np_img_points[self.current_np_img_point_idx] = [img_x, img_y]
        self.current_np_img_point_idx = self.current_np_img_point_idx + 1
        if self.current_np_img_point_idx == 4:
            self.state.remove(self.states.specify_points)
            self.state.add(self.states.modify_points)


    def canvas_click(self, event):
        if  self.states.specify_points in self.state:
            self.record_pt([event.x, event.y])

            # part one of line drawing, other part is handled by canvas_mouseover
            pairs=[[0,1],[1,2],[2,3],[3,0]]
            for pt1_idx,pt2_idx in pairs:
                if (pt1_idx < self.current_np_img_point_idx) & (pt2_idx < self.current_np_img_point_idx):
                    pt1 = self.img_2_canvas_pt(self.np_img_points[pt1_idx])
                    pt2 = self.img_2_canvas_pt(self.np_img_points[pt2_idx])
                    self.canvas.coords(self.line_handles[pt1_idx], * (pt1+pt2))


    def canvas_mouseover(self, event):

        ## move oval to cursor if needed
        if self.current_np_img_point_idx < 4:
            pt1 = [event.x, event.y]
            o_size = 5
            oval = [pt1[0] - o_size, pt1[1] - o_size, pt1[0] + o_size, pt1[1] + o_size]
            self.canvas.coords(self.cursor_oval_handles[self.current_np_img_point_idx], oval)


        ## draw line to cursor if needed
        if (self.current_np_img_point_idx > 0) and (self.current_np_img_point_idx < 3):
            pt1 = self.img_2_canvas_pt(self.np_img_points[self.current_np_img_point_idx-1])
            pt2 = [event.x, event.y]
            o_size = 5
            x = event.x
            y = event.y
            oval = [x - o_size, y - o_size, x + o_size, y + o_size]
            self.canvas.coords(self.line_handles[self.current_np_img_point_idx-1], [pt1[0], pt1[1], pt2[0], pt2[1]])

        elif self.current_np_img_point_idx == 3:
            pt1 = self.img_2_canvas_pt(self.np_img_points[2])
            pt2 = [event.x, event.y]
            pt3 = self.img_2_canvas_pt(self.np_img_points[0])
            o_size = 5
            x = event.x
            y = event.y
            oval = [x - o_size, y - o_size, x + o_size, y + o_size]
            self.canvas.coords(self.line_handles[2], [pt1[0], pt1[1], pt2[0], pt2[1]])
            self.canvas.coords(self.line_handles[3], [pt3[0], pt3[1], pt2[0], pt2[1]])

    def img_2_canvas_pt(self, pt: list):
        x = (pt[0] / self.np_img.shape[1]) * self.canvas.winfo_width()
        y = (pt[1] / self.np_img.shape[0]) * self.canvas.winfo_height()
        return ([x, y])

    def resize(self, event):
        w = self.canvas.winfo_height()
        h = self.canvas.winfo_width()
        self.img = np_photo_image(cv2.resize(self.np_img, (h, w)))

        if not self.image_handle:
            self.image_handle = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
            self.canvas.tag_lower(self.image_handle)
        else:
            self.canvas.itemconfig(self.image_handle, image=self.img)
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


if __name__== "__main__":
    root = tk.Tk()
    # Resize the display window
    root.geometry("800x1000")
    app = Application(master=root)
    app.mainloop()
