import tkinter as tk
from tkinter import messagebox
from collections import deque

class State:
    def __init__(self, missionaries_left, cannibals_left, boat_position):
        self.missionaries_left = missionaries_left
        self.cannibals_left = cannibals_left
        self.boat_position = boat_position  # 0 for left, 1 for right

    def is_valid(self):
        if (self.missionaries_left < 0 or self.cannibals_left < 0 or
            (self.missionaries_left > 0 and self.missionaries_left < self.cannibals_left)):
            return False
        return True

    def is_goal(self):
        return self.missionaries_left == 0 and self.cannibals_left == 0

    def __hash__(self):
        return hash((self.missionaries_left, self.cannibals_left, self.boat_position))

    def __eq__(self, other):
        return (self.missionaries_left, self.cannibals_left, self.boat_position) == (other.missionaries_left, other.cannibals_left, other.boat_position)

class MissionariesCannibalsApp:
    def __init__(self, master):
        self.master = master
        master.title("Missionaries and Cannibals Problem")

        self.canvas = tk.Canvas(master, width=600, height=400, bg="lightblue")
        self.canvas.pack()

        self.start_button = tk.Button(master, text="Solve", command=self.solve)
        self.start_button.pack(pady=10)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset)
        self.reset_button.pack(pady=5)

        self.states = []
        self.current_step = 0

        # Initial state
        self.initial_state = State(3, 3, 0)
        self.solution_path = self.bfs(self.initial_state)

    def bfs(self, initial_state):
        queue = deque([initial_state])
        visited = set()
        parent_map = {initial_state: None}

        while queue:
            current_state = queue.popleft()

            if current_state.is_goal():
                return self.reconstruct_path(parent_map, current_state)

            visited.add(current_state)

            for m in range(3):  # 0 to 2 missionaries
                for c in range(3):  # 0 to 2 cannibals
                    if m + c >= 1 and m + c <= 2:
                        if current_state.boat_position == 0:
                            new_state = State(current_state.missionaries_left - m, current_state.cannibals_left - c, 1)
                        else:
                            new_state = State(current_state.missionaries_left + m, current_state.cannibals_left + c, 0)

                        if new_state.is_valid() and new_state not in visited:
                            visited.add(new_state)
                            queue.append(new_state)
                            parent_map[new_state] = current_state

        return None

    def reconstruct_path(self, parent_map, state):
        path = []
        while state is not None:
            path.append(state)
            state = parent_map[state]
        return path[::-1]

    def solve(self):
        if not self.solution_path:
            messagebox.showinfo("No Solution", "No solution exists for this problem.")
            return

        self.current_step = 0
        self.animate_solution()

    def animate_solution(self):
        if self.current_step < len(self.solution_path):
            state = self.solution_path[self.current_step]
            self.draw_state(state)
            self.current_step += 1
            self.master.after(1000, self.animate_solution)  # Delay for 1 second

    def draw_state(self, state):
        self.canvas.delete("all")
        # Draw the left side
        self.canvas.create_text(100, 50, text=f"Left: {state.missionaries_left}M {state.cannibals_left}C", font=("Arial", 14))
        # Draw the right side
        self.canvas.create_text(400, 50, text=f"Right: {3 - state.missionaries_left}M {3 - state.cannibals_left}C", font=("Arial", 14))
        # Draw the boat
        boat_pos = 100 if state.boat_position == 0 else 400
        self.canvas.create_rectangle(boat_pos - 20, 150, boat_pos + 20, 200, fill="brown")
        self.canvas.create_text(boat_pos, 175, text="Boat", font=("Arial", 12))

    def reset(self):
        self.canvas.delete("all")
        self.current_step = 0
        self.initial_state = State(3, 3, 0)
        self.solution_path = self.bfs(self.initial_state)
        self.draw_state(self.initial_state)

if __name__ == "__main__":
    root = tk.Tk()
    app = MissionariesCannibalsApp(root)
    app.reset()  # Initial state display
    root.mainloop()
