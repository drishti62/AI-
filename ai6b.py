import tkinter as tk
from tkinter import messagebox, colorchooser
import random

class NumberPuzzleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Puzzle Game")

        self.tiles = list(range(1, 9)) + [0]
        self.goal = list(range(1, 9)) + [0]
        self.tile_color = "orange"  

        self.create_widgets()
        self.shuffle_puzzle()

    def create_widgets(self):
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=10)

        self.title_label = tk.Label(self.root, text="Number Puzzle Game", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=5)

        self.instructions_label = tk.Label(self.root, font=("Arial", 12))
        self.instructions_label.pack(pady=5)

        self.reset_button = tk.Button(self.root, text="Reset Game", command=self.shuffle_puzzle, font=("Arial", 12))
        self.reset_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.color_button = tk.Button(self.root,command=self.choose_color, font=("Arial", 12))
        self.color_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.board_frame,width=6, height=3, font=("Arial", 16), bg=self.tile_color, command=lambda i=i, j=j: self.move_tile(i, j))
                button.grid(row=i, column=j, padx=5, pady=5)
                row.append(button)
            self.buttons.append(row)
        self.update_buttons()

    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                value = self.tiles[i * 3 + j]
                self.buttons[i][j].config(text="" if value == 0 else str(value))

    def find_zero(self):
        index = self.tiles.index(0)
        return index // 3, index % 3

    def move_tile(self, i, j):
        zero_i, zero_j = self.find_zero()
        if (abs(i - zero_i) == 1 and j == zero_j) or (abs(j - zero_j) == 1 and i == zero_i):
            self.tiles[zero_i * 3 + zero_j], self.tiles[i * 3 + j] = self.tiles[i * 3 + j], self.tiles[zero_i * 3 + zero_j]
            self.update_buttons()
            if self.tiles == self.goal:
                messagebox.showinfo("Congratulations!", "You have solved the puzzle!")

    def shuffle_puzzle(self):
        random.shuffle(self.tiles)
        while not self.is_solvable() or self.tiles == self.goal:
            random.shuffle(self.tiles)
        self.update_buttons()

    def is_solvable(self):
        inversions = 0
        one_d_tiles = [tile for tile in self.tiles if tile != 0]
        for i in range(len(one_d_tiles)):
            for j in range(i + 1, len(one_d_tiles)):
                if one_d_tiles[i] > one_d_tiles[j]:
                    inversions += 1
        return inversions % 2 == 0

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose Tile Color")[1]
        if color_code:
            self.tile_color = color_code
            self.update_tile_colors()

    def update_tile_colors(self):
        for i in range(3):
            for j in range(3):
                if self.tiles[i * 3 + j] != 0:
                    self.buttons[i][j].config(bg=self.tile_color)

def main():
    root = tk.Tk()
    app = NumberPuzzleGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
