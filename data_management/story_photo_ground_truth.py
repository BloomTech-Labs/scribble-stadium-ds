import os
import tkinter as tk
from enum import IntFlag, auto

import cv2
import numpy as np
import glob
import os.path as path

import data_management.custom_tk_widgets
from data_management.phase_tkinter_class import PipelinePhase
from data_management.custom_tk_widgets import GroundTruthWidget
from functools import partial
from data_management.phase_tkinter_class import np_photo_image


class Application(PipelinePhase):
    """
    This Class's purpose is to provide a UI to help with creating/expanding the dataset.
    Specifically the story_photo_ground_truth.py script will allow the user to provide the ground truth/label
    for the handwritten lines or words provided by the photo segmentation phase.
    """

    def __init__(self, next_phase, master=None, prev_phase: PipelinePhase = None, *args, **kwargs):
        super().__init__(next_phase, master=master, prev_phase=prev_phase, *args, **kwargs)
        self.phase = "phase7"
        print("initializing, ", __name__, " as ", self.phase)

        # change default setup from PipelinePhase
        # self.canvas_frame.unbind('<Configure>')
        self.canvas.destroy()
        self.canvas_frame.destroy()

        self.create_widgets()

    def create_widgets(self):
        """
        This function creates the widgets for the UI
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
        self.create_ground_truth_widgets()

    def create_ground_truth_widgets(self):
        """for every detected clip create and populate the fields of a GroundTruthWidget"""
        # Nice scrollable frame
        # TODO: make frame scroll with mouse wheel
        self.ground_truth_widgets_frame = data_management.custom_tk_widgets.ScrollableFrame(self, borderwidth=5,
                                                                                            relief='sunken',
                                                                                            bg="#000000")
        # get every file in the phase folder and filter out any ground truth files
        path_to_clips = self.photo_image_folder
        tmp = glob.glob(path.join(path_to_clips, "*.*"))
        tmp = [fn for fn in tmp if "gt.txt" not in fn]

        # create a tuple with the needed information for the next step
        clips = []
        for i, f in enumerate(tmp):
            clip_base_name, clip_num, clip_base_ext, state = self.get_clip_state_from_fullpath(f)
            text = self.story_text.splitlines()[i]
            clips.append(
                (
                    int(clip_num),
                    f,
                    text
                )
            )
        clips.sort()

        # iterate over the tuples to create the widgets
        self.ground_truth_widgets = []
        for label, image_path, text in clips:
            new_widget = GroundTruthWidget(self.ground_truth_widgets_frame.scrollable_frame, label, image_path,
                                           borderwidth=5,
                                           relief='raised')

            new_widget.invalid_button["command"] = partial(self.button_invalid_event, new_widget)
            new_widget.done_button["command"] = partial(self.button_done_event, new_widget)

            new_widget.textbox.insert(1.0, text)

            new_widget.pack(expand=True, fill=tk.X)
            _, _, _, state = self.get_clip_state_from_fullpath(image_path)

            if "invalid" in state:
                self.__manage_button_toggle(new_widget.invalid_button)
            elif "valid" in state:
                self.__manage_button_toggle(new_widget.done_button, new_widget)
            else:
                pass
            self.ground_truth_widgets.append(new_widget)

        self.ground_truth_widgets_frame.pack(expand=True, fill="both")

    def __manage_button_toggle(self, button: tk.Button, widget: GroundTruthWidget):
        """manage the state of the UI by changing it to provide better feedback to the user based on what state each
        widget is in"""

        # because of some strangeness with "button.setvar" below, just read the state from the current relief style
        pressed = button["relief"] == tk.SUNKEN

        if "done" in button._name:
            pressed_color = "#99FF99"
            button_to_hide = widget.invalid_button
        else:
            pressed_color = "#FF9999"
            button_to_hide = widget.done_button

        if not pressed:
            button.config(relief=tk.SUNKEN, bg=pressed_color)
            button.setvar("pressed", True)
            button_to_hide.pack_forget()
        else:
            button.config(relief=tk.RAISED, bg="#AAAAAA")
            button.setvar("pressed", False)
            button_to_hide.pack()

    def button_done_event(self, widget: GroundTruthWidget):
        """fires when button done is pressed, calls events that change the filename/state on the filesystem"""
        self.__manage_button_toggle(widget.done_button, widget)
        pressed = widget.done_button["relief"] == tk.SUNKEN
        if pressed:
            self.set_clip_valid(widget)
        else:
            self.set_clip_unprocessed(widget)

    def button_invalid_event(self, widget: GroundTruthWidget):
        """fires when invalid button is pressed, calls events that change the filename/state on the filesystem"""
        self.__manage_button_toggle(widget.invalid_button, widget)
        pressed = widget.invalid_button["relief"] == tk.SUNKEN
        if pressed:
            self.set_clip_invalid(widget)
        else:
            self.set_clip_unprocessed(widget)

    def get_clip_state_from_fullpath(self, fullpath):
        """ return clip_base_name, clip_num, clip_base_ext, state
        This function is the master interpreter of what state a clip is in
        """

        if "-invalid" in fullpath:
            fullpath2 = fullpath.replace("-invalid", '')
            clip_split = fullpath2.split("-")
            clip_base_name = "-".join(clip_split[:-1])
            clip_num = clip_split[-1].split(".")[0]
            clip_base_ext = clip_split[-1].split(".")[-1]
            state = "invalid"

        elif "-valid" in fullpath:
            fullpath2 = fullpath.replace("-valid", '')
            clip_split = fullpath2.split("-")
            clip_base_name = "-".join(clip_split[:-1])
            clip_num = clip_split[-1].split(".")[0]
            clip_base_ext = clip_split[-1].split(".")[-1]
            state = "valid"
        else:
            clip_split = fullpath.split("-")
            clip_base_name, clip_num, clip_base_ext, state = "-".join(clip_split[:-1]), \
                                                             clip_split[-1].split(".")[0], \
                                                             clip_split[-1].split(".")[-1], \
                                                             "unprocessed"

        return clip_base_name, clip_num, clip_base_ext, state

    def set_clip_invalid(self, widget: GroundTruthWidget):
        """process to set a clip to invalid on the filesystem"""

        clip_base_name, clip_num, clip_base_ext, state = self.get_clip_state_from_fullpath(widget.image)
        new_name = clip_base_name + \
                   "-" + \
                   clip_num + \
                   "-invalid" + \
                   "." + \
                   clip_base_ext

        os.rename(widget.image, new_name)
        widget.image = new_name

    def set_clip_unprocessed(self, widget: GroundTruthWidget):
        """process to set a clip to unprocessed on the filesystem"""
        clip_base_name, clip_num, clip_base_ext, state = self.get_clip_state_from_fullpath(widget.image)
        new_name = clip_base_name + "-" + clip_num + "." + clip_base_ext
        os.rename(widget.image, new_name)
        widget.image = new_name

    def set_clip_valid(self, widget: GroundTruthWidget):
        """process to set a clip to VALID on the filesystem"""
        clip_base_name, clip_num, clip_base_ext, state = self.get_clip_state_from_fullpath(widget.image)
        new_name = clip_base_name + \
                   "-" + \
                   clip_num + \
                   "-valid" + \
                   "." + \
                   clip_base_ext

        os.rename(widget.image, new_name)
        widget.image = new_name

    def save_text(self):
        """create/update individual ground truth files, 1 for each clip"""
        for widget in self.ground_truth_widgets:
            text = widget.textbox.get(1.0, "end-1c")  # this means "character 1, row 0" "end of textbox minus one
            # character"
            image_full_path = widget.image
            _, _, _, state = self.get_clip_state_from_fullpath(image_full_path)
            if state == "valid":
                gt_file_name = path.splitext(image_full_path)[0] + ".gt.txt"
                print(gt_file_name, text)
                with open(gt_file_name, "w+t") as f:
                    f.write(text)

    def next_phase_button(self):
        """
        Sets a flag that helps in advancing to the next phase
        :return: None
        """
        self.goto_next_phase_flag = True
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x1000")  # this can be changed per your screen size
    root.after(10, lambda: root.update())
    app = Application(master=root, next_phase=None)
    app.pack(expand=True, fill="both")
    app.mainloop()  # this call is "blocking"
