import tkinter as tk
import math

class RectangleDashboardCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="white", width=600, height=250, **kwargs)

        # Draw elements
        self.odometer_text = self.create_text(80, 125, text="00000 km", font=("Arial", 16, "bold"))
        self.temp_text = self.create_text(520, 125, text="30°C", font=("Arial", 16, "bold"))

        # Fuel gauge
        self.fuel_gauge = Gauge(self, center=(230, 125), radius=50, label_left="E", label_right="F", title=None)

        # Temperature gauge
        self.temp_gauge = Gauge(self, center=(370, 125), radius=50, label_left="C", label_right="H", title=None)


    def update_odometer(self, km):
        self.itemconfig(self.odometer_text, text=f"{km:05d} km")

    def update_temperature_text(self, temp_c):
        self.itemconfig(self.temp_text, text=f"{temp_c:.0f}°C")

    def update_fuel_level(self, level):  # level: 0.0 (E) to 1.0 (F)
        self.fuel_gauge.update(level)

    def update_engine_temp_level(self, level):  # level: 0.0 (C) to 1.0 (H)
        self.temp_gauge.update(level)

class Gauge:
    def __init__(self, canvas, center, radius, label_left, label_right, title=None):
        self.canvas = canvas
        self.center = center
        self.radius = radius
        self.needle = None
        self.knob = None
        self._draw_gauge(label_left, label_right, title)

    def _draw_gauge(self, left_label, right_label, title):
        cx, cy = self.center
        r = self.radius

        # Arc (semi-circle)
        self.canvas.create_arc(cx - r, cy - r, cx + r, cy + r, start=135, extent=270, style=tk.ARC, width=2)

        # Ticks
        for i in range(6):
            angle = 135 + i * 45
            self._draw_tick(angle)

        # Labels
        self._place_label(left_label, 135, offset=20)
        self._place_label(right_label, 405, offset=20)

        # Optional title
        if title:
            self.canvas.create_text(cx, cy + r + 10, text=title, font=("Arial", 10))

        # Needle
        self.needle = self.canvas.create_line(cx, cy, cx, cy - r + 10, width=4, fill="red")

        # Center knob
        self.knob = self.canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill="gray", outline="black")

    def _draw_tick(self, angle_deg):
        r_outer = self.radius
        r_inner = self.radius - 10
        cx, cy = self.center
        angle_rad = math.radians(angle_deg)
        x1 = cx + r_inner * math.cos(angle_rad)
        y1 = cy - r_inner * math.sin(angle_rad)
        x2 = cx + r_outer * math.cos(angle_rad)
        y2 = cy - r_outer * math.sin(angle_rad)
        self.canvas.create_line(x1, y1, x2, y2, width=2)

    def _place_label(self, text, angle_deg, offset=15):
        cx, cy = self.center
        angle_rad = math.radians(angle_deg)
        x = cx + (self.radius + offset) * math.cos(angle_rad)
        y = cy - (self.radius + offset) * math.sin(angle_rad)
        self.canvas.create_text(x, y, text=text, font=("Arial", 10, "bold"))

    def update(self, level):  # level: 0.0 to 1.0
        angle = 135 + (270 * level)
        angle_rad = math.radians(angle)
        cx, cy = self.center
        r = self.radius - 10
        x = cx + r * math.cos(angle_rad)
        y = cy - r * math.sin(angle_rad)
        self.canvas.coords(self.needle, cx, cy, x, y)