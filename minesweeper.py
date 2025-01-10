import random  # Used to randomly place mines on the board
import tkinter as tk  # Used to create the graphical user interface for the Minesweeper game

# Function to create the initial game board with mines placed randomly
def create_board(rows, cols, mines):
    board = [[' ' for _ in range(cols)] for _ in range(rows)]  # Initialize a blank board
    mine_positions = set()  # Set to keep track of mine locations

    while len(mine_positions) < mines:  # Loop until all mines are placed
        row, col = random.randint(0, rows - 1), random.randint(0, cols - 1)  # Randomly select a cell
        if (row, col) not in mine_positions:  # Check if the cell is already a mine
            mine_positions.add((row, col))  # Add the mine position to the set
            board[row][col] = '💣'  # Place a bomb emoji in the cell

    for row in range(rows):  # Loop through every cell in the board
        for col in range(cols):
            if board[row][col] != '💣':  # If the cell is not a mine
                board[row][col] = str(count_adjacent_mines(board, row, col))  # Count adjacent mines
    return board, mine_positions  # Return the completed board and mine positions
# Function to count the number of adjacent mines for a given cell
def count_adjacent_mines(board, row, col):
    count = 0  # Initialize mine count to 0
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]  # All adjacent directions
    for dr, dc in directions:  # Loop through each direction
        nr, nc = row + dr, col + dc  # Calculate the neighboring cell coordinates
        if 0 <= nr < len(board) and 0 <= nc < len(board[0]) and board[nr][nc] == '💣':  # Check if neighbor is a mine
            count += 1  # Increment mine count
    return count  # Return the total number of adjacent mines

# Function to reveal cells on the board
def reveal_board(board, visible_board, row, col):
    if visible_board[row][col] != ' ':  # If the cell is already revealed, do nothing
        return

    visible_board[row][col] = board[row][col]  # Reveal the cell

    if board[row][col] == '0':  # If the cell is blank ('0')
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]  # All adjacent directions
        for dr, dc in directions:  # Loop through each direction
            nr, nc = row + dr, col + dc  # Calculate the neighboring cell coordinates
            if 0 <= nr < len(board) and 0 <= nc < len(board[0]) and visible_board[nr][nc] == ' ':  # If neighbor is unrevealed
                reveal_board(board, visible_board, nr, nc)  # Recursively reveal the neighboring cell

# Initialize flag tracking and game over state
flag_positions = set()  # Default value is an empty set; tracks the positions of flagged cells
game_over = False  # Default value is False; tracks whether the game has ended

# Function to handle button clicks in the GUI
def on_click(row, col):
    global game_over
    if game_over:  # If the game is over, ignore clicks
        return

    if visible_board[row][col] != ' ':  # If the cell is already revealed, trigger surrounding reveal
        reveal_around_number(row, col)
        return

    if (row, col) in mine_positions:  # If the clicked cell is a mine
        reveal_all_mines()  # Reveal all mines
        status_label.config(text="Game Over! You hit a mine.")  # Display game over message
        game_over = True  # Set game over state
        show_restart_button()  # Show restart button
        return

    reveal_board(board, visible_board, row, col)  # Reveal the clicked cell
    update_buttons()  # Update the button states
    check_win_condition()  # Check if the player has won

# Function to check if the player has won
def check_win_condition():
    global game_over

    # Check if all non-mine cells are revealed
    all_non_mines_revealed = all(
        visible_board[r][c] != ' ' for r in range(rows) for c in range(cols) if (r, c) not in mine_positions
    )

    # Check if all mines are flagged correctly
    all_mines_flagged = all(
        (r, c) in flag_positions for r, c in mine_positions
    ) and len(flag_positions) == len(mine_positions)

    # Declare win if both conditions are met
    if all_non_mines_revealed or all_mines_flagged:
        status_label.config(text="Congratulations! You've cleared the board.")  # Display win message
        game_over = True  # Set game over state
        show_restart_button()  # Show restart button

# Function to handle right-clicks (flagging mines)
def on_right_click(row, col):
    if game_over:  # If the game is over, ignore clicks
        return

    if (row, col) not in flag_positions:  # If the cell is not flagged
        buttons[row][col].config(text='🚩', state='normal', fg='red')  # Add a flag
        flag_positions.add((row, col))  # Add the cell to flagged positions
        check_win_condition()  # Check if the player has won
    else:  # If the cell is already flagged
        buttons[row][col].config(text=' ', state='normal', fg='black')  # Remove the flag
        flag_positions.remove((row, col))  # Remove the cell from flagged positions
        check_win_condition()  # Check if the player has won

# Update the button labels to reflect revealed cells with colors
def update_buttons():
    bg_color = '#d1d1d1'  # Default value is light gray; used for revealed cells
    for r in range(rows):
        for c in range(cols):
            if visible_board[r][c] != ' ':  # If the cell is revealed
                fg_color = 'gray' if visible_board[r][c] == '0' else 'blue'  # Choose font color
                buttons[r][c].config(text=visible_board[r][c], state='disabled', fg=fg_color, bg=bg_color)  # Update button

