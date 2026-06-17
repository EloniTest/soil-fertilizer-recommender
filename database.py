import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(__file__), "agrochem.db")

def get_Connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    # Creating tables and filling directories if there is no database
    conn = get_Connection()
    sql = conn.cursor()

    # creating table (crops)
    sql.execute("""CREATE TABLE IF NOT EXISTS crops (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT UNIQUE, 
        display_name TEXT)""")
    # creating table (crop norms)
    sql.execute("""CREATE TABLE IF NOT EXISTS crop_norms (
        crop_name TEXT PRIMARY KEY REFERENCES crops(name),
        n_min REAL, n_max REAL, 
        p_min REAL, p_max REAL, 
        k_min REAL, k_max REAL,
        ph_min REAL, ph_max REAL, 
        c_n REAL, c_p REAL, c_k REAL)""")
    
    # creating table (fertilizers)
    sql.execute("""CREATE TABLE IF NOT EXISTS fertilizers (
        element TEXT, 
        name TEXT, 
        content_pct REAL, 
        method TEXT, 
        notes TEXT)""")



    # inserting culture
    crops = [("wheat", "Пшеница озимая"), ("potato", "Картофель"), ("tomato", "Томат")]
    sql.executemany("INSERT OR IGNORE INTO crops (name, display_name) VALUES (?,?)", crops)

    # inserting values
    norms = [
        ("wheat", 60, 90, 50, 80, 130, 180, 6.0, 7.5, 1.0, 0.9, 0.85),
        ("potato", 70, 110, 60, 90, 150, 220, 5.5, 6.5, 0.9, 1.2, 1.40),
        ("tomato", 80, 120, 70, 100, 160, 240, 6.2, 6.8, 1.1, 1.2, 1.50)
    ]
    sql.executemany("INSERT OR IGNORE INTO crop_norms VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", norms)



    # filling the table with data
    fertilizers = [
        ("N", "Аммиачная селитра", 34.0, "основное (весна)", "Аммонийно-нитратный азот"),
        ("P", "Двойной суперфосфат", 45.0, "основное (осень)", "Требует глубокой заделки"),
        ("K", "Сульфат калия", 50.0, "предпосевное", "Бесхлорное, идеально для овощей"),
        ("lime", "Известь молотая", 100.0, "основное под вспашку", "Для нейтрализации кислотности")
    ]
    sql.executemany("INSERT OR IGNORE INTO fertilizers VALUES (?,?,?,?,?)", fertilizers)


    # saving what function does
    conn.commit()
    conn.close()


def get_crops_list():
    # Getting list of crops from database
    conn = get_Connection()
    sql = conn.cursor()
    
    sql.execute("SELECT name, display_name FROM crops ORDER BY display_name")
    res = sql.fetchall()
    conn.close()
    return res

def get_crop_data(crop_name):
    # Getting data for crop from database
    conn = get_Connection()
    sql = conn.cursor()

    sql.execute("SELECT * FROM crop_norms WHERE crop_name = ?", (crop_name))
    res = sql.fetchall()
    conn.close()
    return res

def get_fertilizer_by_elem(element):
    # Getting fertilizer by element from database
    conn = get_Connection()
    sql = conn.cursor()
    
    sql.execute("SELECT name, content_pct, method, notes FROM fertilizers WHERE element = ?", (element,))
    res = sql.fetchone()
    
    conn.close()
    return res