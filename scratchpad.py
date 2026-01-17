import tkinter as tk

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scratchpad")
        self.root.geometry("800x600")

        # Create the canvas for drawing
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        # Create a "Clear All" button
        self.clear_button = tk.Button(self.root, text="Clear All", command=self.clear_canvas)
        self.clear_button.pack(side=tk.BOTTOM, fill=tk.X)

        self.last_x = None
        self.last_y = None

    def start_draw(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def draw(self, event):
        if self.last_x is not None and self.last_y is not None:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, width=2, fill="black", capstyle=tk.ROUND, smooth=True)
            self.last_x = event.x
            self.last_y = event.y

    def stop_draw(self, event):
        self.last_x = None
        self.last_y = None

    def clear_canvas(self):
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
