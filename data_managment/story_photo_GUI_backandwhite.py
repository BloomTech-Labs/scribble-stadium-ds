"""
This module's purpose is to open the image in it's original format and display through
a tkinter application and further enable the user to see the same image in a
grayscale format. Finally the image can be saved in the same directory
as that of the image as grayscale.

image will be saved with _grayscale appended before the file extension
"""

import numpy as np
import os.path as path
import tkinter as tk
import os.path as path
import tkinter as tk
from tkinter import filedialog as fd
import cv2
from phase_tkinter_class import PipelinePhase
from phase_tkinter_class import np_photo_image


class Application(PipelinePhase):
    def __init__(self, next_phase, master=None, prev_phase: PipelinePhase = None):
        super().__init__(next_phase, master=master, prev_phase=prev_phase)

        # Convert image to Black and White
        self.im_gray = cv2.imread(self.filename, cv2.IMREAD_GRAYSCALE)
        (thresh, self.np_img_bw) = cv2.threshold(self.im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        self.points = []
        self.cursor_oval_handles = []
        self.line_handles = []
        self.create_widgets()
        self.newest_pt_idx = -1
        # self.cursor

        print(self.filename)

    def create_widgets(self):

        # Show button to convert to Black and White
        self.show_as_bw = tk.Button(self)
        self.show_as_bw["text"] = "Show as Black and White"
        self.show_as_bw["command"] = self.show_as_bw_button
        self.show_as_bw.pack(side="left")

        # Save Button for Black and White
        self.save_btn_bw = tk.Button(self)
        self.save_btn_bw["text"] = "Save as Black and White"
        self.save_btn_bw["command"] = self.save_button_bw
        self.save_btn_bw.pack(side="left")

        # Next Phase button
        self.next_phase_btn = tk.Button(self)
        self.next_phase_btn["text"] = "Next Phase"
        self.next_phase_btn["command"] = self.next_phase_button
        self.next_phase_btn.pack(side="right")

        # Quit Button
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="right")

        # canvas
        self.canvas = tk.Canvas()
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(8, 8, anchor=tk.NW, image=self.photo_image)
        self.canvas.bind('<Configure>', self.resize)
        # self.canvas.bind("<Button-1>", self.canvas_click)
        # self.canvas.bind("<Motion>", self.canvas_mouseover)

        self.image_handle = None

    def next_phase_button(self):
        self.goto_next_phase_flag = True
        command = self.master.destroy()

    def save_button_bw(self):
        """
        Save Button Grayscale to save file as Grayscale in file path directory
        :return: None
        """
        directory = path.dirname(self.filename)
        filename, extension = path.basename(self.filename).split(".")
        if "jpg" in extension:
            extension = "png"
        new_file_name = path.join(directory, filename + "-bw" + "." + extension)
        cv2.imwrite(new_file_name, self.np_img_bw)
        self.filename = new_file_name
        print('File saved as Black and White, path -->', new_file_name)

    def show_as_bw_button(self):
        """
        Transform Button to open image as Grayscale
        :return: None
        """
        print('Black and White Button Pressed')
        self.im_gray = cv2.imread(self.filename, cv2.IMREAD_GRAYSCALE)
        (thresh, self.np_img) = cv2.threshold(self.im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # self.np_img = cv2.cvtColor(self.np_img, cv2.COLOR_BGR2GRAY)
        # self.np_img = cv2.cvtColor(self.np_img, cv2.THRESH_BINARY)
        self.resize(None)

    def resize(self, event):
        w = self.canvas.winfo_height()
        h = self.canvas.winfo_width()
        self.photo_image = np_photo_image(cv2.resize(self.np_img, (h, w)))

        if not self.image_handle:
            self.image_handle = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
        else:
            self.canvas.itemconfig(self.image_handle, image=self.photo_image)
        self.canvas.update()


if __name__ == "__main__":
    root = tk.Tk()
    # Resize the display window
    root.geometry("800x1000")
    app = Application(master=root, next_phase=None)
    app.mainloop()
