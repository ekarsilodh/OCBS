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

def display_book_cab(fullname):
    st.header("Dashboard - Book a Cab")

    #tabs for booking types
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Shown Fare", "Offer Own Fare", "Intercity Booking",
                                                  "Round Trip Booking", "Hourly Rental", "Self Drive Rental"])

    with tab1:
        st.header("Book On Shown Fare")

        # User input section
        pickup_location = st.text_input("Pickup Location", key="pickup_location")
        dropoff_location = st.text_input("Drop-off Location", key="dropoff_location")
        num_passengers = st.number_input("Enter the Number of Passengers", min_value=1, value=1)
        cab_type = st.selectbox("Choose a Cab Type", ["Mini", "Sedan", "SUV", "Bike"], index=None, placeholder="Select Cab Type")

        #to check if all the fields are entered
        if pickup_location and dropoff_location and cab_type and num_passengers:
            if num_passengers > 1 and cab_type == "Bike":
                st.warning("Bike can be used for only one rider!!!")
            elif num_passengers > 4 and cab_type == "Mini":
                st.warning(f"{cab_type} can only accomodate maximum of 4 passengers!!!")
            elif num_passengers > 4 and cab_type == "Sedan":
                st.warning(f"{cab_type} can only accomodate maximum of 4 passengers!!!")
            else:
                # calculate the distance
                distance = fm.distance_calculator(pickup_location, dropoff_location)
                with st.spinner("Calculating Fare"):
                    fare = fm.fare_calculator(distance, num_passengers, cab_type)

                st.info(f"Estimated Fare: ₹{fare}")

                if st.button("Book Cab"):
                    st.subheader("Booking Details")
                    st.write(f"Pickup Location: {pickup_location}")
                    st.write(f"Drop-off Location: {dropoff_location}")
                    st.write(f"Cab Type: {cab_type}")
                    st.write(f"Number of Passengers: {num_passengers}")
                    st.write(f"Estimated Fare: ₹{fare}")

                    #check for all available cabs in pickup_location
                    cabs = dm.retrieve_cab(db_book_data, pickup_location)
                    if len(cabs) < 1:
                        cabs = None
                    #check if cabs are present
                    if cabs is not None:
                        # create a list to store all possible cabs
                        possible_cabs = []
                        #check for cab type
                        for i in range(len(cabs)):
                            user_info = dm.retrieve_user_cab(db_file_driver, cabs[i][1])
                            #fill the possible cabs list
                            if user_info[9] == cab_type:
                                driver_id = cabs[i][1]
                                possible_cabs.append(driver_id)

                        # initialise a count variable
                        lb = 0
                        #st.write(possible_cabs)
                        while st.session_state.booking_state_refresh:
                            if not st.session_state.booking_state:
                                st.info("Cab Found....Booking in Progress....")
                                #update the database for book cab
                                dm.update_book_cab_data(db_book_data, possible_cabs[lb], "Booked", pickup_location, dropoff_location, fare, "Shown Fare")
                                st.session_state.booking_state = True
                                # fetch the start time
                                start_time = time.time()
                                while st.session_state.booking_state_available:
                                    user_info = dm.check_ride_accept(db_book_data, possible_cabs[lb])
                                    if user_info[8] == "Accepted":
                                        st.info("Cab Booked!")
                                        driver_details = dm.retrieve_booked_user(db_file_driver, possible_cabs[lb])
                                        st.info(f"```\nCab Details:\nCab Type: {cab_type}\nCab Number: {driver_details[10]}\nCab Model: {driver_details[12]} {driver_details[13]}\n```")
                                        st.session_state.booking_state_available = False
                                        st.session_state.booking_state_refresh = False
                                    elif user_info[3] == "Free":
                                        lb = lb + 1
                                        if lb == len(possible_cabs):
                                            st.warning("No cabs found!!!")
                                            st.session_state.booking_state_available = False
                                            st.session_state.booking_state = False
                                        st.session_state.booking_state = False
                                        st.session_state.booking_state_available = False

                                    # fetch the current time
                                    current_time = time.time()
                                    #check if 1 min is passed
                                    if current_time - start_time >= 60:
                                        lb = lb + 1
                                        if lb == len(possible_cabs):
                                            st.warning("No cabs found!!!")
                                            st.session_state.booking_state_available = False
                                            st.session_state.booking_state = False
                                        dm.reject_order(db_book_data, "Free", driver_details[3])
                                        dm.accept_order(db_book_data, "Free", driver_details[3])
                                        st.session_state.booking_state = False
                                        st.session_state.booking_state_available = False

                    if cabs is None:
                        st.error("No cabs found!!!")