# Reveal all mines on the board
def reveal_all_mines():
    for r, c in mine_positions:  # Loop through all mine positions
        if (r, c) in flag_positions:  # If the mine is flagged
            buttons[r][c].config(text='🚩', fg='green')  # Mark correctly flagged mines in green
        else:  # If the mine is not flagged
            buttons[r][c].config(text='💣', state='disabled', fg='red')  # Show unflagged mines in red

# Function to reveal surrounding cells when clicking on a revealed cell
def reveal_around_number(row, col):
    global game_over
    hit_mine = False
    if game_over:  # If the game is over, ignore clicks
        return
    if visible_board[row][col].isdigit() and visible_board[row][col] != '0':  # If the cell is a number
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]  # All adjacent directions
        for dr, dc in directions:  # Loop through each direction
            nr, nc = row + dr, col + dc  # Calculate the neighboring cell coordinates
            if 0 <= nr < rows and 0 <= nc < cols:  # Check if the neighbor is within board boundaries
                if visible_board[nr][nc] != ' ':  # If the neighbor is already revealed, skip
                    continue
                if (nr, nc) in flag_positions:  # If the neighbor is flagged, skip
                    continue
                if (nr, nc) in mine_positions:  # If the neighbor is a mine
                    hit_mine = True  # Set hit mine flag
                reveal_board(board, visible_board, nr, nc)  # If not revealed, reveal the neighbor
        update_buttons()  # Update the button states

        if hit_mine and not game_over:  # If a mine was hit
            reveal_all_mines()  # Reveal all mines
            status_label.config(text="Game Over! You hit a mine.")  # Display game over message
            game_over = True  # Set game over state
            show_restart_button()  # Show restart button

# Show restart button after game over
def show_restart_button():
    restart_button = tk.Button(root, text="Restart", command=lambda: restart_game())  # Create restart button
    restart_button.grid(row=rows + 1, column=0, columnspan=cols)  # Position the restart button

# Restart the game
def restart_game():
    root.destroy()  # Close the current game window
    choose_difficulty()  # Return to the difficulty selection screen

# Function to choose difficulty and start the game
def choose_difficulty():
    def start_game(size, mines):
        nonlocal root
        root.destroy()  # Close the difficulty selection window
        play_minesweeper(size, mines)  # Start the game with selected parameters

    root = tk.Tk()  # Initialize the difficulty selection window
    root.title("Choose Difficulty")  # Set the window title
    root.geometry("280x280")  # Set the window size to match 8x8
    # Add difficulty selection buttons
    tk.Label(root, text="Select Difficulty:").pack(pady=10)  # Add a label prompting difficulty selection
    tk.Button(root, text="Beginner (8x8, 10 mines)", command=lambda: start_game((8, 8), 10)).pack(pady=5)  # Beginner level
    tk.Button(root, text="Intermediate (16x16, 40 mines)", command=lambda: start_game((16, 16), 40)).pack(pady=5)  # Intermediate level
    tk.Button(root, text="Expert (30x16, 99 mines)", command=lambda: start_game((16, 30), 99)).pack(pady=5)  # Expert level

    root.mainloop()  # Start the Tkinter event loop to keep the window active

# Initialize the Minesweeper game in a GUI
def play_minesweeper(board_size, mines):
    global board, mine_positions, visible_board, buttons, status_label, rows, cols, root, game_over

    rows, cols = board_size  # Extract rows and columns from the board size tuple
    game_over = False  # Reset the game state
    board, mine_positions = create_board(rows, cols, mines)  # Generate the board and place mines
    visible_board = [[' ' for _ in range(cols)] for _ in range(rows)]  # Create the visible board (all cells unrevealed)

    root = tk.Tk()  # Create the main game window
    root.title("Minesweeper")  # Set the window title

    buttons = [[None for _ in range(cols)] for _ in range(rows)]  # Create a grid for the buttons

    # Add buttons to the grid
    for r in range(rows):
        for c in range(cols):
            btn = tk.Button(root, width=3, height=1, command=lambda r=r, c=c: on_click(r, c))  # Left-click binding
            btn.grid(row=r, column=c)  # Place the button in the grid
            buttons[r][c] = btn
            btn.bind('<Button-3>', lambda e, r=r, c=c: on_right_click(r, c))  # Right-click binding
            btn.bind('<Button-1>', lambda e, r=r, c=c: reveal_around_number(r, c)) #reveal-around binding

    # Add a status label below the board
    status_label = tk.Label(root, text="Good luck!")  # Initial message
    status_label.grid(row=rows, column=0, columnspan=cols)  # Position the label

    root.mainloop()  # Start the Tkinter event loop to keep the game window active

if __name__ == "__main__":
    choose_difficulty()  # Start the game with the difficulty selection window
