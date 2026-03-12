import random

# 定義一些隨機零件名稱和廠商，讓資料看起來真實
names = ["螺絲", "螺帽", "齒輪", "軸承", "墊片", "彈簧", "感測器", "馬達", "皮帶", "接頭"]
specs = ["M3", "M5", "10mm", "20mm", "V1", "V2", "Type-A", "Type-B"]
vendors = ["金豐工業", "台積電", "聯電", "鴻海", "大立光", "捷安特", "漢翔", "上銀科技"]

print("正在產生10筆資料...")

with open('parts.txt', 'w', encoding='utf-8') as f:
    # 寫入標題列
    f.write("barcode,name,spec,vendor,stock,price\n")

    for i in range(1, 11):
        barcode = f"A{i:05d}"  # 產生 A00001 ~ A10000
        name = random.choice(names)
        spec = random.choice(specs)
        vendor = random.choice(vendors)
        stock = random.randint(0, 500)
        price = random.randint(10, 2000)

        # 寫入一行資料
        f.write(f"{barcode},{name},{spec},{vendor},{stock},{price}\n")

print("✅ 成功！parts.txt 已產生10筆資料。")