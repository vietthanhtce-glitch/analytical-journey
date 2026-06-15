import streamlit as st
import google.generativeai as genai
import json
import re
import requests
from streamlit_lottie import st_lottie

# --- CÀI ĐẶT TRANG ---
st.set_page_config(page_title="The Analytical Journey", page_icon="🗡️", layout="centered")

# --- HÀM TẢI ẢNH ĐỘNG (LOTTIE) ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Link ảnh động (có thể thay thế bằng link khác từ lottiefiles.com)
lottie_wizard = load_lottieurl("https://lottie.host/80540450-48b4-4b11-a8ee-fdf4e9a1801c/S71N24QYpK.json")
lottie_castle = load_lottieurl("https://lottie.host/5b55de17-3843-42e6-a052-a5d625d3dfae/hBw1LCLrU0.json")

# --- SIDEBAR: NHẬP API KEY ---
with st.sidebar:
    st.header("⚙️ Cấu hình Game Master")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    if api_key:
        genai.configure(api_key=api_key)
        st.success("AI Connected Successfully!")

# --- KHỞI TẠO SESSION STATE ---
if 'stage' not in st.session_state:
    st.session_state.stage = 0
    st.session_state.topic = ""
    st.session_state.roles = {} # Lưu trữ vai diễn tự động
    st.session_state.micro_ans = ""
    st.session_state.micro_fb = ""
    st.session_state.meso_ans = ""
    st.session_state.meso_fb = ""
    st.session_state.macro_ans = ""
    st.session_state.macro_fb = ""

def reset_game():
    st.session_state.stage = 0
    st.session_state.topic = ""
    st.session_state.roles = {}
    for key in ['micro_ans', 'micro_fb', 'meso_ans', 'meso_fb', 'macro_ans', 'macro_fb']:
        st.session_state[key] = ""

# --- HÀM GỌI AI ---
def get_dynamic_roles(topic):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    You are the Game Master of an RPG for IELTS Writing Task 2 idea generation.
    The topic is: "{topic}"
    
    Create 3 RPG roles and 1 specific guiding question for each role to help the user brainstorm. The output MUST be in English and formatted EXACTLY as a JSON object.
    
    Roles:
    1. Micro: An individual directly affected (e.g., consumer, student).
    2. Meso: An organizational leader (e.g., school principal, CEO).
    3. Macro: A societal observer or policymaker (e.g., government minister, sociologist).
    
    JSON Format:
    {{
        "micro": {{"role": "[Role name]", "question": "[Specific question]"}},
        "meso": {{"role": "[Role name]", "question": "[Specific question]"}},
        "macro": {{"role": "[Role name]", "question": "[Specific question]"}}
    }}
    """
    response = model.generate_content(prompt)
    match = re.search(r'\{.*\}', response.text, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    return None

def get_ai_feedback(role, answer):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    You are an encouraging Game Master. The user just answered a question from the perspective of a {role}.
    Their answer: "{answer}"
    Provide a very short (2-3 sentences) encouraging feedback in English. Validate their idea, praise their critical thinking, and award them an imaginary item (e.g., 'Fragment of Empathy'). Keep it enthusiastic.
    """
    return model.generate_content(prompt).text

# --- GIAO DIỆN CHÍNH ---
st.title("🗡️ The Analytical Journey")
st.markdown("*An AI-Driven RPG for Idea Generation (IELTS Writing Task 2)*")
st.divider()

if not api_key:
    st.warning("⚠️ Vui lòng nhập API Key ở thanh bên trái để bắt đầu trò chơi.")
    st.stop()

# ==========================================
# TRẠM 0: NHẬP ĐỀ & TẠO VAI DIỄN (INIT)
# ==========================================
if st.session_state.stage == 0:
    st_lottie(lottie_wizard, height=200, key="wizard_init")
    st.info("👋 **[Game Master]:** Welcome traveler! Provide the magical scroll (IELTS Topic) you wish to decode.")
    topic_input = st.text_area("Enter IELTS Writing Task 2 Topic:", height=100)
    
    if st.button("🚀 Begin the Journey"):
        if topic_input:
            with st.spinner("Game Master is analyzing the realm and assigning your roles..."):
                roles = get_dynamic_roles(topic_input)
                if roles:
                    st.session_state.roles = roles
                    st.session_state.topic = topic_input
                    st.session_state.stage = 1
                    st.rerun()
                else:
                    st.error("Lỗi khi kết nối AI. Vui lòng thử lại!")
        else:
            st.warning("Bạn cần nhập đề bài!")

