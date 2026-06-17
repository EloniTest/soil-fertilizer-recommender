from database import init_db, get_crops_list
from calculations import calculate_recommendations, save_report_to_file


def main():
    # connecting to databse and initializing it if necessary
    init_db()

    print("==================================================")
    print("  ПОДБОР УДОБРЕНИЙ ПО РЕЗУЛЬТАТАМ АНАЛИЗА ПОЧВЫ   ")
    print("==================================================")

    crops = get_crops_list()
    for idx, (code, display_name) in enumerate(crops, start=1):
        print(f"  [{idx}] {display_name}")

    choice = int(input("\nВыберите номер культуры: ")) - 1
    crop_code, crop_display_name = crops[choice]

    print("\nВведите результаты лабораторного анализа почвы:")
    fact_n  = float(input("  Азот N (мг/кг): "))
    fact_p  = float(input("  Фосфор P2O5 (мг/кг): "))
    fact_k  = float(input("  Калий K2O (мг/кг): "))
    fact_ph = float(input("  Кислотность pH: "))