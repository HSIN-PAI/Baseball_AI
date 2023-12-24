import csv
from bs4 import BeautifulSoup

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

def save_to_csv(data, csv_filename):
    if data:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # 寫入表頭
            writer.writeheader()

            # 寫入數據
            writer.writerows(data)

        print(f"數據已成功保存至 {csv_filename}")
    else:
        print("無法保存數據，請檢查是否成功解析。")

# 讀取 HTML 檔案
with open('data_input.xml', 'r', encoding='utf-8') as file:
    player_data_html = file.read()

# 解析球員數據
player_data = parse_player_data(player_data_html)

# 保存為 CSV 檔案
save_to_csv(player_data, 'player_data.csv')