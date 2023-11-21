import streamlit as st
import sqlite3
from sqlite3 import Error
import database_manager as dm

# Database files for history
db_history_driver = "Databases/driver_history.db"    #for driver
db_history_rider = "Databases/rider_history.db"      #for rider

# Create a SQLite database or connect to an existing one
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        st.error(str(e))
    return conn


# Create or connect to the database for driver
conn = create_connection(db_history_driver)
if conn is not None:
    create_table_driver(conn)

# Create or connect to the database for rider
conn1 = create_connection(db_history_rider)
if conn is not None:
    create_table_rider(conn1)