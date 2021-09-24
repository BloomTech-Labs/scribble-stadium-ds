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
        self.handles = {self.create_rectangle([0, 0, 0, 0], width=1, fill='blue'): int(self.value_range / 2) for _ in
                        range(self.handles)}

        if len(self.handles)>1:
            stp = self.value_range / (len(self.handles)+1)
            p = stp
            for h,v in self.handles.items():
                self.handles[h]=p
                p=p+stp

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
        self.coords(self.slide_line, [0, int(h / 2), w, int(h / 2)])
        self.value_per_pix = self.value_range / w

        # ticks
        self.pix_per_tick = w / len(self.ticks)
        for i, tick in enumerate(self.ticks):
            self.coords(tick, [i * self.pix_per_tick, 0, i * self.pix_per_tick, h])

        # handles
        pix_per_value = w / (self.max - self.min)
        for handle in self.handles.items():
            hndle,v= handle
            px = v/self.value_per_pix
            self.coords(hndle, [px - self.handle_width, 10, px + self.handle_width, h - 10])

        #for i, tick_handle in zip(range(len(self.handles)), self.handles.items()):
        #    tick_value = tick_handle[1]
        #    px = tick_value * pix_per_value
        #    self.coords(tick_handle[0], [px - self.handle_width, 10, px + self.handle_width, h-10])

        self.update()

    def resize(self, event):
        self.redraw()

class Slider_with_Graph(Slider):
    pass

if __name__ == "__main__":
    root = tk.Tk()
    slider = Slider(root, 3, 0, 10, width=256, height=33, bg='#dddddd')
    slider.pack()
    root.mainloop()
