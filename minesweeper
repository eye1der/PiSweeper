import random  # Used to randomly place mines on the board and generate random numbers for row and column selection
import tkinter as tk  # Used to create the graphical user interface for the Minesweeper game

# Function to create the initial game board with mines placed randomly
def create_board(rows, cols, mines):
    board = [[' ' for _ in range(cols)] for _ in range(rows)]
    mine_positions = set()

    while len(mine_positions) < mines:
        row, col = random.randint(0, rows - 1), random.randint(0, cols - 1)
        if (row, col) not in mine_positions:
            mine_positions.add((row, col))
            board[row][col] = '💣'  # Bomb emoji for mines

    for row in range(rows):
        for col in range(cols):
            if board[row][col] != '💣':
                board[row][col] = str(count_adjacent_mines(board, row, col))
    return board, mine_positions

# Function to count the number of adjacent mines for a given cell
def count_adjacent_mines(board, row, col):
    count = 0
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < len(board) and 0 <= nc < len(board[0]) and board[nr][nc] == '💣':
            count += 1
    return count

# Function to reveal cells on the board
def reveal_board(board, visible_board, row, col):
    if visible_board[row][col] != ' ':
        return

    visible_board[row][col] = board[row][col]
    
    if board[row][col] == '0':
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < len(board) and 0 <= nc < len(board[0]) and visible_board[nr][nc] == ' ':
                reveal_board(board, visible_board, nr, nc)

# Initialize flag tracking and game over state
flag_positions = set()
game_over = False

# Function to handle button clicks in the GUI
def on_click(row, col):
    global game_over
    if game_over:
        return
    
    if visible_board[row][col] != ' ':  # If the cell is already revealed, trigger surrounding reveal
        reveal_around_number(row, col)
        return
    
    if (row, col) in mine_positions:
        for r, c in mine_positions:
            buttons[r][c].config(text='💣', state='disabled', fg='red')
        status_label.config(text="Game Over! You hit a mine.")
        game_over = True
        show_restart_button()
    else:
        reveal_board(board, visible_board, row, col)
        update_buttons()
        if all(visible_board[r][c] != ' ' for r, c in mine_positions):
            status_label.config(text="Congratulations! You've cleared the board.")

# Function to handle right-clicks for flagging mines
def on_right_click(row, col):
    if game_over:
        return
    
    if (row, col) not in flag_positions:
        buttons[row][col].config(text='🚩', state='normal', fg='red')  # Red flag emoji
        flag_positions.add((row, col))
    else:
        buttons[row][col].config(text=' ', state='normal', fg='black')
        flag_positions.remove((row, col))

# Update the button labels to reflect revealed cells with colors
def update_buttons():
    for r in range(rows):
        for c in range(cols):
            if visible_board[r][c] != ' ':
                fg_color = 'gray' if visible_board[r][c] == '0' else 'blue'
                buttons[r][c].config(text=visible_board[r][c], state='disabled', fg=fg_color)

# Function to reveal surrounding cells when double-clicking a number
def reveal_around_number(row, col):
    global game_over
    hit_mine = False

    if visible_board[row][col].isdigit() and visible_board[row][col] != '0':
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            # Reveal only unrevealed cells that aren't flagged
            if 0 <= nr < rows and 0 <= nc < cols and visible_board[nr][nc] == ' ' and (nr, nc) not in flag_positions:
                if (nr, nc) in mine_positions:
                    hit_mine = True
                reveal_board(board, visible_board, nr, nc)

        update_buttons()

        if hit_mine and not game_over:
            status_label.config(text="Game Over! You hit a mine.")
            game_over = True
            show_restart_button()

# Show restart button after game over
def show_restart_button():
    restart_button = tk.Button(root, text="Restart", command=lambda: restart_game())
    restart_button.grid(row=rows + 1, column=0, columnspan=cols)

# Restart the game
def restart_game():
    root.destroy()
    choose_difficulty()

# Function to choose difficulty and start the game
def choose_difficulty():
    def start_game(size, mines):
        nonlocal root
        root.destroy()
        play_minesweeper(size, mines)

    root = tk.Tk()
    root.title("Choose Difficulty")
    root.geometry("280x280")  # Set window size to match 8x8 board size

    tk.Label(root, text="Select Difficulty:").pack(pady=10)
    tk.Button(root, text="Beginner (8x8, 10 mines)", command=lambda: start_game((8, 8), 10)).pack(pady=5)
    tk.Button(root, text="Intermediate (16x16, 40 mines)", command=lambda: start_game((16, 16), 40)).pack(pady=5)
    tk.Button(root, text="Expert (30x16, 99 mines)", command=lambda: start_game((30, 16), 99)).pack(pady=5)

    root.mainloop()

# Initialize the Minesweeper game in a GUI
def play_minesweeper(board_size, mines):
    global board, mine_positions, visible_board, buttons, status_label, rows, cols, root, game_over

    rows, cols = board_size
    game_over = False
    board, mine_positions = create_board(rows, cols, mines)
    visible_board = [[' ' for _ in range(cols)] for _ in range(rows)]

    root = tk.Tk()
    root.title("Minesweeper")

    buttons = [[None for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            btn = tk.Button(root, width=3, height=1, command=lambda r=r, c=c: on_click(r, c))
            btn.grid(row=r, column=c)
            buttons[r][c] = btn
            btn.bind('<Button-3>', lambda e, r=r, c=c: on_right_click(r, c))
            btn.bind('<Double-1>', lambda e, r=r, c=c: reveal_around_number(r, c))

    status_label = tk.Label(root, text="Good luck!")
    status_label.grid(row=rows, column=0, columnspan=cols)

    root.mainloop()

if __name__ == "__main__":
    choose_difficulty()
