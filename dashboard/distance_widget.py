import tkinter as tk
from PIL import Image, ImageTk  # For broader image support

class DistanceCanvas(tk.Canvas):
    def __init__(self, master, front_distance=50, back_distance=30, **kwargs):
        super().__init__(master, bg="white", width=400, height=400, **kwargs)

        self.front_distance = front_distance
        self.back_distance = back_distance

        self.center_x = 200
        self.car_y = 200  # Y position of the car's top

        self.spacing = 15
        self.max_arcs = 4

        # Load and scale the car image
        image_path = "./dashboard/assets/car_top.png"  # <-- your image path
        pil_image = Image.open(image_path).resize((60, 100))
        self.car_image = ImageTk.PhotoImage(pil_image)  # Keep reference

        self.draw_scene()

    def draw_arc_distances(self, direction='front', distance=0):
        color = "red" if direction == 'front' else "blue"
        base_y = self.car_y if direction == 'front' else self.car_y + 100  # 100 is car height
        direction_multiplier = -1 if direction == 'front' else 1

        num_arcs = min(distance // self.spacing, self.max_arcs)

        for i in range(1, num_arcs + 1):
            radius = i * self.spacing
            x0 = self.center_x - radius
            y0 = base_y + direction_multiplier * radius
            x1 = self.center_x + radius
            y1 = base_y - direction_multiplier * radius

            self.create_arc(x0, y0, x1, y1,
                            start=0 if direction == 'front' else 180,
                            extent=180,
                            style=tk.ARC,
                            width=2,
                            outline=color)

    def draw_scene(self):
        self.delete("all")

        self.draw_arc_distances('front', self.front_distance)
        self.draw_arc_distances('back', self.back_distance)

        # Draw the car image centered horizontally
        self.create_image(self.center_x, self.car_y, anchor=tk.N, image=self.car_image)

    def update_distances(self, front, back):
        self.front_distance = front
        self.back_distance = back
        self.draw_scene()
