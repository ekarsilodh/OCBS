import streamlit as st
import time
import functionsmodule as fm
import database_manager as dm

# Database files for profiles
db_file_driver = "Databases/driver_data.db"    #for driver
db_file_rider = "Databases/rider_data.db"      #for rider

# Database files for history
db_history_driver = "Databases/driver_history.db"    #for driver
db_history_rider = "Databases/rider_history.db"      #for rider

#Database file for ride booking
db_book_data = "Databases/book_data.db"

def display_orders(username):
    st.header("Dashboard - Accept/Reject Rides")
    if st.button("Look for orders"):
        #ftech the start time
        start_time = time.time()
        with st.spinner("Looking for orders..."):
            while True:
                user_cab = dm.retrieve_cab_driver(db_book_data, username)
                if user_cab[3] == "Booked":
                    st.session_state.booking_state = True
                    st.session_state.booking_state_details = user_cab
                    break

                #fetch the current time
                current_time = time.time()
                #check if 1 min is passed
                if current_time - start_time >= 60:
                    st.info("No Orders Found!!!")
                    st.session_state.booking_state = False
                    break

    #two cols for options
    col1, col2 = st.columns(2, gap="large")
    with col1:
        #look if any orders are found
        if st.session_state.booking_state:
            st.info("Order Found")
            st.write(f"Pick-Up: {st.session_state.booking_state_details[5]}")
            st.write(f"Drop-Off: {st.session_state.booking_state_details[6]}")
            st.write(f"Fare: ₹{st.session_state.booking_state_details[7]}")
            st.write(f"Booking Type: {st.session_state.booking_state_details[9]}")

    with col2:
        if st.session_state.booking_state:
            if st.button("Accept Order"):
                dm.accept_order(db_book_data, "Accepted", username)
                st.info("Order Accepted!!")

            if st.button(":red[Reject Order]"):
                dm.reject_order(db_book_data, "Free", username)
                dm.accept_order(db_book_data, "Free", username)
                st.warning("Order Rejected!!")
                st.session_state.booking_state = False

