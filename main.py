from database import init_db, get_crops_list

def main():
    # connecting to databse and initializing it if necessary
    init_db()

    print("=" * 45)
    print("  Подбор удобрений по анализу почвы (SQLite)")
    print("=" * 45)