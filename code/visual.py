import pandas as pd
import sqlite3
import matplotlib

def do_databasse_stuff():
    global df 
    conn = sqlite3.connect('tunes.db')
    cursor = conn.cursor()
    
    df = pd.read_sql("SELECT * FROM tunes", conn)
    print(df.head())
    conn.close()
do_databasse_stuff()
print(df)


