import tkinter as tk
import cv2
from data_management.phase_tkinter_class import PipelinePhase


class Application (PipelinePhase):
    """
    This module's purpose is to provide a UI to help with creating/expanding the dataset
    Specifically the story_photo_template.py script will allow the user to pick a photo and export a modified
    version of the photo used for further processing. This template will also act as a base template for other
    transformations required in the future.image will be saved with phase directory in the same location as the
    imported image
    For this phase to work properly, the input image has to be black and white with a white background. Sharpening the
    input first enhances the output.
    """

    def __init__(self, next_phase, master=None, prev_phase: PipelinePhase = None):
        super().__init__(next_phase, master=master, prev_phase=prev_phase)
        self.phase = "phase5"
        self.master = master
        self.pack()
        self.points = []
        self.cursor_oval_handles = []
        self.line_handles = []
        self.create_widgets()
        self.newest_pt_idx = -1
        self.np_img = self.np_img.astype("uint8")
        self.np_img_original = self.np_img.copy()

        print(self.filename)

    def create_widgets(self):
        """
        This function creates the widgets for the UI
        :return: None
        """
        self.horz_kernal_width_widget = tk.Scale(self.controls_frame, from_=2, to=100)
        self.horz_kernal_width_widget["command"] = self.removeLines_button
        self.horz_kernal_width_widget.pack()

        self.transform_btn = tk.Button(self.controls_frame)
        self.transform_btn["text"] = "lines_removed"
        self.transform_btn["command"] = self.removeLines_button
        self.transform_btn.pack(side="top")

        self.save_btn = tk.Button(self.controls_frame)
        self.save_btn["text"] = "save"
        self.save_btn["command"] = self.save_button
        self.save_btn.pack(side="top")

        # Next Phase button
        self.next_phase_btn = tk.Button(self.controls_frame)
        self.next_phase_btn["text"] = "Next Phase"
        self.next_phase_btn["command"] = self.next_phase_button
        self.next_phase_btn.pack(side="top")

        self.quit = tk.Button(self.controls_frame, text="QUIT", fg="red", command=self.destroy)
        self.quit.pack(side="bottom")

        self.image_handle = None

    def next_phase_button(self):
        self.goto_next_phase_flag = True
        command = self.master.destroy()

    def removeLines_button(self, event=None):
        """
        This function removes horizontal lines in the input image
        :return: modified image
        """
        can_h = self.canvas.winfo_height()
        can_w = self.canvas.winfo_width()
        img_w = self.np_img.shape[1]
        img_h = self.np_img.shape[0]

        self.np_img = self.np_img_original
        self.np_img = cv2.threshold(self.np_img, 127, 255, cv2.THRESH_BINARY)[1]

        # thresh
        thresh = cv2.threshold(self.np_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Remove horizontal
        horz_kernel_size = (self.horz_kernal_width_widget.get(), 1)
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, horz_kernel_size)
        print(self.np_img.shape)
        detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(self.np_img, [c], -1, (255, 255, 255), 2)

        print(self.np_img.shape)

        # Repair image
        repair_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 3))
        self.np_img = 255 - cv2.morphologyEx(255 - self.np_img, cv2.MORPH_CLOSE, repair_kernel, iterations=1)
        self.redraw()


if __name__ == "__main__":
    root = tk.Tk()
    #the user can modify window display parameters as needed
    root.geometry("800x1000")
    app = Application(master=root, next_phase=None)
    app.mainloop()
