"""
Flappy Bird Game
Click or press SPACE to make the bird jump!
"""

import streamlit as st
from streamlit.components.v1 import html

def initialize_game():
    """Initialize game state"""
    if "flappy_game_started" not in st.session_state:
        st.session_state.flappy_game_started = False
    
    # Initialize speed setting
    if "flappy_speed" not in st.session_state:
        st.session_state.flappy_speed = "Medium"

def run():
    """Main game function"""
    initialize_game()
    
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to bottom, #87CEEB 0%, #E0F6FF 100%);
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 style="text-align: center; color: #3498db; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">🕹️ Flappy Bird</h1>', unsafe_allow_html=True)
    
    # Instructions
    if not st.session_state.flappy_game_started:
        st.markdown("""
        <div style="text-align: center; margin: 2rem; background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="color: #3498db;">How to Play:</h3>
            <p style="color: #2c3e50;">🐦 Click or press SPACE to make the bird fly</p>
            <p style="color: #2c3e50;">🚧 Avoid the pipes!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        # Speed selection
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.session_state.flappy_speed = st.selectbox(
                "Select Speed:",
                ["Slow", "Medium", "Fast"],
                index=["Slow", "Medium", "Fast"].index(st.session_state.flappy_speed),
                key="flappy_speed_select"
            )
        
        st.write("")
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🎮 Start Game", key="start_flappy", use_container_width=True, type="primary"):
                st.session_state.flappy_game_started = True
                st.rerun()
        return
    
    # Use default green color for bird
    bird_color = "#27ae60"
    
    # Get speed settings
    speed_map = {
        "Slow": {"gravity": 0.3, "jump": -5.5, "pipe": 2},
        "Medium": {"gravity": 0.4, "jump": -7.5, "pipe": 2.5},
        "Fast": {"gravity": 0.5, "jump": -9.5, "pipe": 3}
    }
    speed_settings = speed_map.get(st.session_state.flappy_speed, speed_map["Medium"])
    
    # Game canvas with HTML5/JavaScript
    flappy_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0;
                background: linear-gradient(to bottom, #87CEEB 0%, #E0F6FF 100%);
                font-family: Arial, sans-serif;
            }}
            #gameCanvas {{
                border: 4px solid #3498db;
                box-shadow: 0 0 20px rgba(52, 152, 219, 0.5);
                cursor: pointer;
            }}
            #score {{
                position: absolute;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                color: white;
                font-size: 48px;
                font-weight: bold;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
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
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 0 30px rgba(0,0,0,0.3);
            }}
        </style>
    </head>
    <body>
        <div id="score">0</div>
        <div id="gameOver">
            GAME OVER!<br>
            <span style="font-size: 24px; color: #3498db;">Score: <span id="finalScore">0</span></span><br>
            <span style="font-size: 18px; color: #7f8c8d;">Click or press SPACE to restart</span>
        </div>
        <canvas id="gameCanvas" width="400" height="600"></canvas>
        
        <script>
            const canvas = document.getElementById('gameCanvas');
            const ctx = canvas.getContext('2d');
            const scoreElement = document.getElementById('score');
            const gameOverElement = document.getElementById('gameOver');
            const finalScoreElement = document.getElementById('finalScore');
            
            let bird = {{
                x: 80,
                y: 250,
                velocity: 0,
                radius: 15
            }};
            
            let pipes = [];
            let score = 0;
            let gameOver = false;
            let frameCount = 0;
            const birdColor = "{bird_color}";
            
            const gravity = {speed_settings['gravity']};
            const jumpStrength = {speed_settings['jump']};
            const pipeWidth = 60;
            const pipeGap = 180;
            const pipeSpeed = {speed_settings['pipe']};
            
            function createPipe() {{
                const minHeight = 50;
                const maxHeight = canvas.height - pipeGap - 50;
                const height = Math.random() * (maxHeight - minHeight) + minHeight;
                
                pipes.push({{
                    x: canvas.width,
                    topHeight: height,
                    bottomY: height + pipeGap,
                    scored: false
                }});
            }}
            
            function jump() {{
                if (!gameOver) {{
                    bird.velocity = jumpStrength;
                }} else {{
                    // Restart game
                    bird = {{
                        x: 80,
                        y: 250,
                        velocity: 0,
                        radius: 15
                    }};
                    pipes = [];
                    score = 0;
                    gameOver = false;
                    frameCount = 0;
                    scoreElement.textContent = '0';
                    gameOverElement.style.display = 'none';
                }}
            }}
            
            canvas.addEventListener('click', jump);
            document.addEventListener('keydown', (e) => {{
                if (e.code === 'Space') {{
                    e.preventDefault();
                    jump();
                }}
            }});
            
            function drawBird() {{
                // Bird body
                ctx.fillStyle = birdColor;
                ctx.beginPath();
                ctx.arc(bird.x, bird.y, bird.radius, 0, Math.PI * 2);
                ctx.fill();
                
                // Bird eye
                ctx.fillStyle = 'white';
                ctx.beginPath();
                ctx.arc(bird.x + 5, bird.y - 3, 5, 0, Math.PI * 2);
                ctx.fill();
                
                ctx.fillStyle = 'black';
                ctx.beginPath();
                ctx.arc(bird.x + 6, bird.y - 3, 3, 0, Math.PI * 2);
                ctx.fill();
                
                // Bird beak
                ctx.fillStyle = '#e67e22';
                ctx.beginPath();
                ctx.moveTo(bird.x + bird.radius, bird.y);
                ctx.lineTo(bird.x + bird.radius + 10, bird.y - 3);
                ctx.lineTo(bird.x + bird.radius + 10, bird.y + 3);
                ctx.closePath();
                ctx.fill();
            }}
            
            function drawPipes() {{
                ctx.fillStyle = '#27ae60';
                pipes.forEach(pipe => {{
                    // Top pipe
                    ctx.fillRect(pipe.x, 0, pipeWidth, pipe.topHeight);
                    // Top pipe cap
                    ctx.fillRect(pipe.x - 5, pipe.topHeight - 20, pipeWidth + 10, 20);
                    
                    // Bottom pipe
                    ctx.fillRect(pipe.x, pipe.bottomY, pipeWidth, canvas.height - pipe.bottomY);
                    // Bottom pipe cap
                    ctx.fillRect(pipe.x - 5, pipe.bottomY, pipeWidth + 10, 20);
                    
                    // Pipe details
                    ctx.strokeStyle = '#229954';
                    ctx.lineWidth = 3;
                    ctx.strokeRect(pipe.x, 0, pipeWidth, pipe.topHeight);
                    ctx.strokeRect(pipe.x, pipe.bottomY, pipeWidth, canvas.height - pipe.bottomY);
                }});
            }}
            
            function updateGame() {{
                if (gameOver) return;
                
                frameCount++;
                
                // Update bird
                bird.velocity += gravity;
                bird.y += bird.velocity;
                
                // Check ground/ceiling collision
                if (bird.y + bird.radius > canvas.height || bird.y - bird.radius < 0) {{
                    gameOver = true;
                    gameOverElement.style.display = 'block';
                    finalScoreElement.textContent = score;
                    return;
                }}
                
                // Create pipes
                if (frameCount % 110 === 0) {{ // More spacing between pipes (was 90)
                    createPipe();
                }}
                
                // Update pipes
                for (let i = pipes.length - 1; i >= 0; i--) {{
                    pipes[i].x -= pipeSpeed;
                    
                    // Remove off-screen pipes
                    if (pipes[i].x + pipeWidth < 0) {{
                        pipes.splice(i, 1);
                        continue;
                    }}
                    
                    // Check collision
                    if (bird.x + bird.radius > pipes[i].x && 
                        bird.x - bird.radius < pipes[i].x + pipeWidth) {{
                        if (bird.y - bird.radius < pipes[i].topHeight || 
                            bird.y + bird.radius > pipes[i].bottomY) {{
                            gameOver = true;
                            gameOverElement.style.display = 'block';
                            finalScoreElement.textContent = score;
                            return;
                        }}
                    }}
                    
                    // Score
                    if (!pipes[i].scored && pipes[i].x + pipeWidth < bird.x) {{
                        pipes[i].scored = true;
                        score++;
                        scoreElement.textContent = score;
                    }}
                }}
            }}
            
            function drawGame() {{
                // Sky background
                const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
                gradient.addColorStop(0, '#87CEEB');
                gradient.addColorStop(1, '#E0F6FF');
                ctx.fillStyle = gradient;
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                // Clouds
                ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
                ctx.beginPath();
                ctx.arc(100, 80, 30, 0, Math.PI * 2);
                ctx.arc(130, 80, 40, 0, Math.PI * 2);
                ctx.arc(160, 80, 30, 0, Math.PI * 2);
                ctx.fill();
                
                drawPipes();
                drawBird();
                updateGame();
                requestAnimationFrame(drawGame);
            }}
            
            drawGame();
        </script>
    </body>
    </html>
    """
    
    # Display the game
    html(flappy_html, height=700)
    
    st.write("")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🏠 Menu", key="menu_flappy", use_container_width=True, type="secondary"):
            st.session_state.current_page = "desktop"
            st.rerun()
    with col2:
        if st.button("🔄 New Game", key="reset_flappy", use_container_width=True, type="secondary"):
            st.session_state.flappy_game_started = False
            st.rerun()