# ==========================================
# TRẠM 1: MICRO VILLAGE
# ==========================================
elif st.session_state.stage == 1:
    st.subheader("🏕️ Stage 1: The Micro Village")
    st.caption(f"**Topic:** {st.session_state.topic}")
    
    role = st.session_state.roles['micro']['role']
    question = st.session_state.roles['micro']['question']
    
    st.success(f"**[Game Master]:** You have transformed into a **{role}**.\n\n*\"{question}\"*")
    
    ans = st.text_area("Play your role and answer (in English):", height=150)
    
    if st.button("Submit & Listen to Game Master"):
        if ans:
            with st.spinner("Game Master is reading your mind..."):
                st.session_state.micro_ans = ans
                st.session_state.micro_fb = get_ai_feedback(role, ans)
                st.session_state.stage = 1.5
                st.rerun()

elif st.session_state.stage == 1.5:
    st.subheader("🏕️ Stage 1: The Micro Village")
    st.info(f"**[Game Master]:** {st.session_state.micro_fb}")
    if st.button("Proceed to The Meso Guild ➡️"):
        st.session_state.stage = 2
        st.rerun()

# ==========================================
# TRẠM 2: MESO GUILD
# ==========================================
elif st.session_state.stage == 2:
    st.subheader("🏛️ Stage 2: The Meso Guild")
    st.caption(f"**Topic:** {st.session_state.topic}")
    
    role = st.session_state.roles['meso']['role']
    question = st.session_state.roles['meso']['question']
    
    st.success(f"**[Game Master]:** You have leveled up to a **{role}**.\n\n*\"{question}\"*")
    
    ans = st.text_area("Play your role and answer (in English):", height=150)
    
    if st.button("Submit & Listen to Game Master"):
        if ans:
            with st.spinner("Game Master is analyzing your strategy..."):
                st.session_state.meso_ans = ans
                st.session_state.meso_fb = get_ai_feedback(role, ans)
                st.session_state.stage = 2.5
                st.rerun()

elif st.session_state.stage == 2.5:
    st.subheader("🏛️ Stage 2: The Meso Guild")
    st.info(f"**[Game Master]:** {st.session_state.meso_fb}")
    if st.button("Proceed to The Macro Kingdom ➡️"):
        st.session_state.stage = 3
        st.rerun()

# ==========================================
# TRẠM 3: MACRO KINGDOM
# ==========================================
elif st.session_state.stage == 3:
    st.subheader("🏰 Stage 3: The Macro Kingdom")
    st.caption(f"**Topic:** {st.session_state.topic}")
    
    role = st.session_state.roles['macro']['role']
    question = st.session_state.roles['macro']['question']
    
    st.success(f"**[Game Master]:** Welcome to the throne room. You are now a **{role}**.\n\n*\"{question}\"*")
    
    ans = st.text_area("Play your role and answer (in English):", height=150)
    
    if st.button("Submit & Listen to Game Master"):
        if ans:
            with st.spinner("Game Master is pondering your global vision..."):
                st.session_state.macro_ans = ans
                st.session_state.macro_fb = get_ai_feedback(role, ans)
                st.session_state.stage = 3.5
                st.rerun()

elif st.session_state.stage == 3.5:
    st.subheader("🏰 Stage 3: The Macro Kingdom")
    st.info(f"**[Game Master]:** {st.session_state.macro_fb}")
    if st.button("Unlock The Treasure Board 💎"):
        st.session_state.stage = 4
        st.rerun()

# ==========================================
# ĐÍCH ĐẾN: THE TREASURE BOARD
# ==========================================
elif st.session_state.stage == 4:
    st.balloons()
    st_lottie(lottie_castle, height=250, key="castle_end")
    st.header("💎 The Treasure Board")
    
    st.info("Game Master is forging your fragments into a master outline...")
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    You are the Game Master. The user has completed the RPG for this IELTS topic: "{st.session_state.topic}"
    
    Their insights:
    1. Micro ({st.session_state.roles['micro']['role']}): {st.session_state.micro_ans}
    2. Meso ({st.session_state.roles['meso']['role']}): {st.session_state.meso_ans}
    3. Macro ({st.session_state.roles['macro']['role']}): {st.session_state.macro_ans}
    
    Task:
    Synthesize these into a highly logical, detailed IELTS Essay Outline in English. 
    Include advanced vocabulary (Lexical Resource) suggestions based on their input.
    """
    
    try:
        with st.spinner('Forging outline...'):
            response = model.generate_content(prompt)
        st.write(response.text)
    except Exception as e:
        st.error(f"Error calling AI: {e}")

    st.divider()
    if st.button("🔄 Start a New Journey"):
        reset_game()
        st.rerun()
