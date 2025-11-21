"""
My Skins Page - Select Active Skin
"""

import streamlit as st

def run():
    """My Skins page for selecting active skin"""
    
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
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 style="text-align: center; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">🎨 My Skins</h1>', unsafe_allow_html=True)
    
    st.markdown(f'<div style="text-align: center; color: white; font-size: 1.5rem; margin: 2rem;">Current Active Skin: {st.session_state.active_skin.title()}</div>', unsafe_allow_html=True)
    
    # Skin details
    skins = {
        "green": {"name": "Green", "color": "#27ae60"},
        "red": {"name": "Red", "color": "#e74c3c"},
        "blue": {"name": "Blue", "color": "#3498db"},
        "yellow": {"name": "Yellow", "color": "#f1c40f"},
        "rainbow": {"name": "Rainbow", "color": "linear-gradient(90deg, #e74c3c, #f39c12, #f1c40f, #2ecc71, #3498db, #9b59b6)"},
        "gradient": {"name": "Gradient", "color": "linear-gradient(180deg, #27ae60, #16a085)"},
    }
    
    st.write("")
    st.markdown('<div style="text-align: center; color: white; margin-bottom: 2rem;">Select a skin to use in Snake and Flappy Bird:</div>', unsafe_allow_html=True)
    
    # Display owned skins
    cols = st.columns(3)
    idx = 0
    for skin_id in st.session_state.owned_skins:
        if skin_id in skins:
            with cols[idx % 3]:
                skin_data = skins[skin_id]
                is_active = skin_id == st.session_state.active_skin
                
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 1rem; border: {'3px solid gold' if is_active else '2px solid white'};">
                    <div style="background: {skin_data['color']}; width: 100px; height: 100px; margin: 0 auto 10px; border-radius: 10px; border: 3px solid white;"></div>
                    <h3 style="color: white;">{skin_data['name']}</h3>
                    {'<p style="color: gold; font-weight: bold;">✨ ACTIVE ✨</p>' if is_active else ''}
                </div>
                """, unsafe_allow_html=True)
                
                if not is_active:
                    if st.button(f"Use {skin_data['name']}", key=f"use_{skin_id}", use_container_width=True, type="primary"):
                        st.session_state.active_skin = skin_id
                        st.success(f"Activated {skin_data['name']}!")
                        st.rerun()
                else:
                    st.info("Currently Active")
                
                idx += 1
    
    if len(st.session_state.owned_skins) == 1:
        st.write("")
        st.info("🛒 Visit the Store to buy more skins!")
