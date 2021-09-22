"""
This module's purpose is to provide a UI to help with creating/expanding the dataset
Specifically the story_photo_transformer.py script will allow the user to pick a photo and define where the corners of
the body of text is, then the script will transform the image in preparation for further processing

image will be saved with _transformed appended before the file extension
"""

import numpy as np
import os.path as path
import tkinter as tk

import cv2
from phase_tkinter_class import PipelinePhase
from phase_tkinter_class import np_photo_image
from enum import IntFlag, auto


class Application(PipelinePhase):
    def __init__(self, next_phase, master=None, prev_phase: PipelinePhase = None):
        super().__init__(next_phase, master=master, prev_phase=prev_phase)

        class States(IntFlag):
            choose_file = auto()
            specify_points = auto()
            modify_points = auto()
            saved = auto()
            modified = auto()

        self.states = States
        self.state = States.choose_file

        self.np_img_points = [[]] * 4
        self.current_np_img_point_idx = 0

        self.state = set()
        self.state.add(States.specify_points)
        self.state.add(States.saved)

        self.create_widgets()

    def create_widgets(self):
        self.transform_btn = tk.Button(self)
        self.transform_btn["text"] = "Transform"
        self.transform_btn["command"] = self.transform_button
        self.transform_btn.pack(side="top")

        self.save_btn = tk.Button(self)
        self.save_btn["text"] = "Save"
        self.save_btn["command"] = self.save_button
        self.save_btn.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.next_phase_btn = tk.Button(self)
        self.next_phase_btn["text"] = "Next Phase"
        self.next_phase_btn["command"] = self.next_phase_button
        self.next_phase_btn.pack(side="right")

        self.line_handles = [self.canvas.create_line([0, 0, 0, 0], fill="#ffff00") for i in range(4)]
        self.cursor_oval_handles = [self.canvas.create_oval([-10, -10, 10, 10], fill="#ffff00") for i in range(4)]
        self.image_handle = None

    def next_phase_button(self):
        self.goto_next_phase_flag = True
        command = self.master.destroy()

    def save_button(self):
        directory = path.dirname(self.filename)
        filename, extension = path.basename(self.filename).split(".")
        new_file_name = path.join(directory, filename + "-transformed" + "." + extension)
        # convert before saving
        self.np_img = np.array(cv2.cvtColor(self.np_img, cv2.COLOR_BGR2RGB))
        cv2.imwrite(new_file_name, self.np_img)
        # convert after saving so next phase gets correct image
        self.np_img = np.array(cv2.cvtColor(self.np_img, cv2.COLOR_RGB2BGR))
        self.filename = new_file_name
        print(new_file_name)

    def transform_button(self):
        can_h = self.canvas.winfo_height()
        can_w = self.canvas.winfo_width()
        img_w = self.np_img.shape[1]
        img_h = self.np_img.shape[0]
        print(self.np_img.shape, ":", img_w, img_h, can_w, can_h)

        pts1 = np.float32(self.np_img_points)
        pts2 = np.float32([[0, 0], [img_w, 0], [img_w, img_h], [0, img_h]])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        warped = cv2.warpPerspective(self.np_img, matrix, (img_w, img_h))
        resized = cv2.resize(warped, (int(can_w), int(can_h)))
        resized_photoimage = np_photo_image(resized)

        self.np_img = resized
        self.photo_image = resized_photoimage
        self.canvas.create_image(0, 0, anchor=tk.NW, image=resized_photoimage)
        print(self.master.winfo_height())

        self.np_img_points = []
        self.cursor_oval_handles = []
        self.line_handles = []

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
        if self.states.specify_points in self.state:
            self.record_pt([event.x, event.y])

            # part one of line drawing, other part is handled by canvas_mouseover
            pairs = [[0, 1], [1, 2], [2, 3], [3, 0]]
            for pt1_idx, pt2_idx in pairs:
                if (pt1_idx < self.current_np_img_point_idx) & (pt2_idx < self.current_np_img_point_idx):
                    pt1 = self.img_2_canvas_pt(self.np_img_points[pt1_idx])
                    pt2 = self.img_2_canvas_pt(self.np_img_points[pt2_idx])
                    self.canvas.coords(self.line_handles[pt1_idx], *(pt1 + pt2))

    def canvas_mouseover(self, event):

        # move oval to cursor if needed
        if self.current_np_img_point_idx < 4:
            pt1 = [event.x, event.y]
            o_size = 5
            oval = [pt1[0] - o_size, pt1[1] - o_size, pt1[0] + o_size, pt1[1] + o_size]
            self.canvas.coords(self.cursor_oval_handles[self.current_np_img_point_idx], oval)

        # draw line to cursor if needed
        if (self.current_np_img_point_idx > 0) and (self.current_np_img_point_idx < 3):
            pt1 = self.img_2_canvas_pt(self.np_img_points[self.current_np_img_point_idx - 1])
            pt2 = [event.x, event.y]
            o_size = 5
            x = event.x
            y = event.y
            oval = [x - o_size, y - o_size, x + o_size, y + o_size]
            self.canvas.coords(self.line_handles[self.current_np_img_point_idx - 1], [pt1[0], pt1[1], pt2[0], pt2[1]])

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


if __name__ == "__main__":
    import story_image_clip
    import story_photo_GUI_grayscale
    import story_photo_GUI_backandwhite
    import story_photo_removelines

    phase_list = [Application, story_image_clip, story_photo_GUI_grayscale, story_photo_GUI_backandwhite,
                  story_photo_removelines]

    first = True
    root = tk.Tk()
    root.geometry("800x1000")
    app = Application(master=root, next_phase=None)

    for app_to_run in phase_list:
        if app.goto_next_phase_flag or first:
            if not first:
                last_phase = app
                root = tk.Tk()
                app = app_to_run.Application(master=root, next_phase=None, prev_phase=last_phase)
                # Resize the display window
                root.geometry("800x1000")

            app.mainloop()  # this call is "blocking"
            first = False
