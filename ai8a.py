import tkinter as tk
from tkinter import messagebox

class BlockWorld:
    def __init__(self, initial_state, goal_state):
        self.state = initial_state
        self.goal_state = goal_state
        self.history = []

    def is_goal(self):
        return self.state == self.goal_state

    def move(self, from_stack, to_stack):
        if self.state[from_stack]:
            block = self.state[from_stack][-1]
            new_state = [stack.copy() for stack in self.state]
            new_state[from_stack].pop()
            new_state[to_stack].append(block)
            return new_state
        return None

    def get_possible_moves(self):
        moves = []
        for i in range(len(self.state)):
            for j in range(len(self.state)):
                if i != j:
                    new_state = self.move(i, j)
                    if new_state is not None:
                        moves.append(new_state)
        return moves

    def search(self):
        stack = [self.state]

        while stack:
            current_state = stack.pop()
            self.history.append(current_state)

            if self.is_goal():
                return current_state

            for next_state in self.get_possible_moves():
                if next_state not in self.history:
                    stack.append(next_state)

        return None  # No solution found

class BlockWorldGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Block World Problem Solver")

        # Initial and Goal States with more blocks
        self.initial_state = [[1, 2], [3, 4], [5], []]  # Blocks A, B, C, D, E
        self.goal_state = [[], [1, 2], [3, 4, 5], []]   # Goal: A, B on one stack; C, D, E on another

        self.block_world = BlockWorld(self.initial_state, self.goal_state)
        self.selected_block = None

        self.canvas = tk.Canvas(root, width=400, height=300, bg='white')
        self.canvas.pack()

        self.draw_blocks()

        self.move_button = tk.Button(root, text="Move Block", command=self.move_block)
        self.move_button.pack(pady=10)

        self.solve_button = tk.Button(root, text="Solve", command=self.solve)
        self.solve_button.pack(pady=5)

    def draw_blocks(self):
        self.canvas.delete("all")
        colors = ['red', 'green', 'blue', 'orange', 'purple']
        for i, stack in enumerate(self.block_world.state):
            for j, block in enumerate(stack):
                self.canvas.create_rectangle(50 + i * 100, 250 - j * 50, 
                                              50 + i * 100 + 80, 250 - j * 50 - 40, 
                                              fill=colors[block - 1])
                self.canvas.create_text(50 + i * 100 + 40, 250 - j * 50 - 20, 
                                        text=f'Block {block}', fill='white')

    def move_block(self):
        if self.selected_block is not None:
            from_stack = self.selected_block[0]
            to_stack = (from_stack + 1) % len(self.block_world.state)  # Move to next stack
            new_state = self.block_world.move(from_stack, to_stack)

            if new_state:
                self.block_world.state = new_state
                self.draw_blocks()
            else:
                messagebox.showinfo("Error", "Invalid move!")

    def select_block(self, event):
        x, y = event.x, event.y
        stack_index = x // 100
        if stack_index < len(self.block_world.state):
            if self.block_world.state[stack_index]:
                self.selected_block = (stack_index, self.block_world.state[stack_index][-1])
                print(f"Selected Block: {self.selected_block[1]} from Stack {stack_index}")

    def solve(self):
        solution = self.block_world.search()
        if solution:
            self.block_world.state = solution
            self.draw_blocks()
            messagebox.showinfo("Solution Found", f"Goal state reached: {solution}")
        else:
            messagebox.showinfo("No Solution", "No solution exists.")

def main():
    root = tk.Tk()
    app = BlockWorldGUI(root)
    root.bind("<Button-1>", app.select_block)  # Bind left-click to select blocks
    root.mainloop()

if __name__ == "__main__":
    main()
