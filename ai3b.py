import tkinter as tk
import random

class HillClimbing2DApp:
    def __init__(self, root):
        self.root = root
        self.root.title("2D Hill Climbing Algorithm Visualization")

        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack()

        self.start_button = tk.Button(root, text="Start Hill Climbing", command=self.start_hill_climbing)
        self.start_button.pack(pady=10)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack(pady=10)

        self.max_iterations = 100
        self.current_x = random.uniform(-5, 5)
        self.current_y = random.uniform(-5, 5)

        self.draw_function()

    def function(self, x, y):
        # Example function: f(x, y) = - (x^2 + y^2) + 10
        return -(x**2 + y**2) + 10

    def draw_function(self):
        self.canvas.delete("all")
        for x in range(-300, 301):
            for y in range(-200, 201):
                x_value = x / 100.0
                y_value = y / 100.0
                z_value = self.function(x_value, y_value)
                color_value = int((z_value + 10) * 255 / 20)  # Normalize to 0-255
                color_value = max(0, min(255, color_value))
                self.canvas.create_rectangle(x + 300, 200 - y, x + 301, 200 - (y + 1),
                                             fill=f'#{color_value:02x}00{(255 - color_value):02x}', outline='')

        self.plot_current_point()

    def plot_current_point(self):
        self.canvas.create_oval(295 + self.current_x * 100, 195 - self.current_y * 100,
                                305 + self.current_x * 100, 205 - self.current_y * 100, fill='red')

    def start_hill_climbing(self):
        for _ in range(self.max_iterations):
            next_x = self.current_x + random.uniform(-0.1, 0.1)
            next_y = self.current_y + random.uniform(-0.1, 0.1)
            if -5 <= next_x <= 5 and -5 <= next_y <= 5:
                next_z = self.function(next_x, next_y)
                if next_z > self.function(self.current_x, self.current_y):
                    self.current_x = next_x
                    self.current_y = next_y
                    self.canvas.after(50, self.plot_current_point)  # Delay for smoother updates
                    self.root.update()

        self.show_result()

    def show_result(self):
        result_text = f"Local maximum at (x, y) = ({self.current_x:.2f}, {self.current_y:.2f}), f(x, y) = {self.function(self.current_x, self.current_y):.2f}"
        self.canvas.create_text(300, 350, text=result_text, fill="blue", font=("Arial", 12))

    def reset(self):
        self.current_x = random.uniform(-5, 5)
        self.current_y = random.uniform(-5, 5)
        self.draw_function()

if __name__ == "__main__":
    root = tk.Tk()
    app = HillClimbing2DApp(root)
    root.protocol("WM_DELETE_WINDOW", root.quit)  # Properly handle window close
    root.mainloop()
