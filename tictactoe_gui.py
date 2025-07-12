import tkinter as tk
from tkinter import messagebox
import random
import os

# --- Game State Variables ---
root = tk.Tk()
root.withdraw()  # Hide main window until setup is complete

current_player = "X"
buttons = []
score_x = score_o = score_draws = 0
vs_computer = False
difficulty = "Easy"
theme = "Light"

STATS_FILE = "tictactoe_stats.txt"
LOG_FILE = "tictactoe_log.txt"

# --- Dummy Sound Functions (No Sound) ---
def play_click_sound(): pass
def play_win_sound(): pass

# --- Game Logic Functions ---
def check_winner():
    for i in range(3):
        if buttons[i][0]['text'] == buttons[i][1]['text'] == buttons[i][2]['text'] != "":
            return True
        if buttons[0][i]['text'] == buttons[1][i]['text'] == buttons[2][i]['text'] != "":
            return True
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        return True
    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        return True
    return False

def check_draw():
    return all(btn['text'] != "" for row in buttons for btn in row)

def get_empty_cells():
    return [(r, c) for r in range(3) for c in range(3) if buttons[r][c]['text'] == ""]

def try_win_or_block(symbol):
    for r, c in get_empty_cells():
        buttons[r][c]['text'] = symbol
        if check_winner():
            buttons[r][c]['text'] = ""
            return r, c
        buttons[r][c]['text'] = ""
    return None

def ai_move():
    global current_player, score_o, score_draws
    if difficulty == "Easy":
        r, c = random.choice(get_empty_cells())
    else:
        move = try_win_or_block("O") or try_win_or_block("X")
        if move:
            r, c = move
        elif (1, 1) in get_empty_cells():
            r, c = (1, 1)
        else:
            r, c = random.choice(get_empty_cells())
    buttons[r][c]['text'] = "O"
    play_click_sound()
    if check_winner():
        score_o += 1
        play_win_sound()
        log_game_result("Computer")
        messagebox.showinfo("Game Over", "Computer wins!")
        save_scores()
        update_scoreboard()
        reset_board()
    elif check_draw():
        score_draws += 1
        log_game_result("Draw")
        messagebox.showinfo("Game Over", "It's a draw!")
        save_scores()
        update_scoreboard()
        reset_board()
    else:
        current_player = "X"
        update_turn_label()

def button_click(row, col):
    global current_player, score_x, score_draws
    if buttons[row][col]['text'] == "":
        buttons[row][col]['text'] = current_player
        play_click_sound()
        if check_winner():
            if current_player == "X":
                score_x += 1
            else:
                score_o += 1
            play_win_sound()
            log_game_result(current_player)
            messagebox.showinfo("Game Over", f"Player {current_player} wins!")
            save_scores()
            update_scoreboard()
            reset_board()
        elif check_draw():
            score_draws += 1
            log_game_result("Draw")
            messagebox.showinfo("Game Over", "It's a draw!")
            save_scores()
            update_scoreboard()
            reset_board()
        else:
            current_player = "O"
            update_turn_label()
            if vs_computer:
                root.after(500, ai_move)

# --- UI Functions ---
def reset_board():
    global current_player
    current_player = "X"
    for row in buttons:
        for btn in row:
            btn['text'] = ""
    update_turn_label()

def update_turn_label():
    turn_label.config(text=f"Turn: {current_player}")

def show_history():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            content = f.read()
    else:
        content = "No history yet."
    top = tk.Toplevel(root)
    top.title("Game History")
    tk.Label(top, text=content, justify="left", font=("Arial", 12)).pack(padx=10, pady=10)

def log_game_result(winner):
    with open(LOG_FILE, "a") as f:
        f.write(f"{winner} won\n")

# --- Scoreboard ---
def update_scoreboard():
    score_label.config(text=f"X: {score_x}    O: {score_o}    Draws: {score_draws}")

def load_scores():
    global score_x, score_o, score_draws
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            lines = f.read().splitlines()
            if len(lines) == 3:
                score_x = int(lines[0])
                score_o = int(lines[1])
                score_draws = int(lines[2])

def save_scores():
    with open(STATS_FILE, "w") as f:
        f.write(f"{score_x}\n{score_o}\n{score_draws}")

