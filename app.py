"""
Game Hub - Main Desktop Interface
A Windows-like desktop launcher for mini games
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Game Hub 🎮",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Windows-like desktop
st.markdown("""
<style>
    /* Dark desktop background */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Desktop title */
    .desktop-title {
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-bottom: 2rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Game icon container */
    .game-icon {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        cursor: pointer;
    }
    
    .game-icon:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-5px);
        border-color: rgba(255, 255, 255, 0.5);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    /* Game icon emoji */
    .game-emoji {
        font-size: 5rem;
        margin-bottom: 10px;
    }
    
    /* Game title */
    .game-title {
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    # Button styling */
    .stButton button {
        width: 100%;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        font-size: 1rem !important;
    }
    
    .stButton > button:hover {
        background: transparent !important;
    }
    
    /* Back button */
    div[data-testid="stHorizontalBlock"] > div:first-child .stButton button {
        background: rgba(255, 255, 255, 0.2) !important;
        border: 2px solid white !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        color: white !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stHorizontalBlock"] > div:first-child .stButton button:hover {
        background: rgba(255, 255, 255, 0.3) !important;
        transform: scale(1.05) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "active_game" not in st.session_state:
    st.session_state.active_game = None

def show_desktop():
    """Display the main desktop interface with game icons"""
    
    st.markdown('<div class="desktop-title">🎮 Game Hub Desktop</div>', unsafe_allow_html=True)
    
    # Game definitions
    games = [
        {"name": "Snake", "emoji": "🐍", "key": "snake"},
        {"name": "Flappy Bird", "emoji": "🕹️", "key": "flappy"},
        {"name": "XOX", "emoji": "❌⭕", "key": "xox"},
        {"name": "Ping Pong", "emoji": "🏓", "key": "pong"},
        {"name": "Beaver Hit", "emoji": "🦫", "key": "beaver"},
    ]
    
    # Create grid layout (3 columns for better spacing)
    st.write("")  # Spacing
    st.write("")
    
    # First row - 3 games
    cols = st.columns(3)
    for idx in range(3):
        with cols[idx]:
            game = games[idx]
            st.markdown(f"""
                <div class="game-icon">
                    <div class="game-emoji">{game['emoji']}</div>
                    <div class="game-title">{game['name']}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Launch {game['name']}", key=f"btn_{game['key']}", use_container_width=True):
                st.session_state.active_game = game['key']
                st.rerun()
    
    st.write("")  # Spacing between rows
    
    # Second row - 2 games (centered)
    cols = st.columns([1, 2, 2, 1])
    for idx in range(2):
        with cols[idx + 1]:
            game = games[idx + 3]
            st.markdown(f"""
                <div class="game-icon">
                    <div class="game-emoji">{game['emoji']}</div>
                    <div class="game-title">{game['name']}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Launch {game['name']}", key=f"btn_{game['key']}", use_container_width=True):
                st.session_state.active_game = game['key']
                st.rerun()

def back_to_desktop():
    """Return to the main desktop"""
    st.session_state.active_game = None
    st.rerun()

def main():
    """Main application logic"""
    
    # Check which game is active
    active_game = st.session_state.get("active_game")
    
    if active_game is None:
        # Show desktop
        show_desktop()
    else:
        # Show back button at the top
        col1, col2, col3 = st.columns([1, 4, 1])
        with col1:
            if st.button("⬅️ Back to Desktop", key="back_button", use_container_width=True, type="secondary"):
                back_to_desktop()
        
        # Launch the selected game
        try:
            if active_game == "snake":
                from games import snake
                snake.run()
            elif active_game == "flappy":
                from games import flappy
                flappy.run()
            elif active_game == "xox":
                from games import xox
                xox.run()
            elif active_game == "pong":
                from games import pong
                pong.run()
            elif active_game == "beaver":
                from games import beaver_hit
                beaver_hit.run()
        except Exception as e:
            st.error(f"Error loading game: {e}")
            st.info("This game is still under development. Click 'Back to Desktop' to return.")
            if st.button("🏠 Return to Desktop", key="error_back"):
                back_to_desktop()

if __name__ == "__main__":
    main()
