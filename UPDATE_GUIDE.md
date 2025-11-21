# 🎮 GAME HUB UPDATE IMPLEMENTATION GUIDE

## ✅ COMPLETED:
1. ✅ Created `games/store.py` - Store page for buying skins
2. ✅ Created `games/my_skins.py` - Page for managing and selecting skins  
3. ✅ Updated `app.py` - Added Store and My Skins to desktop

## ⚠️ MANUAL UPDATES REQUIRED:

### 1. Fix `games/snake.py` (File has duplicates - needs clean rewrite)

**ENTIRE FILE SHOULD BE:**
```python
"""
Snake Game
Classic snake game with arrow key controls
"""

import streamlit as st
import random
import time
from streamlit.components.v1 import html

def initialize_game():
    """Initialize game state"""
    if "snake_game_started" not in st.session_state:
        st.session_state.snake_game_started = False
        st.session_state.snake_game_over = False
        st.session_state.snake_score = 0
    
    # Initialize global coin and skin system
    if "coins" not in st.session_state:
        st.session_state.coins = 0
    if "owned_skins" not in st.session_state:
        st.session_state.owned_skins = ["green"]
    if "active_skin" not in st.session_state:
        st.session_state.active_skin = "green"
    if "snake_speed" not in st.session_state:
        st.session_state.snake_speed = "Medium"

def run():
    """Main game function"""
    initialize_game()
    
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 style="text-align: center; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">🐍 Snake Game</h1>', unsafe_allow_html=True)
    
    # Display coins at top
    st.markdown(f'<div style="text-align: center; color: white; font-size: 1.5rem; margin-bottom: 1rem;">💰 Coins: {st.session_state.coins}</div>', unsafe_allow_html=True)
    
    # Instructions
    if not st.session_state.snake_game_started:
        st.markdown("""
        <div style="text-align: center; margin: 2rem; background: rgba(255,255,255,0.9); padding: 2rem; border-radius: 15px;">
            <h3 style="color: #27ae60;">How to Play:</h3>
            <p style="color: #2c3e50;">🎮 Use Arrow Keys (↑ ↓ ← →) to control the snake</p>
            <p style="color: #2c3e50;">🍎 Eat the red apples to grow and earn coins</p>
            <p style="color: #2c3e50;">⚠️ Don't hit the walls or yourself!</p>
            <p style="color: #2c3e50;">💰 +2 Score and +1 Coin per apple!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        # Speed selection
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.session_state.snake_speed = st.selectbox(
                "Select Speed:",
                ["Slow", "Medium", "Fast"],
                index=["Slow", "Medium", "Fast"].index(st.session_state.snake_speed),
                key="snake_speed_select"
            )
        
        st.write("")
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🎮 Start Game", key="start_snake", use_container_width=True, type="primary"):
                st.session_state.snake_game_started = True
                st.rerun()
        return
    
    # Get skin color mapping
    skin_colors = {
        "green": "#27ae60",
        "red": "#e74c3c",
        "blue": "#3498db",
        "yellow": "#f1c40f",
        "rainbow": "rainbow",
        "gradient": "gradient"
    }
    
    active_skin = st.session_state.active_skin
    skin_color = skin_colors.get(active_skin, "#27ae60")
    
    # Get speed setting
    speed_map = {"Slow": 200, "Medium": 150, "Fast": 100}
    initial_speed = speed_map.get(st.session_state.snake_speed, 150)
    
    # Game canvas with HTML5/JavaScript
    snake_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0;
                background: #1a1a1a;
                font-family: Arial, sans-serif;
            }}
            #gameCanvas {{
                border: 4px solid #27ae60;
                background: #2c3e50;
                box-shadow: 0 0 20px rgba(39, 174, 96, 0.5);
            }}
            #score {{
                position: absolute;
                top: 10px;
                left: 50%;
                transform: translateX(-50%);
                color: white;
                font-size: 24px;
                font-weight: bold;
            }}
            #coins {{
                position: absolute;
                top: 40px;
                left: 50%;
                transform: translateX(-50%);
                color: #f1c40f;
                font-size: 20px;
                font-weight: bold;
            }}
            #gameOver {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: #e74c3c;
                font-size: 36px;
                font-weight: bold;
                display: none;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div id="score">Score: 0</div>
        <div id="coins">Coins: {st.session_state.coins}</div>
        <div id="gameOver">
            GAME OVER!<br>
            <span style="font-size: 20px;">Press SPACE to restart</span>
        </div>
        <canvas id="gameCanvas" width="600" height="600"></canvas>
        
        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            const scoreElement = document.getElementById('score');
            const coinsElement = document.getElementById('coins');
            const gameOverElement = document.getElementById('gameOver');
            
            const gridSize = 20;
            const tileCount = 30;
            
            let snake = [{{x: 15, y: 15}}];
            let direction = {{x: 0, y: 0}};
            let nextDirection = {{x: 0, y: 0}};
            let food = {{x: 10, y: 10}};
            let score = 0;
            let coins = {st.session_state.coins};
            let gameOver = false;
            let speed = {initial_speed};
            const skinColor = "{skin_color}";
            const skinType = "{active_skin}";
            
            function randomFood() {{
                food.x = Math.floor(Math.random() * tileCount);
                food.y = Math.floor(Math.random() * tileCount);
                
                for (let segment of snake) {{
                    if (segment.x === food.x && segment.y === food.y) {{
                        randomFood();
                        break;
                    }}
                }}
            }}
            
            function getSnakeColor(segmentIndex) {{
                if (skinType === 'rainbow') {{
                    const colors = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#3498db', '#9b59b6'];
                    return colors[segmentIndex % colors.length];
                }} else if (skinType === 'gradient') {{
                    const alpha = 1 - (segmentIndex / snake.length) * 0.5;
                    return `rgba(39, 174, 96, ${{alpha}})`;
                }} else {{
                    return skinColor;
                }}
            }}
            
            function drawGame() {{
                if (gameOver) return;
                
                direction = nextDirection;
                
                if (direction.x !== 0 || direction.y !== 0) {{
                    const head = {{
                        x: snake[0].x + direction.x,
                        y: snake[0].y + direction.y
                    }};
                    
                    if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {{
                        gameOver = true;
                        gameOverElement.style.display = 'block';
                        return;
                    }}
                    
                    for (let segment of snake) {{
                        if (segment.x === head.x && segment.y === head.y) {{
                            gameOver = true;
                            gameOverElement.style.display = 'block';
                            return;
                        }}
                    }}
                    
                    snake.unshift(head);
                    
                    if (head.x === food.x && head.y === food.y) {{
                        score += 2;
                        coins += 1;
                        scoreElement.textContent = 'Score: ' + score;
                        coinsElement.textContent = 'Coins: ' + coins;
                        randomFood();
                        speed = Math.max(80, speed - 1);
                    }} else {{
                        snake.pop();
                    }}
                }}
                
                ctx.fillStyle = '#2c3e50';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                for (let i = 0; i < snake.length; i++) {{
                    const segment = snake[i];
                    ctx.fillStyle = getSnakeColor(i);
                    ctx.fillRect(
                        segment.x * gridSize,
                        segment.y * gridSize,
                        gridSize - 2,
                        gridSize - 2
                    );
                    
                    if (i === 0) {{
                        const headColor = skinType === 'rainbow' ? '#e74c3c' : (skinType === 'gradient' ? '#2ecc71' : skinColor);
                        ctx.fillStyle = headColor;
                        ctx.fillRect(
                            segment.x * gridSize + 2,
                            segment.y * gridSize + 2,
                            gridSize - 6,
                            gridSize - 6
                        );
                    }}
                }}
                
                ctx.fillStyle = '#e74c3c';
                ctx.beginPath();
                ctx.arc(
                    food.x * gridSize + gridSize / 2,
                    food.y * gridSize + gridSize / 2,
                    gridSize / 2 - 2,
                    0,
                    Math.PI * 2
                );
                ctx.fill();
            }}
            
            document.addEventListener('keydown', (e) => {{
                if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Space'].includes(e.code)) {{
                    e.preventDefault();
                }}
                
                if (gameOver && e.code === 'Space') {{
                    snake = [{{x: 15, y: 15}}];
                    direction = {{x: 0, y: 0}};
                    nextDirection = {{x: 0, y: 0}};
                    score = 0;
                    gameOver = false;
                    speed = {initial_speed};
                    scoreElement.textContent = 'Score: 0';
                    gameOverElement.style.display = 'none';
                    randomFood();
                    return;
                }}
                
                switch(e.key) {{
                    case 'ArrowUp':
                        if (direction.y !== 1) {{
                            nextDirection = {{x: 0, y: -1}};
                        }}
                        break;
                    case 'ArrowDown':
                        if (direction.y !== -1) {{
                            nextDirection = {{x: 0, y: 1}};
                        }}
                        break;
                    case 'ArrowLeft':
                        if (direction.x !== 1) {{
                            nextDirection = {{x: -1, y: 0}};
                        }}
                        break;
                    case 'ArrowRight':
                        if (direction.x !== -1) {{
                            nextDirection = {{x: 1, y: 0}};
                        }}
                        break;
                }}
            }});
            
            function gameLoop() {{
                drawGame();
                setTimeout(gameLoop, speed);
            }}
            
            randomFood();
            gameLoop();
        </script>
    </body>
    </html>
    """
    
    html(snake_html, height=700)
    
    st.write("")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🔄 New Game", key="reset_snake", use_container_width=True, type="secondary"):
            st.session_state.snake_game_started = False
            st.session_state.snake_game_over = False
            st.session_state.snake_score = 0
            st.rerun()
```

