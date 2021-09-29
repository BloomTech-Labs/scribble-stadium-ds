"""
This module's purpose is to open the image in it's original format and display through
a tkinter application and further enable the user to see the same image in a
Black and White format. Finally the image can be saved in the same directory
as that of the image as Black and White.

image will be saved with _bw appended before the file extension
"""

from data_management.phase_tkinter_class import PipelinePhase


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
        self.show_as_bw.pack(side="top")

        # Save Button for Black and White
        self.save_btn_bw = tk.Button(self)
        self.save_btn_bw["text"] = "Save as Black and White"
        self.save_btn_bw["command"] = self.save_button_bw
        self.save_btn_bw.pack(side="top")

        # Next Phase button
        self.next_phase_btn = tk.Button(self)
        self.next_phase_btn["text"] = "Next Phase"
        self.next_phase_btn["command"] = self.next_phase_button
        self.next_phase_btn.pack(side="top")

        # Quit Button
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.image_handle = None

    def next_phase_button(self):
        self.goto_next_phase_flag = True
        command = self.master.destroy()

    def save_button_bw(self):
        """
        Save Button to save file as Black and White in file path directory
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
        Transform Button to open image as Black and White
        :return: None
        """
        print('Black and White Button Pressed')
        self.im_gray = cv2.imread(self.filename, cv2.IMREAD_GRAYSCALE)
        (thresh, self.np_img) = cv2.threshold(self.im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # self.np_img = cv2.cvtColor(self.np_img, cv2.COLOR_BGR2GRAY)
        # self.np_img = cv2.cvtColor(self.np_img, cv2.THRESH_BINARY)
        self.canvas.update()


if __name__ == "__main__":
    root = tk.Tk()
    # Resize the display window
    root.geometry("800x1000")
    app = Application(master=root, next_phase=None)
    app.mainloop()
