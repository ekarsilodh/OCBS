import streamlit as st
import database_manager as dm
import functionsmodule as fm

# Database files for profiles
db_file_driver = "Databases/driver_data.db"    #for driver
db_file_rider = "Databases/rider_data.db"      #for rider

# Database files for history
db_history_driver = "Databases/driver_history.db"    #for driver
db_history_rider = "Databases/rider_history.db"      #for rider

#Database file for ride booking
db_book_data = "Databases/book_data.db"

#function for dashboard in app.py
def display_dashboard(fullname, state):
    st.header(f"{state} Dashboard", divider='green')
    st.header("Welcome to 🚕 CabOnTheGo 🚕")
    st.header(fullname)

    #Dashboard for rider page
    if state == "Rider":
        #retrieving the user profile info
        user_info = dm.retrieve_user(db_file_rider, fullname, state)
        #retriving user history
        user_history = dm.retrieve_user_history(db_history_rider, fullname, state)
        #accessing the binary image
        image_binary = user_info[7]

        # Accessing the rating
        if (user_history[9] != 0):
            rating = user_history[5] / user_history[12]
        else:
            rating = user_history[5]

        #two cols for profile info displaying
        col1, col2, col3 = st.columns(3, gap="large")

        #1st column for profile details
        with col1:
            st.subheader(":blue[Profile Details]")
            st.write(f"Username: {user_info[2]}")
            st.write(f"Name: {user_info[1]}")
            st.write(f"Date of Birth: {user_info[4]}")
            st.write(f"Age: {fm.agecalc_dashboard(user_info[4])} years")
            st.write(f"Email: {user_info[5]}")
            st.write(f"Phone Number: {user_info[6]}")

        # 2nd column for ride details
        with col2:
            st.subheader(":orange[Other Details]")
            with st.expander("Click to view"):
                st.write(f"Rating: {rating} ({user_history[12]})")
                st.write(f"Completed Rides: {user_history[3]}")
                st.write(f"Total Rides: {int(user_history[3]) + int(user_history[4])}")
                st.write(f"Last Ride Type: {user_history[10]}")
                st.write(f"Last Ride On: {user_history[11]}")

        with col3:
            img = fm.fetchdp(image_binary)
            if img is not None:
                st.image(img, use_column_width=True)
            elif img is None:
                st.write("No Profile Picture")

    # Dashboard for driver page
    if state == "Driver":
        # retrieving the user profile info
        user_info = dm.retrieve_user(db_file_driver, fullname, state)
        # retriving user history
        user_history = dm.retrieve_user_history(db_history_driver, fullname, state)
        #retriving current location
        current_location =dm.retrieve_current_location(db_book_data, user_info[3])
        # accessing the binary image
        image_binary = user_info[11]

        #Accessing the rating
        if (user_history[9] != 0):
            rating = user_history[6]/user_history[9]
        else:
            rating = user_history[6]

        # three cols for profile info displaying
        col1, col2, col3 = st.columns(3, gap="large")

        # 1st column for profile details
        with col1:
            st.subheader(":blue[Profile Details]")
            st.write(f"Username: {user_info[3]}")
            st.write(f"Driver Id: {user_info[1]}")
            st.write(f"Name: {user_info[2]}")
            st.write(f"Date of Birth: {user_info[5]}")
            st.write(f"Age: {fm.agecalc_dashboard(user_info[5])} years")
            st.write(f"Email: {user_info[6]}")
            st.write(f"Phone Number: {user_info[7]}")
            st.write(f"DL Number: {user_info[8]}")
            st.write(f"Vehicle Type: {user_info[9]}")
            st.write(f"Vehicle Number: {user_info[10]}")

        # 2nd column for ride details
        with col2:
            st.subheader(":orange[Other Details]")
            with st.expander("Click to view"):
                st.write(f"Rating: {rating} ({user_history[9]})")
                st.write(f"Completed Rides: {user_history[4]}")
                st.write(f"Total Rides: {int(user_history[4]) + int(user_history[5])}")
                st.write(f"Availability Status: {user_history[7]}")
                st.write(f"Current Location: {current_location[4]}")

            with col3:
                img = fm.fetchdp(image_binary)
                if img is not None:
                    st.image(img, use_column_width=True)
                elif img is None:
                    st.write("No Profile Picture")

