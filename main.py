import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


from Retrieve.retriever import hybrid_search, retrieve
import google.generativeai as genai

import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)


model = genai.GenerativeModel("gemma-3-27b-it")

history = []
def build_retrieval_query(question, history):
    """
    Tạo query tốt hơn để truy xuất RAG

    question: câu hỏi hiện tại của user
    history: list chat history
    model_call: hàm gọi LLM
    """

    # lấy 4 message gần nhất
    history_text = ""
    for msg in history[-4:]:
        role = msg["role"]
        content = msg["content"]
        history_text += f"{role}: {content}\n"

    prompt = f"""
Bạn là hệ thống tạo câu hỏi tìm kiếm tài liệu.

Dựa vào lịch sử hội thoại và câu hỏi hiện tại,
hãy viết lại câu hỏi sao cho đầy đủ ngữ cảnh
để truy xuất tài liệu về Đại học Bách khoa TP.HCM. 

Chỉ trả về 1 câu hỏi duy nhất, mà không thay đổi ý nghĩa chính của câu hỏi.

History:
{history_text}

User question:
{question}

Search query:
"""

    query = model.generate_content(prompt)
    print(query.text)
    return query.text

def build_rag_query(question: str, contexts: list, history):

    context_text = "\n".join(contexts)
    history_text = ""

    for msg in history:
        if msg["role"] == "user":
            history_text += f"User: {msg['content']}\n"
        else:
            history_text += f"Assistant: {msg['content']}\n"

    prompt = f"""
Bạn là chatbot tư vấn dành riêng cho Trường Đại học Bách khoa Đại học Quốc gia TP.HCM.

Nhiệm vụ của bạn:
- Chỉ trả lời các câu hỏi liên quan đến Trường Đại học Bách khoa TP.HCM.
- Các chủ đề bao gồm: tuyển sinh, ngành học, học phí, chương trình đào tạo, địa chỉ, cơ sở vật chất và hoạt động sinh viên.

Quy tắc:
1. Chỉ sử dụng thông tin trong phần Context để trả lời.
2. Nếu câu hỏi không liên quan đến Trường Đại học Bách khoa TP.HCM, hãy trả lời:
   "Xin lỗi, tôi chỉ hỗ trợ thông tin về Trường Đại học Bách khoa TP.HCM."
3. Nếu Context không chứa thông tin cần thiết, hãy trả lời:
   "Xin lỗi, tôi chưa có thông tin về vấn đề này."
4. Trả lời ngắn gọn, rõ ràng và thân thiện.
5. Đọc lại lịch sử hội thoại trước khi trả lời để bổ sung ngữ cảnh

Lịch sử hội thoại:
{history_text}
Context:
{context_text}

Câu hỏi của người dùng:
{question}

Trả lời:
"""
    print(history_text)
    return prompt


def ask_model(question):
    query = build_retrieval_query(question, history)
    context = hybrid_search(query, question)
    prompt = build_rag_query(question, context, history)
    response = model.generate_content(prompt)
    history.append({"role":"user","content":question})
    history.append({"role":"assistant","content":response.text})
    for text in context: 
        print(text)
    return response.text

if __name__ == "__main__":

    question = "bộ nhận diện thương hiệu của trường"
    model_id = "google/gemma-3-27b-it"

    print(ask_model(question))

