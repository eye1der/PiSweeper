# PiSweeper

PiSweeper is a Python-based Minesweeper clone built with a graphical interface using Tkinter.

**How is it different? Just like the original version it has the Smart Number Reveal feature.** No other clones have this to my knowledge  

It's a fun and engaging way to enjoy the classic game of Minesweeper right on your desktop!

## Features

- **Difficulty Levels**: Choose between Beginner (8x8, 10 mines), Intermediate (16x16, 40 mines), and Expert (30x16, 99 mines).
- **Intuitive Interface**: Left-click to reveal cells and right-click to flag mines.
- **Smart Number Reveal**: Click on a revealed numbered cell to uncover all unrevealed surrounding cells (skipping flagged ones).
- **Winning Logic**: Win by flagging all mines or revealing all non-mine cells.
- **Restart Option**: Restart the game or choose a new difficulty after a game over.
- **Dynamic Feedback**: Visual updates for revealed cells, flagged mines, and game status.

## How to Play

1. **Left-Click**: Reveal a cell.
2. **Right-Click**: Place or remove a flag to mark a suspected mine.
3. **Click Numbered Cells**: Click a revealed number to uncover all adjacent unrevealed cells, excluding flagged ones.
4. Avoid clicking on a mine to stay in the game. If you hit a mine, it's game over!
5. Win by correctly flagging all mines or revealing all safe cells.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/eye1der/PiSweeper.git
   ```
2. Navigate to the project directory:
   ```bash
   cd PiSweeper
   ```
3. Run the game:
   ```bash
   python PiSweeper.py
   ```

## Requirements

- Python 3.x
- Tkinter (comes pre-installed with Python on most systems)

## Screenshots

![Start](https://github.com/user-attachments/assets/27fcb6c2-639d-4d3f-b07a-926d5d012c25)

![Won game - some flagged - mined cells left visible](https://github.com/user-attachments/assets/699205a7-9502-4958-86de-62364c3fc8da)



## Contributing

Feel free to submit issues or feature requests. Contributions are welcome! Fork the repository, make your changes, and open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

Enjoy playing PiSweeper! 🎉
