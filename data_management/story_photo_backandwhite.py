import tkinter as tk

import cv2

from data_management.phase_tkinter_class import PipelinePhase


class Application(PipelinePhase):
    """
    This Class's purpose is to open the image in it's original format and display through
    a UI and further enable the user to see the same image in a black and white format.
    Finally the image can be saved in phase4 directory as that of the image in a black and white format.
    """

    def __init__(self, next_phase, master=None, prev_phase: PipelinePhase = None):
        super().__init__(next_phase, master=master, prev_phase=prev_phase)
        self.phase = "phase4"
        # Convert image to Black and White
        self.im_gray = cv2.imread(self.os_filename, cv2.IMREAD_GRAYSCALE)
        (thresh, self.np_img_bw) = cv2.threshold(self.im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        self.points = []
        self.cursor_oval_handles = []
        self.line_handles = []
        self.create_widgets()
        self.newest_pt_idx = -1

        print(self.os_filename)

    def create_widgets(self):
        """
        This function creates the widgets for the UI
        :return: None
        """
        # Show button to convert to Black and White
        self.show_as_bw = tk.Button(self.controls_frame)
        self.show_as_bw["text"] = "Show as Black and White"
        self.show_as_bw["command"] = self.show_as_bw_button
        self.show_as_bw.pack(side="top")

        # Save Button for Black and White
        self.save_btn_bw = tk.Button(self.controls_frame)
        self.save_btn_bw["text"] = "Save as Black and White"
        self.save_btn_bw["command"] = self.save_button_bw
        self.save_btn_bw.pack(side="top")

        # Next Phase button
        self.next_phase_btn = tk.Button(self.controls_frame)
        self.next_phase_btn["text"] = "Next Phase"
        self.next_phase_btn["command"] = self.next_phase_button
        self.next_phase_btn.pack(side="top")

        # Quit Button
        self.quit = tk.Button(self.controls_frame, text="QUIT", fg="red", command=self.destroy)
        self.quit.pack(side="bottom")

        self.image_handle = None

    def next_phase_button(self):
        """
        Sets a flag that helps in advancing to the next phase
        :return: None
        """
        self.goto_next_phase_flag = True
        self.master.destroy()

    def save_button_bw(self):
        """
        Save Button to save file as Black and White
        :return: None
        """
        self.np_img = self.np_img_bw
        self.save_button()

    def show_as_bw_button(self):
        """
        Transform Button to open image as Black and White
        :return: None
        """
        print('Black and White Button Pressed')
        self.im_gray = cv2.imread(self.os_filename, cv2.IMREAD_GRAYSCALE)
        (thresh, self.np_img) = cv2.threshold(self.im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        self.redraw()


if __name__ == "__main__":
    root = tk.Tk()
    # Resize the display window
    root.geometry("800x1000")
    app = Application(master=root, next_phase=None)
    app.mainloop()
