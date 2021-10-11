import tkinter as tk
from tkinter import Canvas


class Slider(Canvas):
    def __init__(self, master, handles: int, min: int, max: int,handle_width:int=5,command=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.handles = handles
        self.max = max
        self.min = min
        self.value_range = max - min
        self.handle_width = handle_width
        self.command = command
        self.current_sorted_values=None
        # set to > 0 when dragging a handle
        self.dragging_handle = -1
        # self.create_oval([0, 0, 10, 10])

        self.bind("<Button-1>", self.canvas_click)
        self.bind("<B1-Motion>", self.canvas_drag)
        self.bind("<ButtonRelease-1>", self.canvas_button_up)
        self.bind("<Motion>", self.canvas_mouseover)
        self.bind('<Configure>', self.resize)

        #self.handle_values = [int((max - min) / 2) for i in range(handles)]

        self.init_canvas()

    def init_canvas(self):
        self.slide_line = self.create_line([0, 0, 0, 0], width=2, fill='black')
        self.ticks = [self.create_line([0, 0, 0, 0], fill='#999999') for _ in range(10)]
        self.handles = {self.create_rectangle([0, 0, 0, 0], width=1, fill='blue'): int(self.value_range /2) for _ in
                        range(self.handles)}

        if len(self.handles)>1:
            stp = self.value_range / (len(self.handles))
            p = stp + stp
            for h,v in self.handles.items():
                self.handles[h]=p
                p = stp - stp


        values = [v for h, v in self.handles.items()]
        values.sort()
        self.current_sorted_values = values


    def canvas_button_up(self, event):
        print("mouse button up", event)

    def canvas_drag(self, event):
        print("drag", event)
        if self.dragging_handle >= 0:
            #print("dragging handle", self.dragging_handle)
            new_val = event.x * self.value_per_pix

            if new_val <self.min:
                new_val = self.min

            if new_val > self.max:
                new_val = self.max

            self.handles[self.dragging_handle] = new_val
            self.redraw()

            values = [ v for h, v in self.handles.items()]
            values.sort()
            self.current_sorted_values=values
            self.command(self.current_sorted_values)

    def canvas_click(self, event):
        print("click", event)
        clicked = self.find_closest(event.x, event.y, 2)
        print(clicked)
        if clicked[0] in self.handles:
            print("clicked handle:", clicked[0])
            self.dragging_handle = clicked[0]

    def canvas_mouseover(self, event):
        pass
        #print("mouse over")

    def redraw(self):
        h = self.winfo_height()
        w = self.winfo_width()

        # slider
        # This is the placement of the black line
        self.coords(self.slide_line, [0, int(h / 2), w, int(h / 2)])
        self.value_per_pix = self.value_range / w

        # ticks
        self.pix_per_tick = w / len(self.ticks)
        for i, tick in enumerate(self.ticks):
            self.coords(tick, [i * self.pix_per_tick, 0, i * self.pix_per_tick, h])

        # handles
        #pix_per_value = w / (self.max - self.min)
        for handle in self.handles.items():
            hndle,v= handle
            px = v/self.value_per_pix
            self.coords(hndle, [px - self.handle_width, 10, px + self.handle_width, h - 10])

        #for i, tick_handle in zip(range(len(self.handles)), self.handles.items()):
         #   tick_value = tick_handle[1]
          #  px = tick_value * pix_per_value
           # self.coords(tick_handle[0], [px - self.handle_width, 10, px + self.handle_width, h-10])

        self.update()

    def resize(self, event):
        self.redraw()


class GroundTruthWidget(tk.Frame):

    def __init__(self, master, label_text: str = "written line number", image: str = "full path to image", **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.image = image
        self.line_number_label = tk.Label(self, text=label_text, font=("Helvetica", 24))
        self.line_number_label.pack(side=tk.LEFT)

        self.frame1 = tk.Frame(self, background="#FFFFFF")
        self.frame1.pack(side=tk.LEFT, expand=True)

        # use opencv to load image
        self.cv2_img = cv2.imread(self.image, cv2.IMREAD_UNCHANGED - cv2.IMREAD_IGNORE_ORIENTATION)
        # convert to numpy array
        self.np_img = np.array(self.cv2_img)
        # convert it to a tk.photoimage
        self.photo_img = phase_tkinter_class.np_photo_image(self.np_img)
        # create canvas of correct diminsions
        self.canvas = tk.Canvas(self.frame1, width=self.photo_img.width(), height=self.photo_img.height(), bg="#0000ff",
                                bd=0, highlightthickness=0)
        self.canvas.pack()
        # create image on the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_img)

        self.textbox = tk.Text(self.frame1, width=40, height=1, font=("Helvetica", 24))
        self.textbox.pack()
        self.update()

        self.frame2 = tk.Frame(self)
        self.frame2.pack(side=tk.LEFT, expand=True)


        self.done_button = tk.Button(self.frame2, font=("Helvetica", 14), name="done_button")
        self.done_button["text"] = "Done"
        self.done_button.pack(expand=True, fill=tk.X)
        self.done_button.setvar("pressed", False)


        self.invalid_button = tk.Button(self.frame2, font=("Helvetica", 14), name="invalid_button")
        self.invalid_button["text"] = "Invalid"
        self.invalid_button.pack(expand=True, fill=tk.X)

        self.invalid_button_pressed = tk.BooleanVar(master=self.invalid_button, name="pressed")
        self.done_button_pressed    = tk.BooleanVar(master=self.done_button, name="pressed")

        self.invalid_button.setvar("pressed", False)
        self.invalid_button.setvar("pressed", False)


class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

if __name__ == "__main__":
    root = tk.Tk()
    slider = Slider(root, 3, 0, 10, width=256, height=33, bg='#dddddd')
    slider.pack()
    root.mainloop()
