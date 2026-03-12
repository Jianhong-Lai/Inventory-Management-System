import csv
# --- 0. 工具箱：廠商索引建立器 ---
def build_vendor_index(data):
    """
    這個函式就像是『分類秘書』。
    輸入：原始零件大字典 (data)
    輸出：分類好的廠商目錄 (temp_index)
    """
    temp_index = {}
    for barcode_f, info_f in data.items():
        v = info_f.get("供應商", "未知")
        if v not in temp_index:
            temp_index[v] = []
        # 把名稱丟進去該廠商的分類夾
        temp_index[v].append(info_f.get("名稱", "未知"))
    return temp_index
inventory = {}

try:
    with open('parts.txt', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            bc = row['barcode']
            # 直接以條碼為 Key，餵入所有的資訊
            row_stock = row.get("stock", "")
            row_price = row.get("price", "")
            inventory[bc] = {
                "名稱": row.get("name", "未知"),
                "規格": row.get("spec", "無規格"),
                "供應商": row.get("vendor", "未知"),
                "庫存": int(row_stock) if row_stock.isdigit() else 0, # 記得轉成整數才能計算
                "單價": int(row_price) if row_price.isdigit() else 0  # 記得轉成整數
            }
    print("✅ CSV 資料載入成功！")
except FileNotFoundError:
    print("❌ 找不到 parts.csv 檔案，請確認檔案在同一資料夾。")

global_vendor_map = build_vendor_index(inventory)

print("=== 🏗️ 金豐機器工業 - 數位化庫存系統啟動 ===")

while True:
    print("\n" + "=" * 45)
    print("1. 列出所有零件  2. 條碼查貨  3. 廠商反向搜尋  4. 存檔並離開")
    print("=" * 45)

    choice = input("請選擇功能：")

    # --- 功能 1：列出所有零件 (展現排版與雙層 Dict 讀取) ---
    if choice == "1":
        print("\n[ 目前總庫存報表 ]")
        for barcode, info in inventory.items():
            # 使用 .get() 確保即使欄位缺失也不會崩潰
            name = info.get("名稱", "未知")
            spec = info.get("規格", "無規格")
            vendor = info.get("供應商", "無供應商")
            stock = info.get("庫存", 0)
            price = info.get("單價", 0)
            print(f"條碼: {barcode} | 名稱: {name} ({spec}) | 供應商: {vendor} | 庫存: {stock} | 單價: {price}")

    # --- 功能 2：條碼查貨與銷售 (展現防呆與庫存邏輯) ---
    elif choice == "2":
        barcode = input("請輸入產品條碼：")
        item = inventory.get(barcode)

        if item:
            print(f"✅ 找到：{item['名稱']} (供應商：{item['供應商']})")
            sell_num = input("請輸入銷售數量：")
            if sell_num.isdigit():
                num = int(sell_num)
                if item['庫存'] >= num:
                    item['庫存'] -= num
                    print(f"💰 銷售成功！剩餘庫存：{item['庫存']}")
                else:
                    print("❌ 庫存不足！")
        else:
            print("⚠️ 查無此條碼。")

    # --- 功能 3：廠商反向搜尋 (展現自動化索引邏輯) ---
    elif choice == "3":
        # 【核心邏輯】自動生成反向索引表


        target_vendor = input("請輸入要查詢的供應商名稱：")
        found_parts = global_vendor_map.get(target_vendor)

        if found_parts:
            print(f"📍 {target_vendor} 提供的零件有：{', '.join(found_parts)}")
        else:
            print("⚠️ 找不到該供應商的資料。")

    elif choice == "4":

        print("💾 正在安全存檔...")

        try:

            with open('parts.txt', mode='w', encoding='utf-8', newline='') as f:

                # 1. 定義標題順序 (重要：必須跟讀取時的 key 一致)

                fieldnames = ['barcode', 'name', 'spec', 'vendor', 'stock', 'price']

                writer = csv.DictWriter(f, fieldnames=fieldnames)

                # 2. 寫入標題 (barcode,name...)

                writer.writeheader()

                # 3. 把 inventory 裡的中文 key 轉回英文欄位寫入

                for bc, info in inventory.items():
                    writer.writerow({

                        'barcode': bc,

                        'name': info.get("名稱"),

                        'spec': info.get("規格"),

                        'vendor': info.get("供應商"),

                        'stock': info.get("庫存"),

                        'price': info.get("單價")

                    })

            print("✅ 存檔成功！庫存已同步至 parts.txt")

        except Exception as e:

            print(f"❌ 存檔失敗：{e}")

        print("系統登出，資料已安全存檔。")

        break