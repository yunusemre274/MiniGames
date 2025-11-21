"""
Store Page - Buy Skins for Games
"""

import streamlit as st

def run():
    """Store page for buying skins"""
    
    # Initialize if needed
    if "coins" not in st.session_state:
        st.session_state.coins = 0
    if "owned_skins" not in st.session_state:
        st.session_state.owned_skins = ["green"]
    if "active_skin" not in st.session_state:
        st.session_state.active_skin = "green"
    
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 style="text-align: center; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">🛒 Skin Store</h1>', unsafe_allow_html=True)
    
    st.markdown(f'<div style="text-align: center; color: white; font-size: 2rem; margin: 2rem;">💰 Your Coins: {st.session_state.coins}</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="text-align: center; color: white; margin-bottom: 2rem;">Purchase skins for 200 coins each</div>', unsafe_allow_html=True)
    
    # Available skins
    skins = {
        "green": {"name": "Green", "color": "#27ae60", "price": 0, "default": True},
        "red": {"name": "Red", "color": "#e74c3c", "price": 200},
        "blue": {"name": "Blue", "color": "#3498db", "price": 200},
        "yellow": {"name": "Yellow", "color": "#f1c40f", "price": 200},
        "rainbow": {"name": "Rainbow", "color": "linear-gradient(90deg, #e74c3c, #f39c12, #f1c40f, #2ecc71, #3498db, #9b59b6)", "price": 200},
        "gradient": {"name": "Gradient", "color": "linear-gradient(180deg, #27ae60, #16a085)", "price": 200},
    }
    
    # Display skins in grid
    cols = st.columns(3)
    for idx, (skin_id, skin_data) in enumerate(skins.items()):
        with cols[idx % 3]:
            owned = skin_id in st.session_state.owned_skins
            
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 1rem;">
                <div style="background: {skin_data['color']}; width: 100px; height: 100px; margin: 0 auto 10px; border-radius: 10px; border: 3px solid white;"></div>
                <h3 style="color: white;">{skin_data['name']}</h3>
                <p style="color: white;">{"DEFAULT" if skin_data.get("default") else f"{skin_data['price']} 💰"}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if owned:
                st.success("✅ Owned")
            elif skin_data.get("default"):
                st.info("Default Skin")
            else:
                if st.button(f"Buy {skin_data['name']}", key=f"buy_{skin_id}", use_container_width=True):
                    if st.session_state.coins >= skin_data['price']:
                        st.session_state.coins -= skin_data['price']
                        st.session_state.owned_skins.append(skin_id)
                        st.success(f"Purchased {skin_data['name']}!")
                        st.rerun()
                    else:
                        st.error("Not enough coins!")
