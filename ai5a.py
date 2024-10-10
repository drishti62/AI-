import tkinter as tk
from tkinter import messagebox

class WaterJugGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Water Jug Game")

        self.jug1_capacity = 4
        self.jug2_capacity = 3
        self.target = 2

        self.jug1 = 0
        self.jug2 = 0

        
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.fill_jug1_button = tk.Button(root, text="Fill Jug 1", command=self.fill_jug1)
        self.fill_jug1_button.pack(side=tk.LEFT)

        self.fill_jug2_button = tk.Button(root, text="Fill Jug 2", command=self.fill_jug2)
        self.fill_jug2_button.pack(side=tk.LEFT)

        self.empty_jug1_button = tk.Button(root, text="Empty Jug 1", command=self.empty_jug1)
        self.empty_jug1_button.pack(side=tk.LEFT)

        self.empty_jug2_button = tk.Button(root, text="Empty Jug 2", command=self.empty_jug2)
        self.empty_jug2_button.pack(side=tk.LEFT)

        self.pour_jug1_to_jug2_button = tk.Button(root, text="Pour Jug 1 to Jug 2", command=self.pour_jug1_to_jug2)
        self.pour_jug1_to_jug2_button.pack(side=tk.LEFT)

        self.pour_jug2_to_jug1_button = tk.Button(root, text="Pour Jug 2 to Jug 1", command=self.pour_jug2_to_jug1)
        self.pour_jug2_to_jug1_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT)

        self.update_display()

    def fill_jug1(self):
        self.jug1 = self.jug1_capacity
        self.update_display()
        self.check_win()

    def fill_jug2(self):
        self.jug2 = self.jug2_capacity
        self.update_display()
        self.check_win()

    def empty_jug1(self):
        self.jug1 = 0
        self.update_display()
        self.check_win()

    def empty_jug2(self):
        self.jug2 = 0
        self.update_display()
        self.check_win()

    def pour_jug1_to_jug2(self):
        pour_amount = min(self.jug1, self.jug2_capacity - self.jug2)
        self.jug1 -= pour_amount
        self.jug2 += pour_amount
        self.update_display()
        self.check_win()

    def pour_jug2_to_jug1(self):
        pour_amount = min(self.jug2, self.jug1_capacity - self.jug1)
        self.jug2 -= pour_amount
        self.jug1 += pour_amount
        self.update_display()
        self.check_win()

    def reset(self):
        self.jug1 = 0
        self.jug2 = 0
        self.update_display()

    def update_display(self):
        self.canvas.delete("all")

       
        self.canvas.create_rectangle(100, 100, 200, 300, outline="black", fill="orange")
        self.canvas.create_rectangle(300, 100, 400, 300, outline="black", fill="lightgreen")

        
        self.canvas.create_rectangle(100, 300 - (self.jug1 / self.jug1_capacity) * 200, 200, 300, outline="black", fill="blue")
        self.canvas.create_rectangle(300, 300 - (self.jug2 / self.jug2_capacity) * 200, 400, 300, outline="black", fill="blue")

      
        self.canvas.create_text(150, 320, text=f"Jug 1: {self.jug1}/{self.jug1_capacity}", font=("Arial", 12))
        self.canvas.create_text(350, 320, text=f"Jug 2: {self.jug2}/{self.jug2_capacity}", font=("Arial", 12))

    def check_win(self):
        if self.jug1 == self.target or self.jug2 == self.target:
            messagebox.showinfo("Congratulations!", f"You have measured {self.target} liters!")
            self.reset()

if __name__ == "__main__":
    root = tk.Tk()
    app = WaterJugGame(root)
    root.mainloop()
