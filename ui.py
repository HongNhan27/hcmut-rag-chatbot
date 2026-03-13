import streamlit as st
from main import ask_model   # hàm trả lời chatbot của bạn

st.set_page_config(
    page_title="Chatbot Bách Khoa",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Chatbot tư vấn Đại học Bách khoa TP.HCM")

st.markdown(
"""
Chatbot hỗ trợ trả lời các câu hỏi về:

- Tuyển sinh
- Ngành học
- Học phí
- Thông tin trường
"""
)

# lưu lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ô nhập câu hỏi
user_input = st.chat_input("Nhập câu hỏi của bạn...")

if user_input:

    # hiển thị user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # gọi chatbot
    with st.chat_message("assistant"):
        with st.spinner("Đang tìm câu trả lời..."):

            answer = ask_model(user_input)

            st.write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