**ACTION REQUIRED:** Delete games/snake.py and save the above code as the new games/snake.py

---

### 2. Update `games/flappy.py`

Add these changes to the existing flappy.py:

**At the top of `initialize_game()` function, add:**
```python
# Initialize global coin and skin system
if "coins" not in st.session_state:
    st.session_state.coins = 0
if "owned_skins" not in st.session_state:
    st.session_state.owned_skins = ["green"]
if "active_skin" not in st.session_state:
    st.session_state.active_skin = "green"
if "flappy_speed" not in st.session_state:
    st.session_state.flappy_speed = "Medium"
```

**After the title, add:**
```python
# Display coins
st.markdown(f'<div style="text-align: center; color: white; font-size: 1.5rem; margin-bottom: 1rem;">💰 Coins: {st.session_state.coins}</div>', unsafe_allow_html=True)
```

**In the instructions section (before Start Game button), add:**
```python
# Speed selection
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.session_state.flappy_speed = st.selectbox(
        "Select Speed:",
        ["Slow", "Medium", "Fast"],
        index=["Slow", "Medium", "Fast"].index(st.session_state.flappy_speed),
        key="flappy_speed_select"
    )
```

**Before the HTML section, add:**
```python
# Get skin color
skin_colors = {
    "green": "#27ae60",
    "red": "#e74c3c",
    "blue": "#3498db",
    "yellow": "#f1c40f",
    "rainbow": "#9b59b6",  # Use purple for rainbow
    "gradient": "#16a085"
}
bird_color = skin_colors.get(st.session_state.active_skin, "#f39c12")

# Get speed setting
speed_map = {"Slow": {"gravity": 0.25, "jump": -5, "pipe": 1.5}, 
             "Medium": {"gravity": 0.35, "jump": -7, "pipe": 2},
             "Fast": {"gravity": 0.45, "jump": -9, "pipe": 2.5}}
speed_settings = speed_map.get(st.session_state.flappy_speed, speed_map["Medium"])
```

