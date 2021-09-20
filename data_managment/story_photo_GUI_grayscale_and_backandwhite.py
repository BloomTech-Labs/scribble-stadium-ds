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
        self.np_img = np.array(cv2.cvtColor(cv2.imread(self.filename), cv2.COLOR_RGB2BGR))
        self.img = np_photo_image(self.np_img)

        # Convert image to grayscale
        self.np_img_grayscale = np.array(cv2.cvtColor(cv2.imread(self.filename), cv2.COLOR_BGR2GRAY))

        # Convert image to Black and White
        self.im_gray = cv2.imread(self.filename, cv2.IMREAD_GRAYSCALE)
        (thresh, self.np_img_bw) = cv2.threshold(self.im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # self.np_img_bw = cv2.threshold(self.im_gray, thresh, 255, cv2.THRESH_BINARY)[1]

        self.points = []
        self.cursor_oval_handles = []
        self.line_handles = []
        self.create_widgets()
        self.newest_pt_idx = -1
        # self.cursor

        print(self.filename)

    def create_widgets(self):
        self.show_as_grayscale = tk.Button(self)
        self.show_as_grayscale["text"] = "Show as Grayscale"
        self.show_as_grayscale["command"] = self.show_as_grayscale_button
        self.show_as_grayscale.pack(side="left")

        # Show button to convert to Black and White
        self.show_as_bw = tk.Button(self)
        self.show_as_bw["text"] = "Show as Black and White"
        self.show_as_bw["command"] = self.show_as_bw_button
        self.show_as_bw.pack(side="left")

        # Save Button for Gray Scale
        self.save_btn_grayscale = tk.Button(self)
        self.save_btn_grayscale["text"] = "Save as GrayScale"
        self.save_btn_grayscale["command"] = self.save_button_grayscale
        self.save_btn_grayscale.pack(side="left")

        # Save Button for Black and White
        self.save_btn_bw = tk.Button(self)
        self.save_btn_bw["text"] = "Save as Black and White"
        self.save_btn_bw["command"] = self.save_button_bw
        self.save_btn_bw.pack(side="left")

        # Quit Button
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="right")

        # canvas
        self.canvas = tk.Canvas()
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(8, 8, anchor=tk.NW, image=self.img)
        self.canvas.bind('<Configure>', self.resize)
        # self.canvas.bind("<Button-1>", self.canvas_click)
        # self.canvas.bind("<Motion>", self.canvas_mouseover)

        self.image_handle = None

    def save_button_grayscale(self):
        """
        Save Button Grayscale to save file as Grayscale in file path directory
        :return: None
        """
        directory = path.dirname(self.filename)
        filename, extension = path.basename(self.filename).split(".")
        if "jpg" in extension:
            extension = "png"
        new_file_name = path.join(directory, filename + "-grayscale" + "." + extension)
        cv2.imwrite(new_file_name, self.np_img_grayscale)
        print('File saved as grayscale, path -->', new_file_name)

    def show_as_grayscale_button(self):
        """
        Transform Button to open image as Grayscale
        :return: None
        """
        print('Grayscale Button Pressed')
        self.np_img = cv2.cvtColor(self.np_img, cv2.COLOR_BGR2GRAY)
        self.resize(None)

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
        self.img = np_photo_image(cv2.resize(self.np_img, (h, w)))

        if not self.image_handle:
            self.image_handle = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
        else:
            self.canvas.itemconfig(self.image_handle, image=self.img)
        self.canvas.update()


if __name__ == "__main__":
    root = tk.Tk()
    # Resize the display window
    root.geometry("800x1000")
    app = Application(master=root)
    app.mainloop()
