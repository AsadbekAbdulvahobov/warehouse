import json
import os
from datetime import datetime

# Fayl nomlari
WAREHOUSE_FILE = 'warehouse.json'
REPORT_FILE = 'monthly_report.json'
TOTAL_TAKEN_FILE = 'total_taken.json'

# JSON fayldan ma'lumotlarni yuklash
def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return {}

# JSON faylga ma'lumotlarni yozish
def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

# Ombor, hisobot va jami ma'lumotlar
warehouse = load_data(WAREHOUSE_FILE)
report = load_data(REPORT_FILE)
total_taken = load_data(TOTAL_TAKEN_FILE)

def show_menu():
    print("\n=== Ombor boshqaruvi tizimi ===")
    print("1. Mahsulot qo'shish")
    print("2. Mahsulot tahrirlash (ombordan chiqarish)")
    print("3. Kam qolgan yoki ko'p mahsulotlarni ko'rish")
    print("4. Ombordagi barcha mahsulotlarni ko'rish")
    print("5. Hisobotlarni ko'rish")
    print("6. Chiqish")

def add_item():
    item = input("Mahsulot nomini kiriting: ")
    quantity = int(input("Miqdorini kiriting: "))

    # Ombor ma'lumotlarini yangilash
    warehouse[item] = warehouse.get(item, 0) + quantity
    save_data(WAREHOUSE_FILE, warehouse)

    print(f"'{item}' mahsuloti {quantity} miqdorda qo'shildi.")

def edit_item():
    item = input("Tahrirlash uchun mahsulot nomini kiriting: ")
    if item not in warehouse:
        print(f"Mahsulot '{item}' omborda topilmadi.")
        return

    old_quantity = warehouse[item]
    print(f"Hozirgi miqdor: {old_quantity}")
    new_quantity = int(input("Qancha miqdorda chiqarishni xohlaysiz: "))

    if new_quantity > old_quantity:
        print(f"Xatolik: Omborda '{item}' mahsulotdan buncha miqdor mavjud emas!")
        return

    # Omborda mahsulotni yangilash
    warehouse[item] = old_quantity - new_quantity
    save_data(WAREHOUSE_FILE, warehouse)

    # Hisobotga yozish
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if item not in report:
        report[item] = []
    report[item].append({'date': timestamp, 'quantity_removed': new_quantity})
    save_data(REPORT_FILE, report)

    # Jami olingan mahsulotlarni yangilash
    if item not in total_taken:
        total_taken[item] = new_quantity
    else:
        total_taken[item] += new_quantity
    save_data(TOTAL_TAKEN_FILE, total_taken)

    print(f"'{item}' mahsulotidan {new_quantity} miqdor chiqarildi.")

def filter_products():
    filter_type = input("Kam qolgan mahsulotlarni ko'rish uchun 'low', ko'p mahsulotlarni ko'rish uchun 'high' yozing: ")

    if filter_type == 'low': # kam mahsulotlarni chiqarish
        low_stock = {item: quantity for item, quantity in warehouse.items() if quantity < 50}
        if low_stock:
            print("\nKam qolgan mahsulotlar:")
            for item, quantity in low_stock.items():
                print(f"{item}: {quantity}")
        else:
            print("Kam mahsulot topilmadi.")

    elif filter_type == 'high': # ko'p mahsulotlarni chiqarish
        high_stock = {item: quantity for item, quantity in warehouse.items() if quantity > 500}
        if high_stock:
            print("\nKo'p mahsulotlar:")
            for item, quantity in high_stock.items():
                print(f"{item}: {quantity}")

        else:
            print("Ko'p mahsulot topilmadi.")
    else:
        print("Noto'g'ri buyruq kiritildi.")

def view_warehouse():
    if warehouse:
        print("\nOmbordagi mahsulotlar:")
        for item, quantity in warehouse.items():
            print(f"{item}: {quantity}")
    else:
        print("Ombor bo'sh.")

def view_reports():
    print("\n=== Hisobotlar ===")
    print("1. Oylik hisobot")
    print("2. Jami olingan mahsulotlar")
    choice = input("Tanlang: ")

    if choice == '1':
        if report:
            print("\nOylik hisobot:")
            for item, logs in report.items():
                print(f"{item}:")
                for log in logs:
                    print(f"  Sana: {log['date']}, Miqdor: {log['quantity_removed']}")
        else:
            print("Hisobot bo'sh.")

    elif choice == '2':
        if total_taken:
            print("\nJami olingan mahsulotlar:")
            for item, total in total_taken.items():
                print(f"{item}: {total}")
        else:
            print("Ma'lumot mavjud emas.")
    else:
        print("Noto'g'ri tanlov.")

if __name__ == '__main__':
    while True:
        show_menu()
        choice = input("Tanlovingizni kiriting: ")

        if choice == '1':
            add_item()
        elif choice == '2':
            edit_item()
        elif choice == '3':
            filter_products()
        elif choice == '4':
            view_warehouse()
        elif choice == '5':
            view_reports()
        elif choice == '6':
            print("Tizimdan chiqildi.")
            break
        else:
            print("Noto'g'ri tanlov. Qayta urinib ko'ring.")