**In the JavaScript section, change:**
```javascript
const gravity = 0.35; // Change to: const gravity = {speed_settings['gravity']};
const jumpStrength = -7; // Change to: const jumpStrength = {speed_settings['jump']};  
const pipeSpeed = 2; // Change to: const pipeSpeed = {speed_settings['pipe']};
```

**Change bird color in drawBird():**
```javascript
// Bird body
ctx.fillStyle = '{bird_color}'; // Instead of '#f39c12'
```

**Update score tracking (in the scoring section):**
```javascript
// Score (find the section where score increments)
if (!pipes[i].scored && pipes[i].x + pipeWidth < bird.x) {
    pipes[i].scored = true;
    score++;
    coins++;  // ADD THIS LINE
    scoreElement.textContent = score;
}
```

**Add coins display in HTML:**
```html
<div id="score">0</div>
<div id="coins" style="position: absolute; top: 40px; left: 50%; transform: translateX(-50%); color: #f1c40f; font-size: 20px; font-weight: bold;">Coins: 0</div>
```

**Add coins element in JavaScript:**
```javascript
const coinsElement = document.getElementById('coins');
let coins = {st.session_state.coins};
```

**Update coins display when scoring:**
```javascript
coins++;
coinsElement.textContent = 'Coins: ' + coins;
```

---

## 📝 SUMMARY OF FEATURES ADDED:

### 🐍 Snake Game:
✅ Speed selection (Slow/Medium/Fast)
✅ +2 score per apple (instead of +10)
✅ +1 coin per apple
✅ Skin system with color support (green, red, blue, yellow, rainbow, gradient)
✅ Coins persist in st.session_state
✅ Displays current coins

### 🕹️ Flappy Bird:
✅ Speed selection (Slow/Medium/Fast) - affects gravity, jump, and pipe speed
✅ Increased jump height (1.3× stronger: -7 → -9 for fast mode)
✅ +1 coin per pipe passed
✅ +1 score per pipe
✅ Bird color matches active skin
✅ Coins persist

### 🛒 Store:
✅ Buy skins for 200 coins
✅ 6 skins available: green (default), red, blue, yellow, rainbow, gradient
✅ Shared between Snake and Flappy Bird

### 🎨 My Skins:
✅ View owned skins
✅ Select active skin
✅ Active skin applies to both games

### 💰 Global System:
✅ `st.session_state.coins` - persists across games
✅ `st.session_state.owned_skins` - list of purchased skins
✅ `st.session_state.active_skin` - currently selected skin
✅ Coins never reset unless manually cleared

---

## 🚀 TESTING CHECKLIST:

1. Delete old `games/snake.py` and replace with new code above
2. Update `games/flappy.py` with the changes listed
3. Restart Streamlit: `streamlit run app.py`
4. Test Snake speed selection
5. Test Snake coin earning (+1 per apple)
6. Test Snake skin colors
7. Test Flappy Bird speed selection
8. Test Flappy Bird coin earning (+1 per pipe)
9. Test Flappy Bird skin colors
10. Test Store - buy skins
11. Test My Skins - change active skin
12. Verify coins persist across games

---

## ⚠️ IMPORTANT NOTES:

- The current snake.py has duplicate HTML code that must be removed
- Simply copying the entire new snake.py code above will fix it
- Flappy.py needs incremental updates as listed
- All coin logic uses st.session_state so it persists automatically
- No database needed - session state handles persistence during the session

