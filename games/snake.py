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
    
    # Instructions
    if not st.session_state.snake_game_started:
        st.markdown("""
        <div style="text-align: center; margin: 2rem; background: rgba(255,255,255,0.9); padding: 2rem; border-radius: 15px;">
            <h3 style="color: #27ae60;">How to Play:</h3>
            <p style="color: #2c3e50;">🎮 Use Arrow Keys (↑ ↓ ← →) to control the snake</p>
            <p style="color: #2c3e50;">🍎 Eat the red apples to grow and score points</p>
            <p style="color: #2c3e50;">⚠️ Don't hit the walls or yourself!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🎮 Start Game", key="start_snake", use_container_width=True, type="primary"):
                st.session_state.snake_game_started = True
                st.rerun()
        return
    
    # Game canvas with HTML5/JavaScript
    snake_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0;
                background: #1a1a1a;
                font-family: Arial, sans-serif;
            }
            #gameCanvas {
                border: 4px solid #27ae60;
                background: #2c3e50;
                box-shadow: 0 0 20px rgba(39, 174, 96, 0.5);
            }
            #score {
                position: absolute;
                top: 10px;
                left: 50%;
                transform: translateX(-50%);
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
            #gameOver {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: #e74c3c;
                font-size: 36px;
                font-weight: bold;
                display: none;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div id="score">Score: 0</div>
        <div id="gameOver">
            GAME OVER!<br>
            <span style="font-size: 20px;">Press SPACE to restart</span>
        </div>
        <canvas id="gameCanvas" width="600" height="600"></canvas>
        
        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            const scoreElement = document.getElementById('score');
            const gameOverElement = document.getElementById('gameOver');
            
            const gridSize = 20;
            const tileCount = 30;
            
            let snake = [{x: 15, y: 15}];
            let direction = {x: 0, y: 0};
            let nextDirection = {x: 0, y: 0}; // Buffer for next direction
            let food = {x: 10, y: 10};
            let score = 0;
            let gameOver = false;
            let speed = 150; // Slower initial speed (was 100)
            
            function randomFood() {
                food.x = Math.floor(Math.random() * tileCount);
                food.y = Math.floor(Math.random() * tileCount);
                
                // Check if food is on snake
                for (let segment of snake) {
                    if (segment.x === food.x && segment.y === food.y) {
                        randomFood();
                        break;
                    }
                }
            }
            
            function drawGame() {
                if (gameOver) return;
                
                // Update direction from buffered input
                direction = nextDirection;
                
                // Move snake
                if (direction.x !== 0 || direction.y !== 0) {
                    const head = {
                        x: snake[0].x + direction.x,
                        y: snake[0].y + direction.y
                    };
                    
                    // Check wall collision
                    if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
                        gameOver = true;
                        gameOverElement.style.display = 'block';
                        return;
                    }
                    
                    // Check self collision
                    for (let segment of snake) {
                        if (segment.x === head.x && segment.y === head.y) {
                            gameOver = true;
                            gameOverElement.style.display = 'block';
                            return;
                        }
                    }
                    
                    snake.unshift(head);
                    
                    // Check food collision
                    if (head.x === food.x && head.y === food.y) {
                        score += 10;
                        scoreElement.textContent = 'Score: ' + score;
                        randomFood();
                        speed = Math.max(80, speed - 1); // Slower speed increase (was 50, -2)
                    } else {
                        snake.pop();
                    }
                }
                
                // Clear canvas
                ctx.fillStyle = '#2c3e50';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                // Draw snake
                ctx.fillStyle = '#27ae60';
                for (let i = 0; i < snake.length; i++) {
                    const segment = snake[i];
                    ctx.fillRect(
                        segment.x * gridSize,
                        segment.y * gridSize,
                        gridSize - 2,
                        gridSize - 2
                    );
                    
                    // Draw head differently
                    if (i === 0) {
                        ctx.fillStyle = '#2ecc71';
                        ctx.fillRect(
                            segment.x * gridSize + 2,
                            segment.y * gridSize + 2,
                            gridSize - 6,
                            gridSize - 6
                        );
                        ctx.fillStyle = '#27ae60';
                    }
                }
                
                // Draw food
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
            }
            
            // Keyboard controls
            document.addEventListener('keydown', (e) => {
                // Prevent default behavior for arrow keys and space
                if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Space'].includes(e.code)) {
                    e.preventDefault();
                }
                
                if (gameOver && e.code === 'Space') {
                    // Restart game
                    snake = [{x: 15, y: 15}];
                    direction = {x: 0, y: 0};
                    nextDirection = {x: 0, y: 0};
                    score = 0;
                    gameOver = false;
                    speed = 150; // Match initial speed
                    scoreElement.textContent = 'Score: 0';
                    gameOverElement.style.display = 'none';
                    randomFood();
                    return;
                }
                
                switch(e.key) {
                    case 'ArrowUp':
                        // Can't go up if currently going down
                        if (direction.y !== 1) {
                            nextDirection = {x: 0, y: -1};
                        }
                        break;
                    case 'ArrowDown':
                        // Can't go down if currently going up
                        if (direction.y !== -1) {
                            nextDirection = {x: 0, y: 1};
                        }
                        break;
                    case 'ArrowLeft':
                        // Can't go left if currently going right
                        if (direction.x !== 1) {
                            nextDirection = {x: -1, y: 0};
                        }
                        break;
                    case 'ArrowRight':
                        // Can't go right if currently going left
                        if (direction.x !== -1) {
                            nextDirection = {x: 1, y: 0};
                        }
                        break;
                }
            });
            
            // Game loop
            function gameLoop() {
                drawGame();
                setTimeout(gameLoop, speed);
            }
            
            randomFood();
            gameLoop();
        </script>
    </body>
    </html>
    """
    
    # Display the game
    html(snake_html, height=700)
    
    # Reset button
    st.write("")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🔄 New Game", key="reset_snake", use_container_width=True, type="secondary"):
            st.session_state.snake_game_started = False
            st.session_state.snake_game_over = False
            st.session_state.snake_score = 0
            st.rerun()
