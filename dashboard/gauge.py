import tkinter as tk
import math

class GaugeCanvas(tk.Canvas):
    def __init__(self, master=None, width=300, height=300, max_value=100, step=10, gauge_text=None, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.width = width
        self.height = height
        self.center = (width // 2, int(height * 0.9))
        self.radius = min(self.center) - 10
        self.max_value = max_value
        self.step = step
        self.gauge_text = gauge_text
        self.angle_range = 180
        self.start_angle = -180
        self.needle = None
        self.knob = None
        self.draw_gauge()
        self.draw_needle(0)

    def draw_gauge(self):
        # Draw outer arc
        # Multiply angle_range by -1 to draw the arc in the correct direction
        self.create_arc(
            10, 10, self.width - 10, self.width -10,
            start=self.start_angle*-1, extent=self.angle_range*-1,
            style="arc", width=3
        )

        # Draw tick marks
        for i in range(0, self.max_value + 1, self.step):
            angle = math.radians(self.start_angle + (i / self.max_value) * self.angle_range)
            inner = (
                self.center[0] + (self.radius - 10) * math.cos(angle),
                self.center[1] + (self.radius - 10) * math.sin(angle)
            )
            outer = (
                self.center[0] + self.radius * math.cos(angle),
                self.center[1] + self.radius * math.sin(angle)
            )
            self.create_line(inner, outer, width=2)

            # Draw number labels
            label_x = self.center[0] + (self.radius - 25) * math.cos(angle)
            label_y = self.center[1] + (self.radius - 25) * math.sin(angle)
            self.create_text(label_x, label_y, text=str(i), font=("Helvetica", 8))

        self.create_text(self.center[0], self.center[1] - 20, text=self.gauge_text, font=("Helvetica", 8, "bold"), justify="center")
    def draw_needle(self, value):
        if self.needle:
            self.delete(self.needle)

        angle = math.radians(self.start_angle + (value / self.max_value) * self.angle_range)
        x = self.center[0] + (self.radius - 30) * math.cos(angle)
        y = self.center[1] + (self.radius - 30) * math.sin(angle)
        self.needle = self.create_line(self.center[0], self.center[1], x, y, fill='red', width=3)
        # Center knob
        self.knob = self.create_oval(self.center[0] - 5, self.center[1] - 5, self.center[0] + 5, self.center[1] + 5, fill="gray", outline="black")
    def update_value(self, value):
        value = min(max(value, 0), self.max_value)
        self.draw_needle(value)
