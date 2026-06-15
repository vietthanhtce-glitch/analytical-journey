import streamlit as st
import google.generativeai as genai

# --- CÀI ĐẶT TRANG ---
st.set_page_config(page_title="The Analytical Journey", page_icon="🗡️", layout="centered")

# --- SIDEBAR: NHẬP API KEY ---
with st.sidebar:
    st.header("⚙️ Cấu hình Game Master (AI)")
    api_key = st.text_input("Nhập Gemini API Key của bạn vào đây:", type="password")
    st.markdown("*Lấy API key miễn phí tại [Google AI Studio](https://aistudio.google.com/)*")
    if api_key:
        genai.configure(api_key=api_key)
        st.success("Đã kết nối AI thành công!")

# --- KHỞI TẠO SESSION STATE ---
if 'stage' not in st.session_state:
    st.session_state.stage = 0
    st.session_state.topic = ""
    st.session_state.micro_ans = ""
    st.session_state.meso_ans = ""
    st.session_state.macro_ans = ""

def reset_game():
    st.session_state.stage = 0
    st.session_state.topic = ""
    st.session_state.micro_ans = ""
    st.session_state.meso_ans = ""
    st.session_state.macro_ans = ""

# --- GIAO DIỆN CHÍNH ---
st.title("🗡️ The Analytical Journey")
st.markdown("*An AI-Driven RPG for Idea Generation (IELTS Writing Task 2)*")
st.divider()

# ==========================================
# TRẠM 0, 1, 2, 3: (Giữ nguyên logic như cũ)
# ==========================================
if st.session_state.stage == 0:
    st.info("👋 Chào mừng lữ khách! Hãy cung cấp cuộn giấy phép thuật (Đề bài IELTS) mà bạn muốn giải mã.")
    topic_input = st.text_area("Nhập đề bài IELTS Writing Task 2:", height=100)
    if st.button("🚀 Bắt đầu Hành trình"):
        if topic_input:
            st.session_state.topic = topic_input
            st.session_state.stage = 1
            st.rerun()
        else:
            st.warning("Bạn cần nhập đề bài để bắt đầu!")

elif st.session_state.stage == 1:
    st.subheader("🏕️ Trạm 1: The Micro Village")
    st.write(f"**Đề bài:** *{st.session_state.topic}*")
    st.success("**[Game Master]:** Chào lữ khách! Xuyên không thành một công dân bình thường (người dùng, học sinh...). Điều gì đang xảy ra với cá nhân bạn? Bạn được gì, mất gì?")
    micro = st.text_area("Nhập vai và trả lời:", height=150)
    if st.button("🧩 Nhận 'Mảnh ghép Tâm lý'"):
        if micro:
            st.session_state.micro_ans = micro
            st.session_state.stage = 2
            st.rerun()

elif st.session_state.stage == 2:
    st.subheader("🏛️ Trạm 2: The Meso Guild")
    st.write(f"**Đề bài:** *{st.session_state.topic}*")
    st.success("**[Game Master]:** Bạn đã thăng cấp thành Trưởng hội! Tổ chức/Doanh nghiệp của bạn cung cấp giải pháp gì, đối mặt thách thức nào và kiếm lợi ra sao từ việc này?")
    meso = st.text_area("Nhập vai và trả lời:", height=150)
    if st.button("⚙️ Nhận 'Mảnh ghép Vận hành'"):
        if meso:
            st.session_state.meso_ans = meso
            st.session_state.stage = 3
            st.rerun()

elif st.session_state.stage == 3:
    st.subheader("🏰 Trạm 3: The Macro Kingdom")
    st.write(f"**Đề bài:** *{st.session_state.topic}*")
    st.success("**[Game Master]:** Thưa Bộ trưởng, ngài nhìn nhận sự việc này ảnh hưởng thế nào đến toàn vương quốc (kinh tế, môi trường, chính sách)?")
    macro = st.text_area("Nhập vai và trả lời:", height=150)
    if st.button("👑 Nhận 'Mảnh ghép Chính sách'"):
        if macro:
            st.session_state.macro_ans = macro
            st.session_state.stage = 4
            st.rerun()

# ==========================================
# ĐÍCH ĐẾN: THE TREASURE BOARD (TÍCH HỢP AI)
# ==========================================
elif st.session_state.stage == 4:
    st.balloons()
    st.header("💎 The Treasure Board")
    
    if not api_key:
        st.error("⚠️ Bạn cần nhập Gemini API Key ở thanh bên trái (Sidebar) để Game Master có thể rèn đúc Dàn ý!")
        if st.button("🔄 Bắt đầu lại"):
            reset_game()
            st.rerun()
    else:
        st.info("Game Master đang dùng phép thuật AI để tổng hợp các mảnh ghép của bạn...")
        
        # Gọi Gemini AI
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"""
            Bạn là Game Master của một trò chơi nhập vai tạo dàn ý IELTS. 
            Đề bài IELTS Writing Task 2 là: "{st.session_state.topic}"
            
            Người chơi đã đi qua 3 trạm và thu thập được các insight sau:
            1. Góc độ Vi mô (Cá nhân): {st.session_state.micro_ans}
            2. Góc độ Trung mô (Tổ chức/Doanh nghiệp): {st.session_state.meso_ans}
            3. Góc độ Vĩ mô (Chính phủ/Xã hội): {st.session_state.macro_ans}
            
            Nhiệm vụ của bạn:
            1. Mở đầu bằng một câu chúc mừng người chơi bằng giọng điệu hào hùng của Game Master.
            2. Tổng hợp 3 ý tưởng trên thành một Dàn ý (Outline) chi tiết và logic cho bài IELTS Essay. 
            3. Giữ nguyên cốt lõi ý tưởng của người chơi nhưng nâng cấp từ vựng học thuật (cung cấp kèm một số cụm từ vựng - lexical resource gợi ý).
            4. Trình bày rõ ràng bằng tiếng Việt, đan xen tiếng Anh cho các thuật ngữ IELTS.
            """
            
            with st.spinner('Đang rèn đúc vũ khí...'):
                response = model.generate_content(prompt)
                
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Có lỗi xảy ra khi gọi AI: {e}")

        st.divider()
        if st.button("🔄 Bắt đầu Hành trình Mới"):
            reset_game()
            st.rerun()