def reset_scores():
    global score_x, score_o, score_draws
    score_x = score_o = score_draws = 0
    save_scores()
    update_scoreboard()
    messagebox.showinfo("Reset", "Scoreboard has been reset.")

# --- Theme ---
def apply_theme(theme_choice):
    bg = "#222" if theme_choice == "Dark" else "#f0f0f0"
    fg = "#eee" if theme_choice == "Dark" else "#000"
    btn_bg = "#444" if theme_choice == "Dark" else "#fff"
    root.configure(bg=bg)
    score_label.configure(bg=bg, fg=fg)
    turn_label.configure(bg=bg, fg=fg)
    history_btn.configure(bg=btn_bg, fg=fg)
    reset_score_btn.configure(bg=btn_bg, fg=fg)
    for row in buttons:
        for btn in row:
            btn.configure(bg=btn_bg, fg=fg, activebackground="#999")

# --- Settings Window ---
def open_settings():
    def update_difficulty_visibility():
        if mode_var.get() == "2-Player":
            difficulty_label.pack_forget()
            easy_btn.pack_forget()
            hard_btn.pack_forget()
        else:
            difficulty_label.pack(anchor="w")
            easy_btn.pack(anchor="w")
            hard_btn.pack(anchor="w")

    def start_game():
        global vs_computer, difficulty, theme
        vs_computer = (mode_var.get() == "1-Player")
        difficulty = difficulty_var.get()
        theme = theme_var.get()
        settings_window.destroy()
        setup_main_game()
        root.deiconify()  # Show main game window

    settings_window = tk.Toplevel()
    settings_window.title("Game Settings")
    settings_window.grab_set()

    tk.Label(settings_window, text="Select Mode:").pack(anchor="w")
    mode_var = tk.StringVar(value="1-Player")
    tk.Radiobutton(settings_window, text="1-Player vs Computer", variable=mode_var, value="1-Player", command=update_difficulty_visibility).pack(anchor="w")
    tk.Radiobutton(settings_window, text="2-Player", variable=mode_var, value="2-Player", command=update_difficulty_visibility).pack(anchor="w")

    difficulty_label = tk.Label(settings_window, text="Select AI Difficulty:")
    difficulty_label.pack(anchor="w")
    difficulty_var = tk.StringVar(value="Easy")
    easy_btn = tk.Radiobutton(settings_window, text="Easy", variable=difficulty_var, value="Easy")
    hard_btn = tk.Radiobutton(settings_window, text="Hard", variable=difficulty_var, value="Hard")
    easy_btn.pack(anchor="w")
    hard_btn.pack(anchor="w")

    tk.Label(settings_window, text="Select Theme:").pack(anchor="w")
    theme_var = tk.StringVar(value="Light")
    tk.Radiobutton(settings_window, text="Light", variable=theme_var, value="Light").pack(anchor="w")
    tk.Radiobutton(settings_window, text="Dark", variable=theme_var, value="Dark").pack(anchor="w")

    tk.Button(settings_window, text="Start Game", command=start_game).pack(pady=10)

# --- Setup GUI After Settings ---
def setup_main_game():
    global score_label, turn_label, history_btn, reset_score_btn, buttons

    score_label = tk.Label(root, text="", font=("Arial", 14))
    score_label.grid(row=0, column=0, columnspan=3, pady=(10, 0))

    turn_label = tk.Label(root, text="", font=("Arial", 12))
    turn_label.grid(row=1, column=0, columnspan=3)

    buttons = [[None for _ in range(3)] for _ in range(3)]
    for r in range(3):
        for c in range(3):
            btn = tk.Button(root, text="", font=("Arial", 32), width=5, height=2,
                            command=lambda r=r, c=c: button_click(r, c))
            btn.grid(row=r+2, column=c)
            buttons[r][c] = btn

    history_btn = tk.Button(root, text="📜 View Game History", font=("Arial", 10), command=show_history)
    history_btn.grid(row=5, column=0, columnspan=3, pady=(10, 0))

    reset_score_btn = tk.Button(root, text="🔄 Reset Scores", font=("Arial", 10), command=reset_scores)
    reset_score_btn.grid(row=6, column=0, columnspan=3, pady=(5, 10))

    apply_theme(theme)
    load_scores()
    update_scoreboard()
    update_turn_label()

# --- Start ---
open_settings()
root.mainloop()
