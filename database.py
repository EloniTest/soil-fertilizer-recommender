import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def get_Connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    # Creating tables and filling directories if there is no database


def get_crops_list():
    # Getting list of crops from database

def get_crop_data(crop_name):
    # Getting data for crop from database

def get_fertilizer_by_elem(element):
    # Getting fertilizer by element from database

