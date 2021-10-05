import logging
import tkinter as tk
# import os
from os import path as path
import matplotlib.pyplot as plt
import cv2
import numpy as np

from data_management.phase_tkinter_class import PipelinePhase


class Application(PipelinePhase):
    """
    This class is an implimentation of PipelinePhase specifically this phase separates each individual line of writing
    from the photograph
    """

    def __init__(self, next_phase, master=None, prev_phase: PipelinePhase = None):
        super().__init__(next_phase, master=master, prev_phase=prev_phase)
        self.phase = "phase6"
        self.points = []
        self.cursor_oval_handles = []
        self.line_handles = []
        self.goto_next_phase_flag = None
        self.np_img_original = self.np_img.copy()
        self.np_img_segmented_lines_list = []
        self.create_widgets()
        self.newest_pt_idx = -1

    def create_widgets(self):
        """
        This function creates the widgets for the UI
        :return: None
        """
        self.alpha_widget = tk.Scale(self.controls_frame, from_=0, to=100, label="Gradient Spread",
                                     orient='horizontal')
        self.alpha_widget["command"] = self.button_segment_function
        self.alpha_widget.set(25)
        self.alpha_widget.pack()

        self.beta_widget = tk.Scale(self.controls_frame, from_=0, to=100, label="black amount",
                                    orient='horizontal')
        self.beta_widget["command"] = self.button_segment_function
        self.beta_widget.set(25)
        self.beta_widget.pack()

        self.button_segment = tk.Button(self.controls_frame)
        self.button_segment["text"] = "Segment lines"
        self.button_segment["command"] = self.button_segment_function
        self.button_segment.pack(side="top")

        self.button_save_segment = tk.Button(self.controls_frame)
        self.button_save_segment["text"] = "Save lines"
        self.button_save_segment["command"] = self.button_segment_save_function
        self.button_save_segment.pack()

        # Quit Button
        self.quit = tk.Button(self.controls_frame, text="QUIT", fg="red", command=self.destroy)
        self.quit.pack(side="left")

        # Next Phase Button
        self.next_phase_btn = tk.Button(self.controls_frame)
        self.next_phase_btn["text"] = "Next Phase"
        self.next_phase_btn["command"] = self.next_phase_button
        self.next_phase_btn.pack(side="right")

        self.image_handle = None

    def button_segment_save_function(self):
        for i, line_np_img in enumerate(self.np_img_segmented_lines_list):
            fn, ext = path.splitext(self.photo_image_filename_only)
            save_file = path.join(self.story_folder, self.phase, fn + "-" + str(i) + ".png")
            #print(save_file)
            cv2.imwrite(save_file, line_np_img)

    def next_phase_button(self):
        """
        Sets a flag that helps in advancing to the next phase
        :return: None
        """
        self.goto_next_phase_flag = True
        self.master.destroy()

    def smooth(self,y, box_pts=3):
        box = np.ones(box_pts) / box_pts
        y_smooth = np.convolve(y, box, mode='same')
        return y_smooth

    def button_segment_function(self, debug=False):
        """
        convert the photo into individual lines of written text
        :return: None
        """
        # reset saved lines from any previous segmentation to empty
        self.np_img_segmented_lines_list = []

        debug = False
        alpha = self.alpha_widget.get()
        alpha1 = 50 - (alpha / 2)
        alpha2 = 50 + (alpha / 2)

        beta = self.beta_widget.get()

        self.np_img = self.np_img_original.copy()

        # convert photo so that written text is 1 and background is 0
        inverted_binary = self.np_img == 0
        # get mean value of black pixels per row
        mean_y = inverted_binary.mean(axis=1)

        # keeping this in here for further experimentation later
        gradient_y = np.gradient(mean_y)

        # smooth the array so as to help capture letters that have more than one part like "i"
        mean_y_smoothed = self.smooth(mean_y, 10)

        # use the smoothed array to create a smoothed gradient, then further smooth it to help not cut lines of written
        # text off
        gradient_y_smoothed = np.gradient(self.smooth(mean_y_smoothed, 5))

        # segments are defined by rows of pixels that are likely not part of the writing.. these segmenting lines
        # are defined in this section

        # first every row whose mean value is less than the beta percentile of mean_y_smoothed is considered a
        # segmenting line
        segments = mean_y < np.percentile(mean_y_smoothed, beta)

        # next every row whose gradient is > alpha1 and < alpha2 is considered
        p1 = np.percentile(gradient_y_smoothed, alpha1)
        p2 = np.percentile(gradient_y_smoothed, alpha2)
        if debug:
            print (np.percentile(gradient_y_smoothed,50))

        # finally both conditions must be true in order to be considered as a segmenting row
        segments = (gradient_y_smoothed > p1) & (gradient_y_smoothed < p2) & segments

        # this section is a state machine, basically it tracks a state and iterates over the rows of the image to
        # make decisions about what to do about each row
        # states:
        # - stop;starting state, also if there is content to be appended to lines[] then append it
        # - new; create a new array for the current line of writing and append this line to it
        # - record; record the row of pixels/data to the current line of writing

        lines = []
        current_line_array = None
        state = "stop"
        for i, v in enumerate(segments):

            if debug:
                print("old state: ", state)

            if v == 1:  # border of handwriting
                if state == "record":
                    state = "stop"

            else:  # actual handwriting
                if state == "stop":
                    state = "new"

                elif state == "new":
                    state = "record"

            if state == "new":
                current_line_array = [self.np_img[i, :]]
            if state == "record":
                current_line_array.append(self.np_img[i, :])

            if state == "stop":
                if current_line_array != None:
                    if len(current_line_array) > 10:
                        lines.append(current_line_array)
                    current_line_array = None

            if debug:
                print("new state: ", state)
                if current_line_array != None:
                    print("current img size", len(current_line_array), " current row: ", i)

        if current_line_array != None:
            if len(current_line_array) > 10:
                lines.append(current_line_array)

        # this section handles the display of the individual lines of writing on the gui
        # clear the image
        self.np_img = np.ones(shape=(self.np_img.shape[0], self.np_img.shape[1] + 100)) * 128
        # iterate over lines and update self.np_img with the contents of just the handwriting lines as detected.
        # self.np_img is basically the backbuffer for the canvas as we have things set up so after the modifications
        # it is necessary to call self.redraw()

        y = 0
        for handwriting_line in lines:
            img = np.array(handwriting_line)

            self.np_img_segmented_lines_list.append(img)

            height = img.shape[0]
            self.np_img[y:y + height, 100:] = img

            # draw a graph of the image mean along axis 1
            img_mean = (255 - img).mean(axis=1)
            img_mean = img_mean - img_mean.min()
            img_mean_max = img_mean.max()
            img_mean = img_mean / img_mean_max
            img_mean = img_mean * 49.0
            img_mean = img_mean.astype("uint8")
            for ii, row in enumerate(img):
                part1 = [0] * img_mean[ii]
                part2 = [255] * (49 - len(part1))
                self.np_img[y + ii, :49] = part1 + part2

            # draw a graph of the abs gradient of the image mean along axis 1
            img_grad = np.abs(np.gradient(img_mean))
            # img_mean = img_mean - img_mean.min()
            img_grad_max = img_grad.max()
            img_grad = img_grad / img_grad_max
            img_grad = img_grad * 49.0
            img_grad = img_grad.astype("uint8")

            for ii, row in enumerate(img):
                part1 = [0] * img_grad[ii]
                part2 = [255] * (49 - len(part1))
                self.np_img[y + ii, 50:99] = part1 + part2

            # here draw a checkerboard pattern to show the user that this is a border section and not part of the
            # detected line of handwriting

            dither1 = [0, 1] * int(self.np_img.shape[1] / 2)
            dither2 = [1, 0] * int(self.np_img.shape[1] / 2)
            line1 = np.array(dither1) * 255
            line2 = np.array(dither2) * 255
            y = y + height

            try:
                self.np_img[y] = line1
                y = y + 1
                self.np_img[y] = line2
                y = y + 1
                self.np_img[y] = line1
            except IndexError as e:
                logging.warning("tried to write a background line past end of array")

        self.redraw()

if __name__ == "__main__":
    """allows the phase to be ran in stand-alone mode or pipeline mode"""
    root = tk.Tk()
    # Resize the display window
    root.geometry("800x1000")
    app = Application(master=root, next_phase=None)
    app.mainloop()
