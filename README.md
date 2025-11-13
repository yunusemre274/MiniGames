# 🎮 Game Hub - Mini Windows Desktop

A Streamlit-based game hub that mimics a Windows desktop interface, featuring 5 classic mini games with smooth controls and polished gameplay.

## 🎯 Features

- **Windows-like Desktop UI**: Stunning gradient background with clickable game icons and hover effects
- **5 Fully Playable Games**:
  - 🐍 **Snake** - Navigate the snake to eat apples and grow (with anti-reverse protection)
  - 🕹️ **Flappy Bird** - Guide the bird through pipes with balanced physics
  - ❌⭕ **XOX (Tic Tac Toe)** - Classic two-player strategy game with win detection
  - 🏓 **Ping Pong** - Two-player paddle game with realistic ball physics
  - 🦫 **Beaver Hit** - Whac-a-Mole style clicking game with 30-second timer
- **Smooth Controls**: No page scrolling, optimized game speeds, intuitive navigation
- **Beautiful UI**: Each game has its own themed gradient background and polished interface

## 📁 Project Structure

```
GameHub/
├── app.py                    # Main launcher with desktop UI
├── requirements.txt          # Python dependencies
├── games/
│   ├── __init__.py          # Package initializer
│   ├── snake.py             # Snake game
│   ├── flappy.py            # Flappy Bird game
│   ├── xox.py               # Tic Tac Toe game
│   ├── pong.py              # Ping Pong game
│   └── beaver_hit.py        # Beaver Hit game
└── README.md                # This file
```

## 🚀 Installation

1. **Clone or download this project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 How to Run

Start the Game Hub:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 🕹️ Game Controls

### 🐍 Snake
- **Arrow Keys** (↑ ↓ ← →) to control snake direction
- **No reverse direction allowed** - prevents instant death from going backwards
- Eat apples to grow and score points
- Avoid hitting walls or yourself
- **SPACE** to restart after game over
- **Balanced speed**: Starts slower, gradually increases

### 🕹️ Flappy Bird
- **SPACE** or **Click** to make the bird jump
- Avoid pipes and ground
- Score points by passing through gaps
- **Optimized physics**: Smoother gravity and wider pipe gaps for better playability

### ❌⭕ XOX (Tic Tac Toe)
- Click on empty squares to place your mark
- ❌ goes first
- Get three in a row (horizontal, vertical, or diagonal) to win
- **Reset button** to start a new game

### 🏓 Ping Pong
- **Player 1 (Left Paddle)**: W = Up, S = Down
- **Player 2 (Right Paddle)**: ↑ = Up, ↓ = Down
- First to 5 points wins
- Ball speed increases with each paddle hit
- **No page scrolling** with arrow keys

### 🦫 Beaver Hit
- Click **Start Game** to begin 30-second timer
- Click on beavers as they pop up from holes
- Score **10 points** per successful hit
- Try to get the highest score before time runs out
- Beavers appear randomly every second

## 🎨 Design Philosophy

This project follows the **KISS principle** (Keep It Simple, Stupid):
- Clean, modular structure
- Each game in its own file
- Minimal dependencies
- Easy to understand and extend

## 🔧 Technical Details

- **Framework**: Streamlit 1.28.0+
- **Language**: Python 3.7+
- **Game Rendering**: HTML5 Canvas + JavaScript for interactive games
- **State Management**: Streamlit session_state for navigation and game states
- **Performance**: Optimized game loops with balanced speeds
- **UX Features**:
  - Prevented page scrolling during gameplay
  - Anti-reverse direction in Snake game
  - Buffered input handling for smooth controls
  - Auto-refresh for real-time game updates
  - Themed backgrounds for each game

## ✨ Key Improvements

1. **No Page Scrolling**: Arrow keys and game controls won't scroll the page
2. **Balanced Game Speed**: Snake and Flappy Bird are now perfectly playable
3. **Snake Anti-Reverse**: Can't accidentally reverse into yourself
4. **Beautiful UI**: Each game has custom gradient backgrounds and styling
5. **Smooth Navigation**: Instant game switching with back button
6. **Responsive Controls**: All buttons and inputs work reliably

## 🆕 Adding New Games

To add a new game:

1. Create a new file in `games/` directory (e.g., `games/tetris.py`)
2. Implement a `run()` function that contains the game logic
3. Add the game to the desktop in `app.py`:
   ```python
   games = [
       # ... existing games ...
       {"name": "Tetris", "emoji": "🧱", "key": "tetris"},
   ]
   ```
4. Add the game launcher in the `main()` function:
   ```python
   elif active_game == "tetris":
       from games import tetris
       tetris.run()
   ```

## 📝 License

This project is open source and available for educational purposes.

## 🎉 Project Status

✅ **COMPLETE** - All features implemented and tested
- All 5 games fully functional
- Smooth controls with no page scrolling
- Balanced gameplay speeds
- Beautiful UI with themed backgrounds
- Bug-free navigation and state management

**Enjoy your Game Hub!** 🎮 Have fun playing these classic games!
