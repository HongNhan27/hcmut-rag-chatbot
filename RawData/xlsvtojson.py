import pandas as pd
import json

file_path = 'RawData\data cho box thông tin trường-completed.xlsx'
df = pd.read_excel(file_path)

data = df.to_dict(orient='records')

with open('Data\data-cleaned.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Đã chuyển đổi thành công sang file data_chatbot.json!")


