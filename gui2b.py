import tkinter as tk
from tkinter import messagebox

class TowerOfHanoiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tower of Hanoi")

        self.num_disks = 3
        self.pegs = {'A': list(range(self.num_disks, 0, -1)), 'B': [], 'C': []}
        self.peg_positions = {'A': (100, 300), 'B': (300, 300), 'C': (500, 300)}
        self.selected_disk = None

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        self.canvas = tk.Canvas(self.main_frame, width=700, height=400, bg='white')
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.grid(row=1, column=0, columnspan=3, pady=10)

        self.instructions_label = tk.Label(self.control_frame,font=("Arial", 14))
        self.instructions_label.pack(pady=5)

        self.disk_options = [3, 4, 5]
        self.disk_var = tk.IntVar(value=self.num_disks)
        self.disk_menu = tk.OptionMenu(self.control_frame, self.disk_var, *self.disk_options, command=self.change_num_disks)
        self.disk_menu.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(self.control_frame, text="Reset", command=self.reset_game, font=("Arial", 14))
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(self.control_frame, text=self.get_status_text(), font=("Arial", 14))
        self.status_label.pack(side=tk.LEFT, padx=5)

        self.setup_ui()

    def setup_ui(self):
        self.draw_poles()
        self.draw_disks()
        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_poles(self):
        self.canvas.delete("all")
        for pole, pos in self.peg_positions.items():
            x, y = pos
            self.canvas.create_rectangle(x - 10, y - 100, x + 10, y, fill='black')
            self.canvas.create_text(x, y + 20, text=f"Pole {pole}", font=("Arial", 14))

    def draw_disks(self):
        self.canvas.delete("disks")
        for pole, disks in self.pegs.items():
            x, y = self.peg_positions[pole]
            for i, disk in enumerate(disks):
                self.canvas.create_rectangle(x - disk * 10, y - (i + 1) * 20,
                                             x + disk * 10, y - i * 20,
                                             fill='green', outline='black', tags="disks")
                self.canvas.create_text(x, y - (i + 1) * 20 + 10, text=str(disk), font=("Arial", 10), tags="disks")

        self.update_status()

    def handle_click(self, event):
        x, y = event.x, event.y
        clicked_pole = self.get_clicked_pole(x, y)

        if not clicked_pole:
            return

        if self.selected_disk is None:
            self.select_disk(clicked_pole)
        else:
            self.move_disk(clicked_pole)

    def select_disk(self, pole):
        if self.pegs[pole]:
            self.selected_disk = self.pegs[pole][-1]
            x, y = self.peg_positions[pole]
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill='yellow', outline='black', tags="moving")

    def move_disk(self, target_pole):
        if self.is_valid_move(self.selected_disk, target_pole):
            source_pole = self.get_current_pole(self.selected_disk)
            self.pegs[target_pole].append(self.pegs[source_pole].pop())
            self.canvas.delete("moving")
            self.selected_disk = None
            self.draw_disks()
        else:
            messagebox.showerror("Invalid Move", "Cannot move disk to the selected pole.")

    def get_clicked_pole(self, x, y):
        for pole, pos in self.peg_positions.items():
            pole_x, pole_y = pos
            if pole_x - 10 < x < pole_x + 10 and pole_y - 100 < y < pole_y:
                return pole
        return None

    def get_current_pole(self, disk):
        for pole, disks in self.pegs.items():
            if disk in disks:
                return pole
        return None

    def is_valid_move(self, disk, target_pole):
        source_pole = self.get_current_pole(disk)
        if not self.pegs[target_pole] or self.pegs[target_pole][-1] > disk:
            return True
        return False

    def reset_game(self):
        self.num_disks = self.disk_var.get()
        self.pegs = {'A': list(range(self.num_disks, 0, -1)), 'B': [], 'C': []}
        self.selected_disk = None
        self.draw_disks()
        self.update_status()

    def change_num_disks(self, value):
        self.num_disks = int(value)
        self.reset_game()

    def update_status(self):
        self.status_label.config(text=self.get_status_text())

    def get_status_text(self):
        return f"Disks on Pole A: {len(self.pegs['A'])}, Pole B: {len(self.pegs['B'])}, Pole C: {len(self.pegs['C'])}"

if __name__ == "__main__":
    root = tk.Tk()
    app = TowerOfHanoiApp(root)
    root.mainloop()
