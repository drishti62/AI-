import random
import numpy as np
import tkinter as tk
from tkinter import messagebox

# Create a distance matrix for cities
def create_distance_matrix(num_cities):
    matrix = np.random.randint(1, 100, size=(num_cities, num_cities))
    matrix = (matrix + matrix.T) / 2  # Ensure the matrix is symmetric
    np.fill_diagonal(matrix, 0)  # Distance from a city to itself is 0
    return matrix

# Calculate the total distance of the route
def calculate_distance(route, distance_matrix):
    return sum(distance_matrix[route[i]][route[(i + 1) % len(route)]] for i in range(len(route)))

# Generate an initial population of routes
def generate_population(size, num_cities):
    return [random.sample(range(num_cities), num_cities) for _ in range(size)]

# Select parents based on fitness
def selection(population, distance_matrix):
    scores = [(calculate_distance(route, distance_matrix), route) for route in population]
    scores.sort(key=lambda x: x[0])
    return [route for _, route in scores[:len(population) // 2]]

# Crossover two parents to create offspring
def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = [None] * len(parent1)
    
    child[start:end] = parent1[start:end]
    fill_positions = [i for i in range(len(parent2)) if parent2[i] not in child]
    
    for i in fill_positions:
        for j in range(len(child)):
            if child[j] is None:
                child[j] = parent2[i]
                break
    
    return child

# Mutate a route by swapping two cities
def mutate(route):
    idx1, idx2 = random.sample(range(len(route)), 2)
    route[idx1], route[idx2] = route[idx2], route[idx1]

# Main Genetic Algorithm function
def genetic_algorithm(num_cities, population_size, generations, mutation_rate):
    distance_matrix = create_distance_matrix(num_cities)
    population = generate_population(population_size, num_cities)

    for generation in range(generations):
        selected = selection(population, distance_matrix)
        next_generation = selected[:]

        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(selected, 2)
            child = crossover(parent1, parent2)

            if random.random() < mutation_rate:
                mutate(child)

            next_generation.append(child)

        population = next_generation

    best_route = min(population, key=lambda route: calculate_distance(route, distance_matrix))
    best_distance = calculate_distance(best_route, distance_matrix)

    return best_route, best_distance

class TSPGUI:
    def __init__(self, master):
        self.master = master
        master.title("Traveling Salesman Problem Solver")

        self.label = tk.Label(master, text="Traveling Salesman Problem Solver")
        self.label.pack(pady=10)

        self.num_cities_label = tk.Label(master, text="Number of Cities:")
        self.num_cities_label.pack()
        self.num_cities_entry = tk.Entry(master)
        self.num_cities_entry.pack()

        self.population_label = tk.Label(master, text="Population Size:")
        self.population_label.pack()
        self.population_entry = tk.Entry(master)
        self.population_entry.pack()

        self.generations_label = tk.Label(master, text="Generations:")
        self.generations_label.pack()
        self.generations_entry = tk.Entry(master)
        self.generations_entry.pack()

        self.mutation_rate_label = tk.Label(master, text="Mutation Rate (0-1):")
        self.mutation_rate_label.pack()
        self.mutation_rate_entry = tk.Entry(master)
        self.mutation_rate_entry.pack()

        self.solve_button = tk.Button(master, text="Solve TSP", command=self.solve_tsp)
        self.solve_button.pack(pady=20)

    def solve_tsp(self):
        try:
            num_cities = int(self.num_cities_entry.get())
            population_size = int(self.population_entry.get())
            generations = int(self.generations_entry.get())
            mutation_rate = float(self.mutation_rate_entry.get())

            best_route, best_distance = genetic_algorithm(num_cities, population_size, generations, mutation_rate)

            route_str = " -> ".join(str(city) for city in best_route) + f" (Distance: {best_distance})"
            messagebox.showinfo("Solution", f"Best route: {route_str}")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")

if __name__ == "__main__":
    root = tk.Tk()
    tsp_gui = TSPGUI(root)
    root.mainloop()
