"""
XOX (Tic Tac Toe) Game
Simple turn-based game for two players
"""

import streamlit as st

def initialize_game():
    """Initialize game state"""
    if "xox_board" not in st.session_state:
        st.session_state.xox_board = [[" " for _ in range(3)] for _ in range(3)]
        st.session_state.xox_current_player = "❌"
        st.session_state.xox_winner = None
        st.session_state.xox_game_over = False

def check_winner(board):
    """Check if there's a winner"""
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != " ":
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]
    
    # Check for draw
    if all(cell != " " for row in board for cell in row):
        return "Draw"
    
    return None

def make_move(row, col):
    """Make a move on the board"""
    if st.session_state.xox_board[row][col] == " " and not st.session_state.xox_game_over:
        st.session_state.xox_board[row][col] = st.session_state.xox_current_player
        
        # Check for winner
        winner = check_winner(st.session_state.xox_board)
        if winner:
            st.session_state.xox_winner = winner
            st.session_state.xox_game_over = True
        else:
            # Switch player
            st.session_state.xox_current_player = "⭕" if st.session_state.xox_current_player == "❌" else "❌"

def reset_game():
    """Reset the game"""
    st.session_state.xox_board = [[" " for _ in range(3)] for _ in range(3)]
    st.session_state.xox_current_player = "❌"
    st.session_state.xox_winner = None
    st.session_state.xox_game_over = False

def run():
    """Main game function"""
    initialize_game()
    
    # Custom CSS for XOX game
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .xox-title {
            text-align: center;
            font-size: 3rem;
            font-weight: bold;
            color: white;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .xox-status {
            text-align: center;
            font-size: 1.8rem;
            font-weight: bold;
            margin-bottom: 2rem;
            color: white;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        div[data-testid="column"] .stButton button {
            width: 120px !important;
            height: 120px !important;
            font-size: 4rem !important;
            background-color: #ffffff !important;
            border: 4px solid #34495e !important;
            border-radius: 15px !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;
        }
        div[data-testid="column"] .stButton button:hover {
            background-color: #ecf0f1 !important;
            transform: scale(1.05) !important;
            box-shadow: 0 6px 12px rgba(0,0,0,0.3) !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="xox-title">❌⭕ Tic Tac Toe</div>', unsafe_allow_html=True)
    
    # Display game status
    if st.session_state.xox_game_over:
        if st.session_state.xox_winner == "Draw":
            st.markdown('<div class="xox-status">🤝 It\'s a Draw!</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="xox-status">🎉 {st.session_state.xox_winner} Wins!</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="xox-status">Current Player: {st.session_state.xox_current_player}</div>', unsafe_allow_html=True)
    
    # Display board
    st.write("")
    for row in range(3):
        cols = st.columns([1, 2, 2, 2, 1])
        for col_idx in range(3):
            cell_idx = col_idx
            with cols[col_idx + 1]:
                cell_value = st.session_state.xox_board[row][cell_idx]
                button_label = cell_value if cell_value != " " else "⬜"
                
                if st.button(button_label, key=f"xox_{row}_{cell_idx}", use_container_width=True):
                    make_move(row, cell_idx)
                    st.rerun()
    
    # Reset button
    st.write("")
    st.write("")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🔄 Reset Game", key="reset_xox", use_container_width=True, type="primary"):
            reset_game()
            st.rerun()
