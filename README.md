♟️ Python Chess Bot
An advanced Python Chess Game built using Pygame, featuring a powerful AI opponent based on Minimax algorithm with Alpha-Beta Pruning, real-time scoring, timers, and persistent win tracking.

🚀 Features
Play against an AI that evaluates moves intelligently and prioritizes winning and king safety

Complete chess functionality: all major pieces, moves, and captures supported

Minimax with alpha-beta pruning for optimized decision-making

5-minute timer per player with game-over by timeout

Permanent win tracking saved in win_tracker.json

Scoreboard display with real-time updates

Clickable Restart button after game ends

Clean user interface with clear board, timers, and status info

🕹️ Controls
Mouse Click – Select and move pieces

Restart Button – Appears after game ends; click to restart

📦 Requirements
Python 3.x

Pygame
Install via pip:

bash
Copy code
pip install pygame
📁 File Structure
bash
Copy code
main.py               # Main game loop and UI
ai.py                 # AI logic (minimax + alpha-beta pruning)
win_tracker.json      # Persistent win tracker file (created automatically)
assets/
    wK.png, bK.png, wQ.png, ...    # Piece images
score.txt             # (optional legacy file)
scoreboard.txt        # (optional legacy file)
▶️ How to Run
Make sure your terminal is inside the project folder and all chess piece images are inside the assets/ directory. Then run:

bash
Copy code
python main.py
🧠 AI Strategy
Uses Minimax Algorithm with Alpha-Beta Pruning

Prioritizes material gain and king safety

Avoids unsafe moves and captures intelligently

Dynamic depth (default: depth = 3)

🏆 Win Tracker
Game results are automatically saved in win_tracker.json:

json
Copy code
{
  "player": 3,
  "ai": 5
}
This persists across multiple sessions and updates after every game.

📸 UI Elements
Score – Number of pieces captured

Timer – 5 minutes per player

Game Over Messages – Displayed when a king is captured or timer ends

Restart – Red button to play again

🧑‍💻 Author
Developed by Yash Vaghasiya
