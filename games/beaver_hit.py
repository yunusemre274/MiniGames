"""
Beaver Hit (Whac-a-Mole) Game
Click on beavers as they pop up to score points!
"""

import streamlit as st
import random
import time

def initialize_game():
    """Initialize game state"""
    if "beaver_score" not in st.session_state:
        st.session_state.beaver_score = 0
        st.session_state.beaver_holes = [False] * 9  # 9 holes, False = empty, True = beaver
        st.session_state.beaver_game_active = False
        st.session_state.beaver_time_left = 30
        st.session_state.beaver_start_time = None
        st.session_state.beaver_last_update = 0

def spawn_beaver():
    """Randomly spawn a beaver in one hole"""
    # Clear all holes
    st.session_state.beaver_holes = [False] * 9
    # Spawn beaver in random hole
    if random.random() < 0.7:  # 70% chance to spawn
        hole = random.randint(0, 8)
        st.session_state.beaver_holes[hole] = True

def hit_beaver(hole_index):
    """Hit a beaver if present"""
    if st.session_state.beaver_holes[hole_index]:
        st.session_state.beaver_score += 10
        st.session_state.beaver_holes[hole_index] = False
        return True
    return False

def start_game():
    """Start a new game"""
    st.session_state.beaver_score = 0
    st.session_state.beaver_holes = [False] * 9
    st.session_state.beaver_game_active = True
    st.session_state.beaver_time_left = 30
    st.session_state.beaver_start_time = time.time()
    st.session_state.beaver_last_update = time.time()

def run():
    """Main game function"""
    initialize_game()
    
    # Custom CSS
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
        }
        .beaver-title {
            text-align: center;
            font-size: 3rem;
            font-weight: bold;
            color: white;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .beaver-score {
            text-align: center;
            font-size: 2rem;
            font-weight: bold;
            color: white;
            margin-bottom: 1rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        .beaver-timer {
            text-align: center;
            font-size: 1.5rem;
            font-weight: bold;
            color: #FFE4B5;
            margin-bottom: 2rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        div[data-testid="column"] .stButton button {
            width: 150px !important;
            height: 150px !important;
            font-size: 5rem !important;
            background-color: #A0522D !important;
            border: 5px solid #654321 !important;
            border-radius: 50% !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="column"] .stButton button:hover {
            transform: scale(1.1) !important;
            background-color: #8B4513 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="beaver-title">🦫 Beaver Hit!</div>', unsafe_allow_html=True)
    
    # Game logic
    if st.session_state.beaver_game_active:
        # Update timer
        elapsed = time.time() - st.session_state.beaver_start_time
        st.session_state.beaver_time_left = max(0, 30 - int(elapsed))
        
        # Check if game over
        if st.session_state.beaver_time_left <= 0:
            st.session_state.beaver_game_active = False
        else:
            # Spawn beaver every 1 second
            if time.time() - st.session_state.beaver_last_update > 1.0:
                spawn_beaver()
                st.session_state.beaver_last_update = time.time()
    
    # Display score and timer
    st.markdown(f'<div class="beaver-score">Score: {st.session_state.beaver_score} 🎯</div>', unsafe_allow_html=True)
    
    if st.session_state.beaver_game_active:
        st.markdown(f'<div class="beaver-timer">⏱️ Time: {st.session_state.beaver_time_left}s</div>', unsafe_allow_html=True)
    else:
        if st.session_state.beaver_score > 0:
            st.markdown(f'<div class="beaver-timer">🎉 Game Over! Final Score: {st.session_state.beaver_score}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="beaver-timer">Click "Start Game" to begin!</div>', unsafe_allow_html=True)
    
    # Display holes in 3x3 grid
    if st.session_state.beaver_game_active:
        st.write("")
        for row in range(3):
            cols = st.columns([1, 2, 2, 2, 1])
            for col in range(3):
                hole_index = row * 3 + col
                with cols[col + 1]:
                    emoji = "🦫" if st.session_state.beaver_holes[hole_index] else "🕳️"
                    if st.button(emoji, key=f"hole_{hole_index}", use_container_width=True):
                        if hit_beaver(hole_index):
                            st.success("🎯 Hit!", icon="✅")
                        st.rerun()
        
        # Auto-refresh to update game state every 1 second
        time.sleep(1.0)
        st.rerun()
    else:
        # Show start button
        st.write("")
        st.write("")
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🎮 Start Game", key="start_beaver", use_container_width=True, type="primary"):
                start_game()
                st.rerun()
