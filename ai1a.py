import tkinter as tk
from tkinter import messagebox
from collections import deque

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BFS Visualization")

        
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        
        self.canvas = tk.Canvas(self.main_frame, width=600, height=400, bg='white')
        self.canvas.grid(row=0, column=0, columnspan=2)

        
        self.bfs_button = tk.Button(self.main_frame, text="Start BFS", command=self.start_bfs)
        self.bfs_button.grid(row=1, column=0, padx=5, pady=5)

        self.reset_button = tk.Button(self.main_frame, text="Reset", command=self.reset_canvas)
        self.reset_button.grid(row=1, column=1, padx=5, pady=5)

        
        self.info_label = tk.Label(self.main_frame)
        self.info_label.grid(row=2, column=0, columnspan=2, pady=5)

        self.nodes = {}
        self.edges = []
        self.node_radius = 20
        self.node_positions = {}

        self.setup_graph()
        self.draw_graph()

    def setup_graph(self):
        self.nodes = {
            1: (100, 100),
            2: (200, 100),
            3: (300, 100),
            4: (200, 200),
            5: (300, 200),
            6: (400, 200),
            7: (500, 200),
        }
        self.edges = [
            (1, 2),
            (1, 3),
            (2, 4),
            (2, 5),
            (3, 6),
            (3, 7),
        ]
        self.node_positions = self.nodes

    def draw_graph(self):
        self.canvas.delete("all")

        for (x, y) in self.node_positions.values():
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                    x + self.node_radius, y + self.node_radius,
                                    fill='orange', outline='black')

        for (start, end) in self.edges:
            x1, y1 = self.node_positions[start]
            x2, y2 = self.node_positions[end]
            self.canvas.create_line(x1, y1, x2, y2, fill='black')

        for node, (x, y) in self.node_positions.items():
            self.canvas.create_text(x, y, text=str(node), font=("Arial", 12, "bold"))

    def bfs(self, start):
        queue = deque([start])
        visited = set()
        visited.add(start)
        traversal_order = []
        paths = {start: None}

        while queue:
            node = queue.popleft()
            traversal_order.append(node)

            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    if neighbor not in paths:
                        paths[neighbor] = node

        return traversal_order, paths

    def get_neighbors(self, node):
        neighbors = []
        for start, end in self.edges:
            if start == node:
                neighbors.append(end)
            elif end == node:
                neighbors.append(start)
        return neighbors

    def start_bfs(self):
        start_node = 1
        traversal_order, paths = self.bfs(start_node)

        if traversal_order:
            self.highlight_nodes(traversal_order, paths)
        else:
            messagebox.showinfo("BFS", "No nodes found.")

    def highlight_nodes(self, order, paths):
        self.reset_canvas() 
        for node in order:
            x, y = self.node_positions[node]
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                    x + self.node_radius, y + self.node_radius,
                                    fill='purple', outline='black')
            self.canvas.create_text(x, y, text=str(node), font=("Arial", 12, "bold"), fill='white')
            self.root.update()
            self.root.after(1000)

        self.draw_paths(paths)

    def draw_paths(self, paths):
        for node, parent in paths.items():
            if parent is not None:
                x1, y1 = self.node_positions[parent]
                x2, y2 = self.node_positions[node]
                self.canvas.create_line(x1, y1, x2, y2, fill='red', dash=(4, 4))
        self.root.update()

    def reset_canvas(self):
        self.draw_graph()  

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
