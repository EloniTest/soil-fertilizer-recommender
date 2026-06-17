from database import init_db, get_crops_list
from calculations import calculate_recommendation

def main():
    init_db()

    print("==================================================")
    print("  ПОДБОР УДОБРЕНИЙ ПО РЕЗУЛЬТАТАМ АНАЛИЗА ПОЧВЫ   ")
    print("==================================================")

    # listing crops directly from SQLite
    crops = get_crops_list()
    for idx, (code, display_name) in enumerate(crops, start=1):
        print(f"  [{idx}] {display_name}")

    # we ask the user to select a crop and provide analysis data
    choice = int(input("\nВыберите номер культуры: ")) - 1
    crop_code, crop_display_name = crops[choice]

    print("\nВведите результаты лабораторного анализа почвы:")
    fact_n  = float(input("  Азот N (мг/кг): "))
    fact_p  = float(input("  Фосфор P2O5 (мг/кг): "))
    fact_k  = float(input("  Калий K2O (мг/кг): "))
    fact_ph = float(input("  Кислотность pH: "))

    # transfer data to the business logic calculation module
    report = calculate_recommendation(crop_code, fact_n, fact_p, fact_k, fact_ph)

    print(f"\n--- Рекомендации для культуры: {crop_display_name()} ---")
    
    n_min, n_max, p_min, p_max, k_min, k_max, ph_min, ph_max = report["norms"]
    print(f"Нормативы оптимума: N({n_min}-{n_max}), P({p_min}-{p_max}), K({k_min}-{k_max}), pH({ph_min}-{ph_max})\n")

    # total output of the report
    if not report["fertilizers"] and not report["lime"]:
        print(" [🎉] Почва в идеальном состоянии! Внесение удобрений не требуется.")
    else:
        for fert in report["fertilizers"]:
            print(f"• Элемент [{fert['element']}] -> {fert['status'].upper()}:")
            print(f"  Рекомендуется: {fert['fert_name']} — {fert['dose_phys']} кг/га")
            print(f"  Способ применения: {fert['method']} ({fert['notes']})\n")

        # Conclusion on deoxidation
        if report["lime"]:
            lime = report["lime"]
            print(f"⚠️ ТРЕБУЕТСЯ ХИМИЧЕСКАЯ МЕЛИОРАЦИЯ (pH {fact_ph} при норме от {ph_min}):")
            print(f"  Рекомендуется: {lime['name']} — {lime['dose']} т/га ({lime['method']})")

    print("==================================================")

if __name__ == "__main__":
    main()