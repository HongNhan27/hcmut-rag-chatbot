# crawler.py
import requests
from bs4 import BeautifulSoup
import re

def clean_text(text: str) -> str:
    """Làm sạch text: bỏ khoảng trắng thừa, ký tự lạ."""
    text = re.sub(r'\n{3,}', '\n\n', text)   # Gộp nhiều dòng trống
    text = re.sub(r'[ \t]+', ' ', text)        # Gộp khoảng trắng
    return text.strip()

def crawl_single_page(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; RAGBot/1.0)"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    # Loại bỏ các thẻ không cần thiết
    for tag in soup(["script", "style", "nav", "footer", "header", "ads"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    return clean_text(text)

# Sử dụng
url = "https://hcmut.edu.vn/tong-quan"
content = crawl_single_page(url)

with open("../Data/hcmut_data.txt", "w", encoding="utf-8") as f:
    f.write(f"SOURCE: {url}\n")
    f.write("=" * 60 + "\n\n")
    f.write(content)

print(f"✅ Đã lưu: output/page.txt ({len(content)} ký tự)")