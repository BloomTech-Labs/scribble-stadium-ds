import numpy as np
import tkinter as tk
from phase_tkinter_class import PipelinePhase
from custom_tk_widgets import Slider


class Application(PipelinePhase):
    """
    This Class's purpose is to allow for color manipulation of the image to produce clearer images for the dataset. This
    is achieved by changing the color data to remove lines and improve contrast.

    image will be saved with -colored appended before the file extension in phase2 directory
    """

    def __init__(self, next_phase, master=None, prev_phase: PipelinePhase = None):
        super().__init__(next_phase, master=master, prev_phase=prev_phase)
        self.phase = "phase2"
        self.points = []
        self.cursor_oval_handles = []
        self.line_handles = []

        self.newest_pt_idx = -1
        self.np_img_orig = self.np_img.copy()
        self.invert_output = False
        self.invert_red = tk.IntVar()
        self.invert_green = tk.IntVar()
        self.invert_blue = tk.IntVar()
        self.controls_frame.pack(side="top")
        self.create_widgets()

        print(self.filename)

    def create_widgets(self):

        # red channel
        self.red_frame = tk.Frame(self.controls_frame, borderwidth=1, relief=tk.SOLID)
        self.red_frame.pack()
        self.red_frame_label = tk.Label(self.controls_frame, borderwidth=1, relief=tk.SOLID, text='Red Channel')
        self.red_frame_label.pack()

        self.red_invert_check = tk.Checkbutton(self.red_frame, text="invert", variable=self.invert_red)
        self.red_invert_check.pack(side="left")

        self.red_slider = Slider(self.red_frame, handles=2, min=0, max=255, width=400, height=40,
                                 command=lambda x: self.update_image("red", x))
        self.red_slider.pack(fill="none", expand="false")

        # green channel
        self.green_frame = tk.Frame(self.controls_frame, borderwidth=1, relief=tk.SOLID)
        self.green_frame.pack()
        self.green_frame_label = tk.Label(self.controls_frame, borderwidth=1, relief=tk.SOLID, text='Green Channel')
        self.green_frame_label.pack()

        self.green_invert_check = tk.Checkbutton(self.green_frame, text="invert", variable=self.invert_green)
        self.green_invert_check.pack(side="left")

        self.green_slider = Slider(self.green_frame, handles=2, min=0, max=255, width=400, height=40,
                                   command=lambda x: self.update_image("green", x))
        self.green_slider.pack(fill="none", expand="false")

        self.blue_frame = tk.Frame(self.controls_frame, borderwidth=1, relief=tk.SOLID)
        self.blue_frame.pack(anchor="w")
        self.blue_frame_label = tk.Label(self.controls_frame, borderwidth=1, relief=tk.SOLID, text='Blue Channel')
        self.blue_frame_label.pack()

        self.blue_invert_check = tk.Checkbutton(self.blue_frame, text="invert", variable=self.invert_blue)
        self.blue_invert_check.pack(side="left")

        self.blue_slider = Slider(self.blue_frame, handles=2, min=0, max=255, width=400, height=40,
                                  command=lambda x: self.update_image("blue", x))
        self.blue_slider.pack(fill="none", expand="false")

        self.invert_output = tk.Checkbutton(self.controls_frame, text="invert output")
        self.invert_output.pack()
        self.invert_output["command"] = self.invert_check_box
        self.save_btn = tk.Button(self.controls_frame)
        self.save_btn["text"] = "save"
        self.save_btn["command"] = self.save_button
        self.save_btn.pack(side="top")

        self.quit = tk.Button(self.controls_frame, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.next_phase_btn = tk.Button(self.controls_frame)
        self.next_phase_btn["text"] = "Next Phase"
        self.next_phase_btn["command"] = self.next_phase_button
        self.next_phase_btn.pack(side="right")

        self.image_handle = None

    def next_phase_button(self):
        """
        Sets a flag that helps in advancing to the next phase
        :return: None
        """
        self.goto_next_phase_flag = True
        command = self.master.destroy()

    def invert_check_box(self):
        """
        Checking then unchecking this box results in an image with text and background colors inverted
        """
        self.invert_output = not self.invert_output
        self.update_image('red', self.red_slider.current_sorted_values)

    def update_image(self, channel, values):
        """
        This function updates the image based on user input from slider selections
        """

        def normalize(C):
            C = C - C.min()
            C = C / C.max()
            C = C * 255
            return C

        if channel == 'red':
            position = 0

        if channel == 'green':
            position = 1

        if channel == 'blue':
            position = 2

        r1, r2 = self.red_slider.current_sorted_values
        g1, g2 = self.green_slider.current_sorted_values
        b1, b2 = self.blue_slider.current_sorted_values

        print(r1, r2, g1, g2, b1, b2)

        selectionR = (self.np_img_orig[:, :, position] >= r1) * (self.np_img_orig[:, :, position] <= r2)
        selectionG = (self.np_img_orig[:, :, position] >= g1) * (self.np_img_orig[:, :, position] <= g2)
        selectionB = (self.np_img_orig[:, :, position] >= b1) * (self.np_img_orig[:, :, position] <= b2)

        if self.invert_red == True:
            selectionR = np.invert(selectionR)
        selection = selectionR * selectionG * selectionB

        selection = np.reshape(selection, (self.np_img.shape[0], self.np_img.shape[1], 1)).astype('uint8')

        if self.invert_output == True:
            self.np_img = normalize(255 - np.multiply(self.np_img_orig, selection, dtype="uint8"))
        else:
            self.np_img = np.multiply(self.np_img_orig, selection, dtype="uint8")

        self.redraw()


if __name__ == "__main__":
    root = tk.Tk()
    # Resize the display window
    root.geometry("800x1000")
    app = Application(master=root, next_phase=None)
    app.mainloop()