import csv
from bs4 import BeautifulSoup
from tkinter import Tk, filedialog

def open_file_dialog():
    root = Tk()
    root.withdraw()  # 隱藏主視窗
    file_path = filedialog.askopenfilename(title="選擇檔案")
    return file_path

def parse_player_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # 找到包含球員數據的區塊
    player_data_block = soup.find('tbody', {'role': 'rowgroup'})

    # 提取數據
    if player_data_block:
        rows = player_data_block.find_all('tr')

        # 解析表頭
        header_row = rows[0]
        headers = [header.text.strip() for header in header_row.find_all('th')]

        # 解析每一行的數據
        data = []
        for row in rows[1:]:
            columns = [column.text.strip() for column in row.find_all('td')]
            player_info = dict(zip(headers, columns))
            data.append(player_info)

        return data
    else:
        print("找不到球員數據區塊。")
        return None

def save_to_csv(data):
    if data:
        root = Tk()
        root.withdraw()  # 隱藏主視窗
        file_path = filedialog.asksaveasfilename(title="儲存檔案",filetypes=[("CSV 檔案", "*.csv"), ("所有檔案", "*.*")])
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # 寫入表頭
            writer.writeheader()
            # 寫入數據
            writer.writerows(data)

        print(f"數據已成功保存至 {file_path}")
    else:
        print("無法保存數據，請檢查是否成功解析。")

# 讀取 HTML 檔案
selected_file = open_file_dialog()
with open(selected_file, 'r', encoding='utf-8') as file:
    player_data_html = file.read()

# 解析球員數據
player_data = parse_player_data(player_data_html)

# 保存為 CSV 檔案
save_to_csv(player_data)