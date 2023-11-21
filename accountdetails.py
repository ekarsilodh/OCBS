import streamlit as st
import database_manager as dm
import functionsmodule as fm

# Database files for profiles
db_file_driver = "Databases/driver_data.db"    #for driver
db_file_rider = "Databases/rider_data.db"      #for rider

def details_edit(fullname, state):
    st.title("Account Details Edit")

    if state == "Driver":
        # retrieving the user profile info
        user_info = dm.retrieve_user(db_file_driver, fullname, state)
        # accessing the binary image
        image_binary = user_info[11]

        #create tabs for account edit options
        tab1, tab2, tab3 = st.tabs(["Add/Update Profile Picture", "Update Profile Details", "Add/Update Vehicle Details"])

        #Access tab1 for profile picture change
        with tab1:
            #columns for current and edit option
            col1, col2 = st.columns(2,gap="large")

            #col2 to update dp option
            with col2:
                st.subheader(":blue[Add/Update Profile Picture]")
                profile_picture = st.file_uploader("Choose a profile picture(within 150KB)", type=["jpg", "png", "jpeg"])

                # Check if an image is uploaded
                if profile_picture is not None:
                    # Read binary data of the uploaded image
                    image_binary_data = profile_picture.read()
                    if dm.insert_profile_image(db_file_driver, user_info[3], image_binary_data, state):
                        st.success("Profile Picture Updated")
                        # retrieving the update user profile info
                        user_info = dm.retrieve_user(db_file_driver, fullname, state)
                        # accessing the binary image
                        image_binary = user_info[11]

                        st.session_state.dp_state = True
                        st.session_state.dp_state_refresh = "Refresh"
                    else:
                        st.error("Profile Picture Upload Failed!!!")
                else:
                    # If no image is uploaded, display a message
                    st.write("Please upload an image.")

            #col1 to show the dp
            with col1:
                st.subheader(":orange[Current Profile Picture]")
                img = fm.fetchdp(image_binary)
                if img is not None:
                    st.session_state.dp_state = True
                    st.session_state.dp_state_refresh = "Refresh"
                elif img is None:
                    st.write("No Profile Picture")
                if st.session_state.dp_state and st.session_state.dp_state_refresh == "Refresh" and img is not None:
                    st.image(img, use_column_width=True)
                    st.session_state.dp_state_refresh = None

        # Access tab2 for profile details change
        with tab2:
            # columns for current and edit option
            col1, col2, col3, col4 = st.columns(4)

            #col2 for changing password
            with col2:
                st.subheader(":blue[Update Password]")
                new_password = st.text_input("New Password", type="password", key="driver_changepswd_password").strip()
                confirm_password = st.text_input("Confirm Password", type="password").strip()
                # check for matching of password & confirm password
                if new_password and confirm_password:
                    if new_password != confirm_password:
                        st.warning("Passwords don't match!!!")
                    if new_password == confirm_password:
                        st.success("Passwords matched!")
                        st.session_state.paswd_matched = True
                if st.session_state.paswd_matched:
                    if st.button("Change Password"):
                        if new_password == user_info[4]:
                            st.error("New Password is same as old password!!!")
                            st.session_state.paswd_matched = False
                        else:
                            if dm.change_password_driver(db_file_driver, user_info[3], new_password):
                                st.success("Password Changed Successfully!!")
                                st.session_state.paswd_matched = False
                            else:
                                st.error("Password Changing Failed!!!")
                                st.session_state.paswd_matched = False

            #col3 for changing email
            with col3:
                st.subheader(":blue[Update Email]")
                new_email = st.text_input("New Email", key="driver_email_update").strip()
                if new_email:
                    #check if entered email is valid
                    if fm.is_valid_email(new_email):
                        #check if new email is same as old one
                        if new_email == user_info[6]:
                            st.error("New Email is same as old one!!!")
                        if new_email != user_info[6] and not st.session_state.update_state:
                            if st.button("Change Email"):
                                if dm.verify_email(db_file_driver, new_email, state):
                                    st.error("Email already registered!!!")
                                else:
                                    if dm.change_email_driver(db_file_driver, user_info[3], new_email):
                                        st.success("Email changed")
                                        st.session_state.update_state = True
                                        st.session_state.update_state_refresh = "Refresh"
                                    else:
                                        st.error("Email Changing Failed!!!")
                                        st.session_state.update_state = False
                                        st.session_state.update_state_refresh = None
                    else:
                        st.error("Entered email is not valid")

            # col3 for changing email
            with col4:
                st.subheader(":blue[Update Phone Number]")
                new_phone = st.text_input("New Phone Number", key="driver_phone_update").strip()
                if new_phone:
                    # check if entered phone number is valid
                    if len(new_phone) != 10 or not new_phone.isdigit():
                        st.warning("Enter valid phone number!!!")
                    else:
                        # check if new phone number is same as old one
                        if new_phone == user_info[7]:
                            st.error("New Phone Number is same as old one!!!")
                        if new_phone != user_info[7] and not st.session_state.update_state:
                            if st.button("Change Phone Number"):
                                if dm.verify_phone_number(db_file_driver, new_phone, state):
                                    st.error("Phone Number already registered!!!")
                                else:
                                    if dm.change_phone_driver(db_file_driver, user_info[3], new_phone):
                                        st.success("Phone Number changed")
                                        st.session_state.update_state = True
                                        st.session_state.update_state_refresh = "Refresh"
                                    else:
                                        st.error("Phone Number Changing Failed!!!")
                                        st.session_state.update_state = False
                                        st.session_state.update_state_refresh = None

            #col1 to show the current details
            with col1:
                st.subheader(":orange[Current Details]")
                if user_info is not None:
                    st.session_state.update_state = True
                    st.session_state.update_state_refresh = "Refresh"
                if st.session_state.update_state and st.session_state.update_state_refresh == "Refresh":
                    user_info = dm.retrieve_user(db_file_driver, fullname, state)
                    st.write(f"Email: {user_info[6]}")
                    st.write(f"Phone Number: {user_info[7]}")
                    st.session_state.update_state = False
                    st.session_state.update_state_refresh = None

        # Access tab3 for vehicle details change
        with tab3:
            # columns for current and edit option
            col1, col2, col3, col4 = st.columns(4)

            #col2 for add vehicle details
            with col2:
                st.subheader(":violet[Add/Change Vehicle Details]")
                company = st.text_input("Enter Vehicle Company", key="vehicle_company").strip()
                model = st.text_input("Enter Vehicle Model", key="vehicle_model").strip()

                #cols for company & model change button
                bcol1, bcol2 = st.columns(2)

                #col for company change
                with bcol1:
                    if company:
                        if st.button("Add/Change Company", use_container_width=True):
                            if dm.edit_vehicle_company(db_file_driver, user_info[3], company):
                                st.success("Vehicle Company Updated!")
                                st.session_state.update_state = True
                                st.session_state.update_state_refresh = "Refresh"
                            else:
                                st.error("Vehicle Company can't be updated!!!")
                                st.session_state.update_state = False
                                st.session_state.update_state_refresh = None

                #col for model change
                with bcol2:
                    if model:
                        if model == user_info[13]:
                            st.error("New vehicle model can't be same as old one!!!")
                        else:
                            if st.button("Add/Change Model", use_container_width=True):
                                if dm.edit_vehicle_model(db_file_driver, user_info[3], model):
                                    st.success("Vehicle Model Updated!")
                                    st.session_state.update_state = True
                                    st.session_state.update_state_refresh = "Refresh"
                                else:
                                    st.error("Vehicle Model can't be updated!!!")
                                    st.session_state.update_state = False
                                    st.session_state.update_state_refresh = None

                if company and model and model != user_info[13]:
                    if st.button("Add/Change Company & Model", use_container_width=True):
                        if dm.edit_vehicle_company(db_file_driver, user_info[3], company) and dm.edit_vehicle_model(db_file_driver, user_info[3], model):
                            st.success("Vehicle Company Updated!")
                            st.success("Vehicle Model Updated!")
                            st.session_state.update_state = True
                            st.session_state.update_state_refresh = "Refresh"
                        else:
                            st.error("Vehicle Company can't be updated!!!")
                            st.error("Vehicle Model can't be updated!!!")
                            st.session_state.update_state = False
                            st.session_state.update_state_refresh = None

            # col3 for changing vehicle details
            with col3:
                st.subheader(":violet[Change Vehicle Type]")
                vehicle_type = st.selectbox("Select the Vehicle Type", ("Mini", "Sedan", "SUV", "Bike"), index=None)
                if vehicle_type:
                    if vehicle_type == user_info[9]:
                        st.error("Select a different vehicle type from the current one!!!")
                    if vehicle_type != user_info[9]:
                        if st.button("Change Vehicle Type"):
                            if dm.change_vehicle_type(db_file_driver, user_info[3], vehicle_type):
                                st.success("Vehicle Type Changed!")
                                st.session_state.update_state = True
                                st.session_state.update_state_refresh = "Refresh"
                            else:
                                st.error("Vehicle Type can't be changed!!!")
                                st.session_state.update_state = False
                                st.session_state.update_state_refresh = None

            # col4 for changing vehicle number
            with col4:
                st.subheader(":violet[Change Vehicle Number]")
                vehicle_number = st.text_input("Enter New Vehicle Number", key="changing_vehicle_number")
                if vehicle_number:
                    if vehicle_number == user_info[10]:
                        st.error("New Vehicle Number can't be same as old one!!!")
                    if vehicle_number != user_info[10]:
                        if st.button("Change Vehicle Number"):
                            if dm.change_vehicle_number(db_file_driver, user_info[3], vehicle_number):
                                st.success("Vehicle Number Changed!")
                                st.session_state.update_state = True
                                st.session_state.update_state_refresh = "Refresh"
                            else:
                                st.error("Vehicle Number can't be changed!!!")
                                st.session_state.update_state = False
                                st.session_state.update_state_refresh = None

            # col1 to show the current details
            with col1:
                st.subheader(":orange[Current Details]")
                if user_info is not None:
                    st.session_state.update_state = True
                    st.session_state.update_state_refresh = "Refresh"
                if st.session_state.update_state and st.session_state.update_state_refresh == "Refresh":
                    user_info = dm.retrieve_user(db_file_driver, fullname, state)
                    st.write(f"Vehicle Type: {user_info[9]}")
                    st.write(f"Vehicle Number: {user_info[10]}")
                    st.write(f"Company: {user_info[12]}")
                    st.write(f"Model: {user_info[13]}")
                    st.session_state.update_state = False
                    st.session_state.update_state_refresh = None

    #Options for the rider settings
    if state == "Rider":
        # retrieving the user profile info
        user_info = dm.retrieve_user(db_file_rider, fullname, state)
        # accessing the binary image
        image_binary = user_info[7]

        #create tabs for account edit options
        tab1, tab2, tab3 = st.tabs(["Add/Update Profile Picture", "Update Profile Details", "Add/Update Home Address"])

        #Access tab1 for profile picture change
        with tab1:
            #columns for current and edit option
            col1, col2 = st.columns(2,gap="large")

            #col2 to update dp option
            with col2:
                st.subheader(":blue[Add/Update Profile Picture]")
                profile_picture = st.file_uploader("Choose a profile picture(within 150KB)", type=["jpg", "png", "jpeg"])

                # Check if an image is uploaded
                if profile_picture is not None:
                    # Read binary data of the uploaded image
                    image_binary_data = profile_picture.read()
                    if dm.insert_profile_image(db_file_rider, user_info[2], image_binary_data, state):
                        st.success("Profile Picture Updated")
                        # retrieving the update user profile info
                        user_info = dm.retrieve_user(db_file_rider, fullname, state)
                        # accessing the binary image
                        image_binary = user_info[7]

                        st.session_state.dp_state = True
                        st.session_state.dp_state_refresh = "Refresh"
                    else:
                        st.error("Profile Picture Upload Failed!!!")
                else:
                    # If no image is uploaded, display a message
                    st.write("Please upload an image.")

            #col1 to show the dp
            with col1:
                st.subheader(":orange[Current Profile Picture]")
                img = fm.fetchdp(image_binary)
                if img is not None:
                    st.session_state.dp_state = True
                    st.session_state.dp_state_refresh = "Refresh"
                elif img is None:
                    st.write("No Profile Picture")
                if st.session_state.dp_state and st.session_state.dp_state_refresh == "Refresh" and img is not None:
                    st.image(img, use_column_width=True)
                    st.session_state.dp_state_refresh = None

        # Access tab2 for profile details change
        with tab2:
            # columns for current and edit option
            col1, col2, col3, col4 = st.columns(4)

            #col2 for changing password
            with col2:
                st.subheader(":blue[Update Password]")
                new_password = st.text_input("New Password", type="password", key="rider_changepswd_password").strip()
                confirm_password = st.text_input("Confirm Password", type="password").strip()
                # check for matching of password & confirm password
                if new_password and confirm_password:
                    if new_password != confirm_password:
                        st.warning("Passwords don't match!!!")
                    if new_password == confirm_password:
                        st.success("Passwords matched!")
                        st.session_state.paswd_matched = True
                if st.session_state.paswd_matched:
                    if st.button("Change Password"):
                        if new_password == user_info[3]:
                            st.error("New Password is same as old password!!!")
                            st.session_state.paswd_matched = False
                        else:
                            if dm.change_password_rider(db_file_rider, user_info[2], new_password):
                                st.success("Password Changed Successfully!!")
                                st.session_state.paswd_matched = False
                            else:
                                st.error("Password Changing Failed!!!")
                                st.session_state.paswd_matched = False

            #col3 for changing email
            with col3:
                st.subheader(":blue[Update Email]")
                new_email = st.text_input("New Email", key="rider_email_update").strip()
                if new_email:
                    #check if entered email is valid
                    if fm.is_valid_email(new_email):
                        #check if new email is same as old one
                        if new_email == user_info[5]:
                            st.error("New Email is same as old one!!!")
                        if new_email != user_info[5] and not st.session_state.update_state:
                            if st.button("Change Email"):
                                if dm.verify_email(db_file_rider, new_email, state):
                                    st.error("Email already registered!!!")
                                else:
                                    if dm.change_email_rider(db_file_rider, user_info[2], new_email):
                                        st.success("Email changed")
                                        st.session_state.update_state = True
                                        st.session_state.update_state_refresh = "Refresh"
                                    else:
                                        st.error("Email Changing Failed!!!")
                                        st.session_state.update_state = False
                                        st.session_state.update_state_refresh = None
                    else:
                        st.error("Entered email is not valid")

            # col3 for changing email
            with col4:
                st.subheader(":blue[Update Phone Number]")
                new_phone = st.text_input("New Phone Number", key="rider_phone_update").strip()
                if new_phone:
                    # check if entered phone number is valid
                    if len(new_phone) != 10 or not new_phone.isdigit():
                        st.warning("Enter valid phone number!!!")
                    else:
                        # check if new phone number is same as old one
                        if new_phone == user_info[6]:
                            st.error("New Phone Number is same as old one!!!")
                        if new_phone != user_info[6] and not st.session_state.update_state:
                            if st.button("Change Phone Number"):
                                if dm.verify_phone_number(db_file_rider, new_phone, state):
                                    st.error("Phone Number already registered!!!")
                                else:
                                    if dm.change_phone_rider(db_file_rider, user_info[2], new_phone):
                                        st.success("Phone Number changed")
                                        st.session_state.update_state = True
                                        st.session_state.update_state_refresh = "Refresh"
                                    else:
                                        st.error("Phone Number Changing Failed!!!")
                                        st.session_state.update_state = False
                                        st.session_state.update_state_refresh = None

            #col1 to show the current details
            with col1:
                st.subheader(":orange[Current Details]")
                if user_info is not None:
                    st.session_state.update_state = True
                    st.session_state.update_state_refresh = "Refresh"
                if st.session_state.update_state and st.session_state.update_state_refresh == "Refresh":
                    user_info = dm.retrieve_user(db_file_rider, fullname, state)
                    st.write(f"Email: {user_info[5]}")
                    st.write(f"Phone Number: {user_info[6]}")
                    st.session_state.update_state = False
                    st.session_state.update_state_refresh = None

        # Access tab3 for home address change change
        with tab3:
            # columns for current and edit option
            col1, col2 = st.columns(2, gap="large")

            # col2 to update dp option
            with col2:
                st.subheader(":violet[Add/Update Home Address]")
                address = st.text_input("Home Address", key="rider_address_update").strip()
                if address:
                    if address == user_info[8]:
                        st.error("New Address can't be same as old address!!!")
                    if address != user_info[8] and not st.session_state.update_state:
                        if st.button("Add/Update Address"):
                            if dm.edit_rider_address(db_file_rider, user_info[2], address):
                                st.success("Home Address updated!")
                                st.session_state.update_state = True
                                st.session_state.update_state_refresh = "Refresh"
                            else:
                                st.error("Address Update Failed!!!")
                                st.session_state.update_state = False
                                st.session_state.update_state_refresh = None

            # col1 to show the dp
            with col1:
                st.subheader(":orange[Current Home Address]")
                if user_info is not None:
                    st.session_state.update_state = True
                    st.session_state.update_state_refresh = "Refresh"
                if st.session_state.update_state and st.session_state.update_state_refresh == "Refresh":
                    user_info = dm.retrieve_user(db_file_rider, fullname, state)
                    st.write(f"Home Address: {user_info[8]}")
                    st.session_state.update_state = False
                    st.session_state.update_state_refresh = None