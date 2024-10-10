import tkinter as tk
import math
import heapq

# Define the Cell class
class Cell:
    def __init__(self):
        self.parent_i = 0
        self.parent_j = 0
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0
        self.is_goal = False

# Define the size of the grid
ROW = 9
COL = 10

class AOStarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AO* Pathfinding Algorithm Visualization")
        
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()
        
        self.grid = [[1 for _ in range(COL)] for _ in range(ROW)]
        self.start = (8, 0)
        self.end = (0, 0)

        # Draw initial grid
        self.draw_grid()
        
        self.start_button = tk.Button(root, text="Run AO* Algorithm", command=self.run_ao_star)
        self.start_button.pack(pady=10)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack(pady=5)

        # Bind mouse clicks to select start and end points or obstacles
        self.canvas.bind("<Button-1>", self.select_obstacle)  # Left-click to set obstacles
        self.canvas.bind("<Button-3>", self.select_end)        # Right-click to set end point
        self.canvas.bind("<Button-2>", self.select_start)      # Middle-click to set start point

    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(ROW):
            for j in range(COL):
                color = 'white' if self.grid[i][j] == 1 else 'black'
                self.canvas.create_rectangle(j * 60, i * 40, j * 60 + 60, i * 40 + 40, fill=color, outline='gray')
        
        # Draw start and end points
        self.canvas.create_oval(self.start[1] * 60 + 10, self.start[0] * 40 + 10, 
                                self.start[1] * 60 + 50, self.start[0] * 40 + 50, fill='green', outline='black')
        self.canvas.create_oval(self.end[1] * 60 + 10, self.end[0] * 40 + 10, 
                                self.end[1] * 60 + 50, self.end[0] * 40 + 50, fill='red', outline='black')

    def is_valid(self, row, col):
        return (0 <= row < ROW) and (0 <= col < COL)

    def is_unblocked(self, row, col):
        return self.grid[row][col] == 1

    def is_destination(self, row, col):
        return (row, col) == self.end

    def calculate_h_value(self, row, col):
        return ((row - self.end[0]) ** 2 + (col - self.end[1]) ** 2) ** 0.5

    def trace_path(self, cell_details):
        path = []
        row, col = self.end

        while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
            path.append((row, col))
            temp_row = cell_details[row][col].parent_i
            temp_col = cell_details[row][col].parent_j
            row, col = temp_row, temp_col

        path.append((row, col))
        path.reverse()

        for (r, c) in path:
            self.canvas.create_rectangle(c * 60 + 10, r * 40 + 10, 
                                          c * 60 + 50, r * 40 + 50, fill='yellow')

    def run_ao_star(self):
        closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
        cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

        i, j = self.start
        cell_details[i][j].f = 0
        cell_details[i][j].g = 0
        cell_details[i][j].h = 0
        cell_details[i][j].parent_i = i
        cell_details[i][j].parent_j = j

        open_list = []
        heapq.heappush(open_list, (0.0, i, j))

        while open_list:
            p = heapq.heappop(open_list)
            i, j = p[1], p[2]
            closed_list[i][j] = True

            if self.is_destination(i, j):
                self.trace_path(cell_details)
                return

            # Check all 8 possible movements (including diagonals)
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dir in directions:
                new_i, new_j = i + dir[0], j + dir[1]

                if self.is_valid(new_i, new_j) and self.is_unblocked(new_i, new_j) and not closed_list[new_i][new_j]:
                    g_new = cell_details[i][j].g + 1.0
                    h_new = self.calculate_h_value(new_i, new_j)
                    f_new = g_new + h_new

                    if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j

                        # Add new cell to the open list
                        if (f_new, new_i, new_j) not in open_list:
                            heapq.heappush(open_list, (f_new, new_i, new_j))

        print("Failed to find the destination cell")

    def select_obstacle(self, event):
        col = event.x // 60
        row = event.y // 40
        if self.is_valid(row, col):
            self.grid[row][col] = 0 if self.grid[row][col] == 1 else 1
            self.draw_grid()

    def select_start(self, event):
        col = event.x // 60
        row = event.y // 40
        if self.is_valid(row, col) and self.is_unblocked(row, col):
            self.start = (row, col)
            self.draw_grid()

    def select_end(self, event):
        col = event.x // 60
        row = event.y // 40
        if self.is_valid(row, col) and self.is_unblocked(row, col):
            self.end = (row, col)
            self.draw_grid()

    def reset(self):
        self.grid = [[1 for _ in range(COL)] for _ in range(ROW)]
        self.start = (8, 0)
        self.end = (0, 0)
        self.draw_grid()

def main():
    root = tk.Tk()
    app = AOStarApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
