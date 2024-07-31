import tkinter as tk
from tkinter import messagebox
import itertools
import random

class CardDeckGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Deck Simulator")
        
        
        self.create_widgets()
        
    def create_widgets(self):
        
        self.draw_button = tk.Button(self.root, text="Draw 5 Cards", command=self.draw_cards)
        self.draw_button.pack(pady=20)
        
        
        self.result_text = tk.Text(self.root, height=10, width=40)
        self.result_text.pack(pady=10)
        
    def draw_cards(self):
       
        ranks = [str(i) for i in range(2, 11)] + ['Jack', 'Queen', 'King', 'Ace']
        suits = ['Spade', 'Heart', 'Diamond', 'Club']
        
       
        deck = list(itertools.product(ranks, suits))
        
        
        random.shuffle(deck)
        
        
        self.result_text.delete(1.0, tk.END)
        
        
        result = "You got:\n"
        for i in range(5):
            result += f"{deck[i][0]} of {deck[i][1]}\n"
        
       
        self.result_text.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = CardDeckGUI(root)
    root.mainloop()
