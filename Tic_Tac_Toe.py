import tkinter as tk
from tkinter import messagebox

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def make_move(self, game_manager, index):
        pass

class PlayerX(Player):
    def make_move(self, game_manager, index):
        if game_manager.board.update_cell(index, self.symbol):
            game_manager.buttons[index].config(text=self.symbol)
            game_manager.after_move()

class PlayerO(Player):
    def make_move(self, game_manager, index):
        if game_manager.board.update_cell(index, self.symbol):
            game_manager.buttons[index].config(text=self.symbol)
            game_manager.after_move()

class GameBoard:
    def __init__(self):
        self.state = [""] * 9

    def is_cell_empty(self, index):
        return self.state[index] == ""

    def update_cell(self, index, symbol):
        if self.is_cell_empty(index):
            self.state[index] = symbol
            return True
        return False

    def is_full(self):
        return all(cell != "" for cell in self.state)

    def check_winner(self, symbol):
        win_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        return any(all(self.state[i] == symbol for i in combo) for combo in win_combos)

    def reset(self):
        self.state = [""] * 9

class GameManager:
    def __init__(self, board):
        self.board = board
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.buttons = []
        self.current_player = None
        self.players = {
            "X": PlayerX("X"),
            "O": PlayerO("O")
        }
        self.current_symbol = "X"
        self.current_player = self.players[self.current_symbol]
        self.create_widgets()

    def create_widgets(self):
        for i in range(9):
            button = tk.Button(self.window, text="", font=("Arial", 24), width=5, height=2,
                               command=lambda i=i: self.on_click(i))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

        history_button = tk.Button(self.window, text="View Match History", font=("Arial", 12),
                                   command=self.show_match_history)
        history_button.grid(row=3, column=0, columnspan=3, sticky="we")

        clear_button = tk.Button(self.window, text="Clear Match History", font=("Arial", 12),
                                 command=self.clear_match_history)
        clear_button.grid(row=4, column=0, columnspan=3, sticky="we")

    def on_click(self, index):
        self.current_player.make_move(self, index)

    def after_move(self):
        if self.board.check_winner(self.current_symbol):
            messagebox.showinfo("Game Over", f"Player {self.current_symbol} wins!")
            self.save_result(f"Winner: Player {self.current_symbol}")
            self.reset_game()
        elif self.board.is_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.save_result("Draw")
            self.reset_game()
        else:
            self.current_symbol = "O" if self.current_symbol == "X" else "X"
            self.current_player = self.players[self.current_symbol]

    def save_result(self, result):
        with open("results.txt", "a") as file:
            file.write(result + "\n")

    def show_match_history(self):
        try:
            with open("results.txt", "r") as file:
                data = file.read()
                if data.strip():
                    messagebox.showinfo("Match History", data)
                else:
                    messagebox.showinfo("Match History", "No games played yet.")
        except FileNotFoundError:
            messagebox.showinfo("Match History", "No history file found.")

    def clear_match_history(self):
        with open("results.txt", "w") as file:
            file.truncate(0)
        messagebox.showinfo("Match History", "Match history cleared.")

    def reset_game(self):
        self.board.reset()
        for button in self.buttons:
            button.config(text="")
        self.current_symbol = "X"
        self.current_player = self.players[self.current_symbol]

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game_board = GameBoard()
    game = GameManager(game_board)
    game.run()
