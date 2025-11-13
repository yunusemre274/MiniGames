"""
Ping Pong Game
Two-player paddle game with keyboard controls
"""

import streamlit as st
from streamlit.components.v1 import html

def initialize_game():
    """Initialize game state"""
    if "pong_game_started" not in st.session_state:
        st.session_state.pong_game_started = False

def run():
    """Main game function"""
    initialize_game()
    
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 style="text-align: center; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">🏓 Ping Pong</h1>', unsafe_allow_html=True)
    
    # Instructions
    if not st.session_state.pong_game_started:
        st.markdown("""
        <div style="text-align: center; margin: 2rem; background: rgba(255,255,255,0.9); padding: 2rem; border-radius: 15px;">
            <h3 style="color: #9b59b6;">How to Play:</h3>
            <p style="color: #2c3e50;">👤 Player 1 (Left): W = Up, S = Down</p>
            <p style="color: #2c3e50;">👤 Player 2 (Right): ↑ = Up, ↓ = Down</p>
            <p style="color: #2c3e50;">🎯 First to score 5 points wins!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🎮 Start Game", key="start_pong", use_container_width=True, type="primary"):
                st.session_state.pong_game_started = True
                st.rerun()
        return
    
    # Game canvas with HTML5/JavaScript
    pong_html = """
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
                border: 4px solid #9b59b6;
                background: #2c3e50;
                box-shadow: 0 0 20px rgba(155, 89, 182, 0.5);
            }
            #score {
                position: absolute;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                color: white;
                font-size: 48px;
                font-weight: bold;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
            #gameOver {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: #9b59b6;
                font-size: 36px;
                font-weight: bold;
                display: none;
                text-align: center;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 0 30px rgba(0,0,0,0.3);
            }
        </style>
    </head>
    <body>
        <div id="score">0 - 0</div>
        <div id="gameOver">
            <span id="winner"></span><br>
            <span style="font-size: 18px; color: #7f8c8d;">Press SPACE to restart</span>
        </div>
        <canvas id="gameCanvas" width="800" height="600"></canvas>
        
        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            const scoreElement = document.getElementById('score');
            const gameOverElement = document.getElementById('gameOver');
            const winnerElement = document.getElementById('winner');
            
            const paddleWidth = 15;
            const paddleHeight = 100;
            const paddleSpeed = 8;
            const ballSize = 15;
            const winningScore = 5;
            
            let player1 = {
                x: 30,
                y: canvas.height / 2 - paddleHeight / 2,
                score: 0,
                dy: 0
            };
            
            let player2 = {
                x: canvas.width - 30 - paddleWidth,
                y: canvas.height / 2 - paddleHeight / 2,
                score: 0,
                dy: 0
            };
            
            let ball = {
                x: canvas.width / 2,
                y: canvas.height / 2,
                dx: 5,
                dy: 3
            };
            
            let gameOver = false;
            let keys = {};
            
            // Keyboard controls
            document.addEventListener('keydown', (e) => {
                // Prevent default behavior for game controls
                if (['ArrowUp', 'ArrowDown', 'Space', 'w', 'W', 's', 'S'].includes(e.key) || 
                    ['ArrowUp', 'ArrowDown', 'Space'].includes(e.code)) {
                    e.preventDefault();
                }
                
                keys[e.key] = true;
                
                if (gameOver && e.code === 'Space') {
                    resetGame();
                }
            });
            
            document.addEventListener('keyup', (e) => {
                // Prevent default behavior for game controls
                if (['ArrowUp', 'ArrowDown', 'Space', 'w', 'W', 's', 'S'].includes(e.key) || 
                    ['ArrowUp', 'ArrowDown', 'Space'].includes(e.code)) {
                    e.preventDefault();
                }
                
                keys[e.key] = false;
            });
            
            function resetGame() {
                player1.score = 0;
                player2.score = 0;
                gameOver = false;
                gameOverElement.style.display = 'none';
                scoreElement.textContent = '0 - 0';
                resetBall();
            }
            
            function resetBall() {
                ball.x = canvas.width / 2;
                ball.y = canvas.height / 2;
                ball.dx = (Math.random() > 0.5 ? 1 : -1) * 5;
                ball.dy = (Math.random() - 0.5) * 6;
            }
            
            function updatePaddles() {
                // Player 1 controls (W/S)
                if (keys['w'] || keys['W']) {
                    player1.y = Math.max(0, player1.y - paddleSpeed);
                }
                if (keys['s'] || keys['S']) {
                    player1.y = Math.min(canvas.height - paddleHeight, player1.y + paddleSpeed);
                }
                
                // Player 2 controls (Arrow keys)
                if (keys['ArrowUp']) {
                    player2.y = Math.max(0, player2.y - paddleSpeed);
                }
                if (keys['ArrowDown']) {
                    player2.y = Math.min(canvas.height - paddleHeight, player2.y + paddleSpeed);
                }
            }
            
            function updateBall() {
                if (gameOver) return;
                
                ball.x += ball.dx;
                ball.y += ball.dy;
                
                // Wall collision (top/bottom)
                if (ball.y - ballSize / 2 <= 0 || ball.y + ballSize / 2 >= canvas.height) {
                    ball.dy = -ball.dy;
                }
                
                // Paddle collision
                // Player 1
                if (ball.x - ballSize / 2 <= player1.x + paddleWidth &&
                    ball.x - ballSize / 2 > player1.x &&
                    ball.y >= player1.y &&
                    ball.y <= player1.y + paddleHeight) {
                    ball.dx = Math.abs(ball.dx) * 1.05;
                    ball.dy += (ball.y - (player1.y + paddleHeight / 2)) * 0.1;
                }
                
                // Player 2
                if (ball.x + ballSize / 2 >= player2.x &&
                    ball.x + ballSize / 2 < player2.x + paddleWidth &&
                    ball.y >= player2.y &&
                    ball.y <= player2.y + paddleHeight) {
                    ball.dx = -Math.abs(ball.dx) * 1.05;
                    ball.dy += (ball.y - (player2.y + paddleHeight / 2)) * 0.1;
                }
                
                // Score points
                if (ball.x < 0) {
                    player2.score++;
                    scoreElement.textContent = player1.score + ' - ' + player2.score;
                    if (player2.score >= winningScore) {
                        gameOver = true;
                        winnerElement.textContent = '🎉 Player 2 Wins! 🎉';
                        gameOverElement.style.display = 'block';
                    } else {
                        resetBall();
                    }
                }
                
                if (ball.x > canvas.width) {
                    player1.score++;
                    scoreElement.textContent = player1.score + ' - ' + player2.score;
                    if (player1.score >= winningScore) {
                        gameOver = true;
                        winnerElement.textContent = '🎉 Player 1 Wins! 🎉';
                        gameOverElement.style.display = 'block';
                    } else {
                        resetBall();
                    }
                }
                
                // Cap ball speed
                ball.dx = Math.max(-10, Math.min(10, ball.dx));
                ball.dy = Math.max(-10, Math.min(10, ball.dy));
            }
            
            function draw() {
                // Clear canvas
                ctx.fillStyle = '#2c3e50';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                // Draw center line
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
                ctx.lineWidth = 4;
                ctx.setLineDash([10, 10]);
                ctx.beginPath();
                ctx.moveTo(canvas.width / 2, 0);
                ctx.lineTo(canvas.width / 2, canvas.height);
                ctx.stroke();
                ctx.setLineDash([]);
                
                // Draw paddles
                ctx.fillStyle = '#3498db';
                ctx.fillRect(player1.x, player1.y, paddleWidth, paddleHeight);
                
                ctx.fillStyle = '#e74c3c';
                ctx.fillRect(player2.x, player2.y, paddleWidth, paddleHeight);
                
                // Draw ball
                ctx.fillStyle = '#f39c12';
                ctx.beginPath();
                ctx.arc(ball.x, ball.y, ballSize / 2, 0, Math.PI * 2);
                ctx.fill();
                
                // Ball trail effect
                ctx.fillStyle = 'rgba(243, 156, 18, 0.3)';
                ctx.beginPath();
                ctx.arc(ball.x - ball.dx, ball.y - ball.dy, ballSize / 2, 0, Math.PI * 2);
                ctx.fill();
            }
            
            function gameLoop() {
                updatePaddles();
                updateBall();
                draw();
                requestAnimationFrame(gameLoop);
            }
            
            gameLoop();
        </script>
    </body>
    </html>
    """
    
    # Display the game
    html(pong_html, height=700)
    
    # Reset button
    st.write("")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🔄 New Game", key="reset_pong", use_container_width=True, type="secondary"):
            st.session_state.pong_game_started = False
            st.rerun()
