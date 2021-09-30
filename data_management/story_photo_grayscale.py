"""
This module's purpose is to open the image in it's original format and display through
a tkinter application and further enable the user to see the same image in a
grayscale format. Finally the image can be saved in the same directory
as that of the image as grayscale.

image will be saved with _grayscale appended before the file extension
"""
from os import path
import cv2
import numpy as np
import tkinter as tk
from data_management.phase_tkinter_class import PipelinePhase

class Application(PipelinePhase):
    def __init__(self, next_phase, master=None, prev_phase: PipelinePhase = None):
        super().__init__(next_phase, master=master, prev_phase=prev_phase)
        self.phase="phase3"

        # Convert image to grayscale
        print(self.np_img,self.np_img.shape)
        self.np_img=self.np_img.astype("uint8")
        self.np_img_grayscale = np.array(cv2.cvtColor(self.np_img, cv2.COLOR_BGR2GRAY))

        self.points = []
        self.cursor_oval_handles = []
        self.line_handles = []
        self.goto_next_phase_flag = None
        self.create_widgets()
        self.newest_pt_idx = -1
        # self.cursor

        print(self.filename)

    def create_widgets(self):
        self.show_as_grayscale = tk.Button(self.controls_frame)
        self.show_as_grayscale["text"] = "Show as Grayscale"
        self.show_as_grayscale["command"] = self.show_as_grayscale_button
        self.show_as_grayscale.pack(side="top")

        # Save Button for Gray Scale
        self.save_btn_grayscale = tk.Button(self.controls_frame)
        self.save_btn_grayscale["text"] = "Save as GrayScale"
        self.save_btn_grayscale["command"] = self.save_button_grayscale
        self.save_btn_grayscale.pack(side="top")

        # Quit Button
        self.quit = tk.Button(self.controls_frame, text="QUIT", fg="red", command=self.destroy)
        self.quit.pack(side="bottom")

        # Next Phase Button
        self.next_phase_btn = tk.Button(self.controls_frame)
        self.next_phase_btn["text"] = "Next Phase"
        self.next_phase_btn["command"] = self.next_phase_button
        self.next_phase_btn.pack(side="right")

        self.image_handle = None

    def next_phase_button(self):
        self.goto_next_phase_flag = True
        command = self.master.destroy()

    def save_button_grayscale(self):
        """
        Save Button Grayscale to save file as Grayscale
        :return: None
        """
        self.np_img = self.np_img_grayscale
        self.save_button()

    def show_as_grayscale_button(self):
        """
        Transform Button to open image as Grayscale
        :return: None
        """
        print('Button Pressed')
        self.np_img = cv2.cvtColor(self.np_img, cv2.COLOR_BGR2GRAY)
        self.redraw()

if __name__ == "__main__":
    root = tk.Tk()
    # Resize the display window
    root.geometry("800x1000")
    app = Application(master=root, next_phase=None)
    app.mainloop()
