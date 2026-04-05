import os
import asyncio
from crawl4ai import AsyncWebCrawler

# Danh sách URL HCMUT (có thể thêm nhiều trang)
URLS = [
    "https://hcmut.edu.vn/thong-diep-cua-hieu-truong",
    "https://hcmut.edu.vn/gioi-thieu/ke-hoach-chien-luoc",
    "https://hcmut.edu.vn/tong-quan"
    "https://hcmut.edu.vn/gioi-thieu/xep-hang-dai-hoc",
    "https://hcmut.edu.vn/tuyen-sinh-dh/dai-hoc-chinh-quy",
    "https://hcmut.edu.vn/co-cau-to-chuc"

    ""
]

OUTPUT_FILE = "Data/hcmut_crawl4ai.txt"

async def crawl_hcmut():
    # Tạo thư mục nếu chưa có
    os.makedirs("Data", exist_ok=True)

    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(urls=URLS)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            for result in results:
                f.write(f"===== URL: {result.url} =====\n")
                f.write(result.markdown)  # nội dung sạch
                f.write("\n\n")

    print(f"✅ Đã lưu dữ liệu vào {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(crawl_hcmut())
