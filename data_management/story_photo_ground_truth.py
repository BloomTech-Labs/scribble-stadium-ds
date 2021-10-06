import tkinter as tk
from enum import IntFlag, auto

import cv2
import numpy as np

from data_management.phase_tkinter_class import PipelinePhase
from data_management.phase_tkinter_class import np_photo_image


class Application(PipelinePhase):
    """
    This Class's purpose is to provide a UI to help with creating/expanding the dataset.
    Specifically the story_photo_transformer.py script will allow the user to pick a photo and define where the corners
    of the body of text are, then the script will transform the image in preparation for further processing
    image will be saved in phase directory in the same location as the imported image.
    """

    def __init__(self, next_phase, master=None, prev_phase: PipelinePhase = None):
        super().__init__(next_phase, master=master, prev_phase=prev_phase)
        print(__name__)
        self.phase = "phase0"

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
        """
        This function creates the widgets for the UI and default canvas widgets
        :return: None
        """

        self.save_btn = tk.Button(self.controls_frame)
        self.save_btn["text"] = "Save"
        self.save_btn["command"] = self.save_text
        self.save_btn.pack(side="top")

        self.quit = tk.Button(self.controls_frame, text="QUIT", fg="red", command=self.destroy)
        self.quit.pack(side="bottom")

        self.next_phase_btn = tk.Button(self.controls_frame)
        self.next_phase_btn["text"] = "Next Phase"
        self.next_phase_btn["command"] = self.next_phase_button
        self.next_phase_btn.pack(side="right")


    def save_text(self):
        pass

    def next_phase_button(self):
        pass


if __name__ == "__main__":

    root = tk.Tk()
    root.geometry("800x1000")  # this can be changed per your screen size
    app = Application(master=root, next_phase=None)
    app.mainloop()  # this call is "blocking"