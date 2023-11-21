import streamlit as st
import sqlite3
from sqlite3 import Error

# Create the users table for drivers if it doesn't exist
def create_table_driver(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS driver_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        driver_id TEXT NOT NULL UNIQUE,  -- Added driver_id field
        full_name TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        dob DATE NOT NULL,
        email TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        dl_number TEXT NOT NULL,
        vehicle_type TEXT NOT NULL,
        vehicle_number TEXT NOT NULL,
        profile_image BLOB,
        company TEXT,
        model TEXT
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        st.error(str(e))

# Create the users table for drivers history if it doesn't exist
def create_history_driver(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS drivers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        driver_id TEXT NOT NULL UNIQUE,
        full_name TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        rides_completed INTEGER DEFAULT 0,
        rides_cancelled INTEGER DEFAULT 0,
        rating REAL DEFAULT 0.0,
        availability_status TEXT DEFAULT 'Available',
        earnings REAL DEFAULT 0.0,
        rating_count REAL DEFAULT 0.0
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        st.error(str(e))

# Create the users table for riders if it doesn't exist
def create_table_rider(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS rider_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        dob DATE NOT NULL,
        email TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        profile_image BLOB,
        address TEXT
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        st.error(str(e))

# Create the users table for riders history if it doesn't exist
def create_history_rider(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS riders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        rides_completed INTEGER DEFAULT 0,
        rides_cancelled INTEGER DEFAULT 0,
        rating REAL DEFAULT 0.0,
        mini_rides INTEGER DEFAULT 0,
        sedan_rides INTEGER DEFAULT 0,
        suv_rides INTEGER DEFAULT 0,
        bike_rides INTEGER DEFAULT 0,
        last_ride_mode TEXT DEFAULT NULL,
        last_ride_on DATE DEFAULT NULL,
        rating_count REAL DEFAULT 0.0
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        st.error(str(e))

def create_table_book_cab(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS cabs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        driver_id TEXT NOT NULL UNIQUE,  -- Added driver_id field
        username TEXT NOT NULL UNIQUE,
        booked_status TEXT DEFAULT 'Free',
        current_location TEXT NOT NULL,
        source TEXT,
        destination TEXT,
        fare INTEGER,
        accept_status TEXT,
        booking_type TEXT 
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        st.error(str(e))

# Create a SQLite database or connect to an existing one
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        st.error(str(e))
    return conn

# checking for driver table
def check_table_driver(db_file):
    conn = create_connection(db_file)
    if conn is not None:
        create_table_driver(conn)
        conn.close()
    if conn:
        conn.close()

# checking for rider table
def check_table_rider(db_file):
    conn = create_connection(db_file)
    if conn is not None:
        create_table_rider(conn)
        conn.close()
    if conn:
        conn.close()

# checking for driver history table
def check_history_driver(db_file):
    conn = create_connection(db_file)
    if conn is not None:
        create_history_driver(conn)
        conn.close()
    if conn:
        conn.close()

# checking for rider history table
def check_history_rider(db_file):
    conn = create_connection(db_file)
    if conn is not None:
        create_history_rider(conn)
        conn.close()
    if conn:
        conn.close()

#checking for book cab table
def check_book_cab(db_file):
    conn = create_connection(db_file)
    if conn is not None:
        create_table_book_cab(conn)
        conn.close()
    if conn:
        conn.close()

# Insert a new driver into the database
def insert_driver(db_file, driver_id, full_name, username, password, dob, email, phone_number, dl_number, vehicle_type, vehicle_number):
    with sqlite3.connect(db_file) as conn:
        # Modified SQL query to insert user data including driver_id
        insert_user_sql = "INSERT INTO driver_users (driver_id, full_name, username, password, dob, email, phone_number, dl_number, vehicle_type, vehicle_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
        try:
            c = conn.cursor()
            c.execute(insert_user_sql, (driver_id, full_name, username, password, dob, email, phone_number, dl_number, vehicle_type, vehicle_number))
            conn.commit()
        except Error as e:
            st.error(str(e))

#for driver history database
def insert_driver_history(db_file, driver_id, full_name, username):
    with sqlite3.connect(db_file) as conn:
        insert_driver_sql = """
        INSERT INTO drivers (driver_id, full_name, username) VALUES (?, ?, ?);
        """
        try:
            c = conn.cursor()
            c.execute(insert_driver_sql, (driver_id, full_name, username))
            conn.commit()
        except Error as e:
            st.error(str(e))

#for book cab database
def insert_book_cab(db_file, driver_id, username, home_location):
    with sqlite3.connect(db_file) as conn:
        insert_driver_sql = """
        INSERT INTO cabs (driver_id, username, current_location) VALUES (?, ?, ?);
        """
        try:
            c = conn.cursor()
            c.execute(insert_driver_sql, (driver_id, username, home_location))
            conn.commit()
        except Error as e:
            st.error(str(e))

# Insert a new rider into the database
def insert_rider(db_file, full_name, username, password, dob, email, phone_number):
    with sqlite3.connect(db_file) as conn:
        # Your existing SQL query for inserting user data into the database
        insert_user_sql = "INSERT INTO rider_users (full_name, username, password, dob, email, phone_number) VALUES (?, ?, ?, ?, ?, ?);"
        try:
            c = conn.cursor()
            c.execute(insert_user_sql, (full_name, username, password, dob, email, phone_number))
            conn.commit()
        except Error as e:
            st.error(str(e))

#for rider history database
def insert_rider_history(db_file, full_name, username):
    with sqlite3.connect(db_file) as conn:
        insert_rider_sql = """
        INSERT INTO riders (full_name, username) VALUES (?, ?);
        """
        try:
            c = conn.cursor()
            c.execute(insert_rider_sql, (full_name, username))
            conn.commit()
        except Error as e:
            st.error(str(e))

#for driver
def change_password_driver(db_file, username_or_driver_id, new_password):
    with sqlite3.connect(db_file) as conn:
        # Modify password for a specific username or driver_id
        update_password_sql = "UPDATE driver_users SET password = ? WHERE (username = ? OR driver_id = ?);"
        try:
            c = conn.cursor()
            c.execute(update_password_sql, (new_password, username_or_driver_id, username_or_driver_id))
            conn.commit()
            return True
        except Error as e:
            st.error(str(e))

#for rider
def change_password_rider(db_file, username, new_password):
    with sqlite3.connect(db_file) as conn:
        # Modify password for a specific username or driver_id
        update_password_sql = "UPDATE rider_users SET password = ? WHERE username = ?;"
        try:
            c = conn.cursor()
            c.execute(update_password_sql, (new_password, username))
            conn.commit()
            return True
        except Error as e:
            st.error(str(e))
#for driver
def change_email_driver(db_file, username, new_email):
    with sqlite3.connect(db_file) as conn:
        # Modify password for a specific username or driver_id
        update_password_sql = "UPDATE driver_users SET email = ? WHERE username = ?;"
        try:
            c = conn.cursor()
            c.execute(update_password_sql, (new_email, username))
            conn.commit()
            return True
        except Error as e:
            st.error(str(e))

#for rider
def change_email_rider(db_file, username, new_email):
    with sqlite3.connect(db_file) as conn:
        # Modify password for a specific username or driver_id
        update_password_sql = "UPDATE rider_users SET email = ? WHERE username = ?;"
        try:
            c = conn.cursor()
            c.execute(update_password_sql, (new_email, username))
            conn.commit()
            return True
        except Error as e:
            st.error(str(e))

# for driver
def change_phone_driver(db_file, username, new_phone):
    with sqlite3.connect(db_file) as conn:
        # Modify password for a specific username or driver_id
        update_password_sql = "UPDATE driver_users SET phone_number = ? WHERE username = ?;"
        try:
            c = conn.cursor()
            c.execute(update_password_sql, (new_phone, username))
            conn.commit()
            return True
        except Error as e:
            st.error(str(e))

# for rider
def change_phone_rider(db_file, username, new_phone):
    with sqlite3.connect(db_file) as conn:
        # Modify password for a specific username or driver_id
        update_password_sql = "UPDATE rider_users SET phone_number = ? WHERE username = ?;"
        try:
            c = conn.cursor()
            c.execute(update_password_sql, (new_phone, username))
            conn.commit()
            return True
        except Error as e:
            st.error(str(e))

#return full_name for driver
def fullname_driver(db_file, username):
    with sqlite3.connect(db_file) as conn:
        select_user_sql = "SELECT * FROM driver_users WHERE username = ?;"
        try:
            c = conn.cursor()
            c.execute(select_user_sql, (username,))
            user = c.fetchone()
            if user is not None:
                full_name = user[2]  # Assuming full_name is at index 2 in the user tuple, modify accordingly
                return full_name
            else:
                return None
        except Error as e:
            st.error(str(e))  # Assuming st.error is a function to handle errors, modify accordingly
            return False

#return full_name for rider
def fullname_rider(db_file, username):
    with sqlite3.connect(db_file) as conn:
        select_user_sql = "SELECT * FROM rider_users WHERE username = ?;"
        try:
            c = conn.cursor()
            c.execute(select_user_sql, (username,))
            user = c.fetchone()
            if user is not None:
                full_name = user[1]  # Assuming full_name is at index 2 in the user tuple, modify accordingly
                return full_name
            else:
                return None
        except Error as e:
            st.error(str(e))  # Assuming st.error is a function to handle errors, modify accordingly
            return False

# Verify user credentials
def verify_user(db_file, username, password, mode):
    with sqlite3.connect(db_file) as conn:
        if mode == "Driver":
            select_user_sql = "SELECT * FROM driver_users WHERE username = ? AND password = ?;"
        elif mode == "Rider":
            select_user_sql = "SELECT * FROM rider_users WHERE username = ? AND password = ?;"
        try:
            c = conn.cursor()
            c.execute(select_user_sql, (username, password))
            user = c.fetchone()
            if user is not None:
                return user[3]
            else:
                return None
        except Error as e:
            st.error(str(e))
            return False

def verify_user_driverid(db_file, driverid, password):
    with sqlite3.connect(db_file) as conn:
        select_user_sql = "SELECT * FROM driver_users WHERE driver_id = ? AND password = ?;"
        try:
            c = conn.cursor()
            c.execute(select_user_sql, (driverid, password))
            user = c.fetchone()
            if user is not None:
                return user[3]
            else:
                return None
        except Error as e:
            st.error(str(e))
            return False

def verify_user_forgetpswd(db_file, username, email):
    with sqlite3.connect(db_file) as conn:
        select_user_sql = "SELECT * FROM driver_users WHERE (username = ? OR driver_id = ?) AND email = ?;"
        try:
            c = conn.cursor()
            c.execute(select_user_sql, (username, username, email))
            user = c.fetchone()
            return user is not None
        except Error as e:
            st.error(str(e))
            return False

#for rider
def verify_user_rider_forgetpswd(db_file, username, email):
    with sqlite3.connect(db_file) as conn:
        select_user_sql = "SELECT * FROM rider_users WHERE username = ? AND email = ?;"
        try:
            c = conn.cursor()
            c.execute(select_user_sql, (username, email))
            user = c.fetchone()
            return user is not None
        except Error as e:
            st.error(str(e))
            return False

def verify_email(db_file, email, mode):
    with sqlite3.connect(db_file) as conn:
        if mode == "Driver":
            select_user_sql = "SELECT * FROM driver_users WHERE email = ?;"
        elif mode == "Rider":
            select_user_sql = "SELECT * FROM rider_users WHERE email = ?;"
        try:
            c = conn.cursor()
            c.execute(select_user_sql, (email,))
            user = c.fetchone()
            return user is not None
        except Error as e:
            st.error(str(e))
            return False

def verify_phone_number(db_file, phone_number, mode):
    with sqlite3.connect(db_file) as conn:
        if mode == "Driver":
            select_user_sql = "SELECT * FROM driver_users WHERE phone_number = ?;"
        elif mode == "Rider":
            select_user_sql = "SELECT * FROM rider_users WHERE phone_number = ?;"
        try:
            c = conn.cursor()
            c.execute(select_user_sql, (phone_number,))
            user = c.fetchone()
            return user is not None
        except Error as e:
            st.error(str(e))
            return False

def verify_fullname(db_file, full_name, mode):
    with sqlite3.connect(db_file) as conn:
        if mode == "Driver":
            select_user_sql = "SELECT * FROM driver_users WHERE full_name = ?;"
        elif mode == "Rider":
            select_user_sql = "SELECT * FROM rider_users WHERE full_name = ?;"
        try:
            c = conn.cursor()
            c.execute(select_user_sql, (full_name,))
            user = c.fetchone()
            return user is not None
        except Error as e:
            st.error(str(e))
            return False

def verify_driver_id(db_file, driver_id):
    with sqlite3.connect(db_file) as conn:
        select_user_sql = "SELECT * FROM driver_users WHERE driver_id = ?;"
        try:
            c = conn.cursor()
            c.execute(select_user_sql, (driver_id,))
            user = c.fetchone()
            return user is not None
        except Error as e:
            st.error(str(e))
            return False

#retrieving user info
def retrieve_user(db_file, full_name, mode):
    with sqlite3.connect(db_file) as conn:
        if mode == "Driver":
            select_user_sql = "SELECT * FROM driver_users WHERE full_name = ?;"
        elif mode == "Rider":
            select_user_sql = "SELECT * FROM rider_users WHERE full_name = ?;"
        try:
            c = conn.cursor()
            c.execute(select_user_sql, (full_name,))
            user = c.fetchone()
            if user is not None:
                return user
        except Error as e:
            st.error(str(e))
            return False

#retrieving user history
def retrieve_user_history(db_file, full_name, mode):
    with sqlite3.connect(db_file) as conn:
        if mode == "Driver":
            select_user_sql = "SELECT * FROM drivers WHERE full_name = ?;"
        elif mode == "Rider":
            select_user_sql = "SELECT * FROM riders WHERE full_name = ?;"
        try:
            c = conn.cursor()
            c.execute(select_user_sql, (full_name,))
            user = c.fetchone()
            if user is not None:
                return user
        except Error as e:
            st.error(str(e))
            return False

#retriving current location
def retrieve_current_location(db_file, username):
    with sqlite3.connect(db_file) as conn:
        select_user_sql = "SELECT * FROM cabs WHERE username = ?;"
        try:
            c = conn.cursor()
            c.execute(select_user_sql, (username,))
            user = c.fetchone()
            if user is not None:
                return user
        except Error as e:
            st.error(str(e))
            return False

# Insert profile_image for a particular username into the database
def insert_profile_image(db_file, username, profile_image, mode):
    with sqlite3.connect(db_file) as conn:
        if mode == "Driver":
            update_user_sql = "UPDATE driver_users SET profile_image = ? WHERE username = ?;"
        elif mode == "Rider":
            update_user_sql = "UPDATE rider_users SET profile_image = ? WHERE username = ?;"
        try:
            c = conn.cursor()
            c.execute(update_user_sql, (profile_image, username))
            conn.commit()
            return True
        except Error as e:
            st.error(str(e))
            return False

#change vehicle type
def change_vehicle_type(db_file, username, new_vehicle_type):
    with sqlite3.connect(db_file) as conn:
        # Modify password for a specific username or driver_id
        update_vehicle_type_sql = "UPDATE driver_users SET vehicle_type = ? WHERE username = ?;"
        try:
            c = conn.cursor()
            c.execute(update_vehicle_type_sql, (new_vehicle_type, username))
            conn.commit()
            return True
        except Error as e:
            st.error(str(e))

#change vehicle number
def change_vehicle_number(db_file, username, new_vehicle_number):
    with sqlite3.connect(db_file) as conn:
        # Modify password for a specific username or driver_id
        update_vehicle_number_sql = "UPDATE driver_users SET vehicle_number = ? WHERE username = ?;"
        try:
            c = conn.cursor()
            c.execute(update_vehicle_number_sql, (new_vehicle_number, username))
            conn.commit()
            return True
        except Error as e:
            st.error(str(e))

#edit vehicle company
def edit_vehicle_company(db_file, username, vehicle_company):
    with sqlite3.connect(db_file) as conn:
        # Modify password for a specific username or driver_id
        update_vehicle_company_sql = "UPDATE driver_users SET company = ? WHERE username = ?;"
        try:
            c = conn.cursor()
            c.execute(update_vehicle_company_sql, (vehicle_company, username))
            conn.commit()
            return True
        except Error as e:
            st.error(str(e))

#edit vehicle model
def edit_vehicle_model(db_file, username, vehicle_model):
    with sqlite3.connect(db_file) as conn:
        # Modify password for a specific username or driver_id
        update_vehicle_model_sql = "UPDATE driver_users SET model = ? WHERE username = ?;"
        try:
            c = conn.cursor()
            c.execute(update_vehicle_model_sql, (vehicle_model, username))
            conn.commit()
            return True
        except Error as e:
            st.error(str(e))

#edit rider home address
def edit_rider_address(db_file, username, address):
    with sqlite3.connect(db_file) as conn:
        # Modify password for a specific username or driver_id
        update_address_sql = "UPDATE rider_users SET address = ? WHERE username = ?;"
        try:
            c = conn.cursor()
            c.execute(update_address_sql, (address, username))
            conn.commit()
            return True
        except Error as e:
            st.error(str(e))

#retrieve user for booking
def retrieve_cab(db_file, pickup_location):
    with sqlite3.connect(db_file) as conn:
        #form the sql query
        retrieve_user_sql = "SELECT * FROM cabs WHERE current_location = ? AND booked_status = 'Free';"
        try:
            c = conn.cursor()
            c.execute(retrieve_user_sql, (pickup_location, ))
            user = c.fetchall()
            if user is not None:
                return user
            if user is None:
                return None
        except Error as e:
            st.error(str(e))
            return False

#retrieve user details for cab identification
def retrieve_user_cab(db_file, driver_id):
    with sqlite3.connect(db_file) as conn:
        select_user_sql = "SELECT * FROM driver_users WHERE driver_id = ?;"
        try:
            c = conn.cursor()
            c.execute(select_user_sql, (driver_id,))
            user = c.fetchone()
            if user is not None:
                return user
        except Error as e:
            st.error(str(e))
            return False

#booking details update
def update_book_cab_data(db_file, driver_id, booked_status, pickup_location, dropoff_location, fare, booking_type):
    with sqlite3.connect(db_file) as conn:
        #update booking details query
        update_booking_details = "UPDATE cabs SET booked_status = ?, source = ?, destination = ?, fare = ?, booking_type = ? WHERE driver_id = ?"
        try:
            c = conn.cursor()
            c.execute(update_booking_details, (booked_status, pickup_location, dropoff_location, fare, booking_type, driver_id))
            conn.commit()
            return True
        except Error as e:
            st.error(str(e))

#retrieve user for driver
def retrieve_cab_driver(db_file, username):
    with sqlite3.connect(db_file) as conn:
        #form the sql query
        retrieve_user_sql = "SELECT * FROM cabs WHERE username = ?;"
        try:
            c = conn.cursor()
            c.execute(retrieve_user_sql, (username, ))
            user = c.fetchone()
            if user is not None:
                return user
        except Error as e:
            st.error(str(e))
            return False

#retrieve user details for ride acceptance check
def check_ride_accept(db_file, driver_id):
    with sqlite3.connect(db_file) as conn:
        select_user_sql = "SELECT * FROM cabs WHERE driver_id = ?;"
        try:
            c = conn.cursor()
            c.execute(select_user_sql, (driver_id,))
            user = c.fetchone()
            if user is not None:
                return user
        except Error as e:
            st.error(str(e))
            return False

#order accept
def accept_order(db_file, status, username):
    with sqlite3.connect(db_file) as conn:
        # update booking details query
        update_booking_details = "UPDATE cabs SET accept_status = ? WHERE username = ?"
        try:
            c = conn.cursor()
            c.execute(update_booking_details, (status, username))
            conn.commit()
            return True
        except Error as e:
            st.error(str(e))

#order reject
def reject_order(db_file, status, username):
    with sqlite3.connect(db_file) as conn:
        # update booking details query
        update_booking_details = "UPDATE cabs SET booked_status = ? WHERE username = ?"
        try:
            c = conn.cursor()
            c.execute(update_booking_details, (status, username))
            conn.commit()
            return True
        except Error as e:
            st.error(str(e))

#retrieve user after cab booking
def retrieve_booked_user(db_file, driver_id):
    with sqlite3.connect(db_file) as conn:
        select_user_sql = "SELECT * FROM driver_users WHERE driver_id = ?;"
        try:
            c = conn.cursor()
            c.execute(select_user_sql, (driver_id,))
            user = c.fetchone()
            if user is not None:
                return user
        except Error as e:
            st.error(str(e))
            return False
