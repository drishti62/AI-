import tkinter as tk
from tkinter import messagebox

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")

        self.current_player = 'X'
        self.board = [[None] * 3 for _ in range(3)]
        
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(pady=10)

        self.game_frame = tk.Frame(root)
        self.game_frame.pack()

        self.status_label = tk.Label(self.top_frame, text=f"Player {self.current_player}'s Turn", font=("Arial", 16))
        self.status_label.pack()

        self.buttons = [[None] * 3 for _ in range(3)]
        self.create_widgets()

        self.reset_button = tk.Button(self.top_frame, text="Reset Game", command=self.reset_game, font=("Arial", 12))
        self.reset_button.pack(pady=5)

    def create_widgets(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.game_frame, font=("Arial", 40), width=5, height=2,
                                   command=lambda r=row, c=col: self.on_button_click(r, c))
                button.grid(row=row, column=col, padx=5, pady=5)
                self.buttons[row][col] = button

    def on_button_click(self, row, col):
        if self.board[row][col] is None and not self.check_winner():
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_winner():
                self.end_game(f"Player {self.current_player} wins!")
            elif all(self.board[row][col] is not None for row in range(3) for col in range(3)):
                self.end_game("It's a tie!")
            else:
                self.current_player = 'O'
                self.ai_move()  # AI plays its move

    def ai_move(self):
        best_score, best_move = self.alpha_beta(self.board, depth=0, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
        if best_move:
            row, col = best_move
            self.board[row][col] = 'O'
            self.buttons[row][col].config(text='O')
            if self.check_winner():
                self.end_game("Player O wins!")
            elif all(self.board[row][col] is not None for row in range(3) for col in range(3)):
                self.end_game("It's a tie!")
            else:
                self.current_player = 'X'
                self.update_status()

    def alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        if self.check_winner():
            return (-1, None) if maximizing_player else (1, None)
        elif all(board[row][col] is not None for row in range(3) for col in range(3)):
            return (0, None)

        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] is None:
                        board[r][c] = 'O'
                        eval = self.alpha_beta(board, depth + 1, alpha, beta, False)[0]
                        board[r][c] = None
                        if eval > max_eval:
                            max_eval = eval
                            best_move = (r, c)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] is None:
                        board[r][c] = 'X'
                        eval = self.alpha_beta(board, depth + 1, alpha, beta, True)[0]
                        board[r][c] = None
                        if eval < min_eval:
                            min_eval = eval
                            best_move = (r, c)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval, best_move

    def check_winner(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] and self.board[row][0] is not None:
                return True

        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] is not None:
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            return True

        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            return True

        return False

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.reset_game()

    def reset_game(self):
        self.current_player = 'X'
        self.board = [[None] * 3 for _ in range(3)]
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="")
        self.update_status()

    def update_status(self):
        if self.check_winner():
            self.status_label.config(text=f"Player {self.current_player} wins!")
        elif all(self.board[row][col] is not None for row in range(3) for col in range(3)):
            self.status_label.config(text="It's a tie!")
        else:
            self.status_label.config(text=f"Player {self.current_player}'s Turn")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
