# 🎓 HCMUT RAG Chatbot

Chatbot hỏi đáp thông tin về **Trường Đại học Bách khoa - Đại học Quốc gia TP.HCM (HCMUT)** sử dụng kiến trúc **Retrieval-Augmented Generation (RAG)**.

Hệ thống cho phép người dùng đặt câu hỏi về:

* Tuyển sinh
* Ngành học
* Học phí
* Thông tin chung về trường
* Cơ sở vật chất và hoạt động sinh viên

Chatbot sử dụng **Vector Search + LLM** để tìm tài liệu liên quan và tạo câu trả lời chính xác.

---

# 🧠 Kiến trúc hệ thống

Pipeline của hệ thống:

User Question
↓
Rewrite Query (LLM)
↓
Embedding (Sentence Transformers)
↓
Vector Search (Cosine Similarity)
↓
Retrieve Top-k Documents
↓
RAG Prompt
↓
Gemma LLM
↓
Final Answer

Công nghệ chính:

* RAG (Retrieval-Augmented Generation)
* Sentence Transformers
* Vector Similarity Search
* Google Gemma LLM
* Streamlit UI

---

# 📂 Cấu trúc thư mục

```
CHATBOT RAG
│
├── main.py                # Logic chính của chatbot + RAG pipeline
├── ui.py                  # Giao diện chatbot bằng Streamlit
├── requirement.txt        # Thư viện cần cài
│
├── Chunk/                 # Xử lý chia nhỏ dữ liệu
│   └── chunkingData.py
│
├── Retrieve/              # Truy xuất dữ liệu từ Vector DB
│   └── retriever.py
│
├── VectorDatabase/        # Lưu embeddings
│   ├── vectorDB.py
│   ├── embeddings.npy
│   └── texts.npy
│
├── Data/                  # Dữ liệu đã xử lý
│   ├── data-cleaned.jsonl
│   ├── hcmut_data.txt
│   └── hcmut_info.txt
│
├── RawData/               # Dữ liệu gốc và script crawl
│   ├── crawlData.py
│   └── xlsvtojson.py
│
└── venv/                  # Python virtual environment
```

---

# ⚙️ Cài đặt

### 1️⃣ Clone project

```bash
git clone <repo-url>
cd chatbot-rag
```

### 2️⃣ Tạo virtual environment

```bash
python -m venv venv
```

Activate:

Windows

```
venv\Scripts\activate
```

Linux / Mac

```
source venv/bin/activate
```

### 3️⃣ Cài thư viện

```bash
pip install -r requirement.txt
```

---
## 🔑 Thiết lập API Key

Dự án này sử dụng **Google Generative AI (Gemma/Gemini)** nên cần API key để chạy.

Vì lý do bảo mật, **API key không được đưa trực tiếp vào repository**.

### 1. Tạo file `.env`

### 2. Thêm API key vào `.env`

Mở file `.env` và thêm API key của bạn:

```
GEMINI_API_KEY=your_api_key_here
```

# 🗄️ Tạo Vector Database

Trước khi chạy chatbot cần tạo embeddings cho dữ liệu:

```bash
python VectorDatabase/vectorDB.py
```

File sau sẽ được tạo:

```
VectorDatabase/
├── embeddings.npy
└── texts.npy
```

---

# 🚀 Chạy Chatbot

Chạy giao diện Streamlit:

```bash
streamlit run ui.py
```

Sau đó mở trình duyệt tại:

```
http://localhost:8501
```

---

# 💬 Ví dụ câu hỏi

Bạn có thể hỏi chatbot:

* Trường Đại học Bách khoa TP.HCM có bao nhiêu cơ sở?
* Trường có những ngành đào tạo nào?
* Học phí của trường là bao nhiêu?
* Địa chỉ của trường ở đâu?

---

# 🛠️ Công nghệ sử dụng

* Python
* Streamlit
* Sentence Transformers
* Scikit-learn
* LangChain
* Google Generative AI
* HuggingFace Transformers

---

# 📌 Ghi chú

Chatbot chỉ trả lời các câu hỏi liên quan đến **Trường Đại học Bách khoa TP.HCM**.
Nếu câu hỏi ngoài phạm vi, hệ thống sẽ từ chối trả lời.

---

# 👨‍💻 Tác giả

Sinh viên thực hiện dự án **RAG Chatbot tư vấn HCMUT** phục vụ mục đích học tập và nghiên cứu AI / NLP.
