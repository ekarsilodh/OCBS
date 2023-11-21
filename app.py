import streamlit as st
from datetime import datetime
import pytz
import database_manager as dm
import functionsmodule as fm
from dashboard import display_dashboard
from book_cab import display_book_cab
from accept_reject import display_orders
from accountdetails import details_edit

#defining page name & icon
st.set_page_config(
    page_title="CabOnTheGo",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
    }
)

#real time date time monitoring
utc_now = datetime.now()
ist_timezone = pytz.timezone('Asia/Kolkata')
current_datetime = utc_now.replace(tzinfo=pytz.utc).astimezone(ist_timezone)

#getting current time & date
current_time = current_datetime.strftime("%H:%M")
current_date = current_datetime.strftime("%B %d, %Y")
current_day = current_datetime.strftime("%A")

# Database files for profiles
db_file_driver = "Databases/driver_data.db"    #for driver
db_file_rider = "Databases/rider_data.db"      #for rider

# Database files for history
db_history_driver = "Databases/driver_history.db"    #for driver
db_history_rider = "Databases/rider_history.db"      #for rider

#Database file for ride booking
db_book_data = "Databases/book_data.db"

#Check for databases
dm.check_table_driver(db_file_driver)
dm.check_history_driver(db_history_driver)
dm.check_table_rider(db_file_rider)
dm.check_history_rider(db_history_rider)
dm.check_book_cab(db_book_data)

# Initialize authentication state in session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Initialize username in session state
if 'username' not in st.session_state:
    st.session_state.username = None
    st.session_state.full_name = None

# Initialize otp flag in session state
if 'otp_flag' not in st.session_state:
    st.session_state.otp_flag = False
    st.session_state.generated_otp = None

# Initialize mode selection status in session state
if 'mode_selected' not in st.session_state:
    st.session_state.mode_selected = False
    st.session_state.selected_mode = None

# Initialize sign up/log in mode selection status in session state
if 'signlog_mode_selected' not in st.session_state:
    st.session_state.signlog_mode_selected = False
    st.session_state.signlog_selected_mode = None
    st.session_state.paswd_matched = False

# Initialize mode selection status for dp in session state
if 'dp_state' not in st.session_state:
    st.session_state.dp_state = False
    st.session_state.dp_state_refresh = None

# Initialize profile details in session state
if 'update_state' not in st.session_state:
    st.session_state.update_state = False
    st.session_state.update_state_refresh = None

#Initialize booking state in session state
if 'booking_state' not in st.session_state:
    st.session_state.booking_state = False
    st.session_state.booking_state_details = None
    st.session_state.booking_state_available = True
    st.session_state.booking_state_refresh = True

#Font Selection
st.markdown(
    """
    <head>
        <link href='https://fonts.googleapis.com/css?family=Pacifico' rel='stylesheet'>
        <link href='https://fonts.googleapis.com/css?family=Mooli' rel='stylesheet'>
        <link href='https://fonts.googleapis.com/css?family=Orbitron' rel='stylesheet'>
        <link href='https://fonts.googleapis.com/css?family=Roboto' rel='stylesheet'>
    </head>
    """,
    unsafe_allow_html=True
)

# Page title
st.markdown(
    """
    <h1 style='text-align: center; font-family: Pacifico, sans-serif'>🚕 CabOnTheGo 🚕</h1>
    """,
    unsafe_allow_html=True
)

#Time display
st.markdown(
    """
    <h3 style='text-align: right; font-family: Orbitron, sans-serif'>{}</h3>
    """.format(current_time),
    unsafe_allow_html=True
)

#Date display
st.markdown(
    """
    <h6 style='text-align: right; font-family: Roboto, sans-serif'>{}</h6>
    """.format(current_date),
    unsafe_allow_html=True
)

#Day display
st.markdown(
    """
    <h6 style='text-align: right; font-family: Roboto, sans-serif'>{}</h6>
    """.format(current_day),
    unsafe_allow_html=True
)

# Option Selector
st.markdown(
    """
    <h2 style='text-align: center; color: yellow; font-family: Mooli, sans-serif'>Select Mode: {}</h2>
    """.format(st.session_state.selected_mode),  # Dynamically update the heading based on the selected mode
    unsafe_allow_html=True
)
st.header("", divider='rainbow')

# Check if the user is authenticated
if not st.session_state.authenticated:
    # Check if a mode is already selected
    if not st.session_state.mode_selected:
        col1, col2 = st.columns(2, gap="large")  # Create two columns
        # Driver Mode button in the first column
        with col1:
            st.image("Images/driver.png", use_column_width=True, output_format="PNG")
            if st.button(":orange[Driver]", key='driver_button', help="Driver Mode", use_container_width=True):
                st.session_state.mode_selected = True
                st.session_state.selected_mode = "Driver"

        # Rider Mode button in the second column
        with col2:
            st.image("Images/rider.png", use_column_width=True, output_format="PNG")
            if st.button(":green[Rider]", key='rider_button', help="Rider Mode", use_container_width=True):
                st.session_state.mode_selected = True
                st.session_state.selected_mode = "Rider"

    # Handle mode selection For Driver
    if st.session_state.mode_selected and st.session_state.selected_mode == "Driver":
        st.header(f":orange[{st.session_state.selected_mode} Authentication]")

        # Check if a sign up/log in mode is already selected
        if not st.session_state.signlog_mode_selected:
            col1, col2, col3 = st.columns(3, gap="medium")  # Create two columns
            # Sign Up Mode button in the first column
            with col1:
                if st.button(":orange[Sign Up]", key='driver_signup_button', use_container_width=True):
                    st.session_state.signlog_mode_selected = True
                    st.session_state.signlog_selected_mode = "Sign Up"

            # Log In Mode button in the second column
            with col2:
                if st.button(":green[Log In]", key='driver_login_button', use_container_width=True):
                    st.session_state.signlog_mode_selected = True
                    st.session_state.signlog_selected_mode = "Log In"

            # Forget Password Mode button in the third column
            with col3:
                if st.button(":red[Forget Password]", key='driver_frgtpswd_button', use_container_width=True):
                    st.session_state.signlog_mode_selected = True
                    st.session_state.signlog_selected_mode = "FrgtPswd"

            # creating the back option
            if st.button(":red[Back]", key="mode_select_page"):
                st.session_state.selected_mode = None
                st.session_state.mode_selected = False

        # Handle sign up mode selection & Authentication For Driver
        if st.session_state.signlog_mode_selected and st.session_state.signlog_selected_mode == "Sign Up":
            st.subheader(":orange[Driver Sign Up]")

            # Sign-up
            # Sign Up Details Section
            new_full_name = st.text_input("Full Name").strip()
            new_username = st.text_input("Username", key="driver_signup_username").strip()
            new_password = st.text_input("Password", type="password", key="driver_signup_password").strip()
            confirm_password = st.text_input("Confirm Password", type="password", key="driver_signup_cnfrmpassword").strip()
            # check for matching of password & confirm password
            if new_password and confirm_password:
                if new_password != confirm_password:
                    st.warning("Passwords don't match!!!")
                elif new_password == confirm_password:
                    st.success("Passwords matched!")
                    st.session_state.paswd_matched = True
            dob = st.date_input("Date of Birth", format="DD/MM/YYYY", min_value=datetime(1900, 1, 1))
            # Check for valid age
            if fm.agecalc(dob) < 20:
                st.warning("The user must be 20 years of age!!")
            new_email = st.text_input("Email", key="driver_signup_email").strip()
            # check for a valid email
            if new_email and not fm.is_valid_email(new_email):
                st.warning("Enter a valid email!!!")
            if new_email and fm.is_valid_email(new_email) and not st.session_state.otp_flag:
                # sent OTP to email
                generated_otp = fm.generate_otp()
                st.session_state.generated_otp = generated_otp
                st.session_state.otp_flag = True
                message = f"Your OTP for CabOnTheGo is {generated_otp}"
                with st.status("Sending OTP...") as status:
                    if fm.send_email(new_email, message, "OTP"):
                        status.update(label="OTP Sent Successfully!! Check mail.", state="complete", expanded=False)
                    else:
                        status.update(label="Can't send OTP!!!", state="error")
            phone_number = st.text_input("Phone Number").strip()
            # check for a valid phone number
            if phone_number:
                if len(phone_number) != 10 or not phone_number.isdigit():
                    st.warning("Enter valid phone number!!!")
            dl_number = st.text_input("Enter DL Number").strip()
            vehicle_type = st.selectbox("Select the Vehicle Type", ("Mini", "Sedan", "SUV", "Bike"),index=None)
            vehicle_number = st.text_input("Enter Vehicle Number").strip()
            home_location = st.text_input("Enter Your Current City (to be set as your base city)").strip()
            given_otp = st.text_input("Enter The OTP!", key="driver_signup_otp").strip()

            # Sign Up Action Section
            if st.button(":orange[Sign Up]"):
                if not new_full_name or not new_username or not new_password or not confirm_password or not dob or not new_email or not phone_number or not dl_number or not vehicle_type or not vehicle_number or not given_otp:
                    st.error("Please fill in all fields.")
                else:
                    # Check if the username already exists
                    user_exists = dm.verify_user(db_file_driver, new_username, new_password, st.session_state.selected_mode)
                    user_fullname_exists = dm.verify_fullname(db_file_driver, new_full_name, st.session_state.selected_mode)
                    user_phone_exists = dm.verify_phone_number(db_file_driver, phone_number, st.session_state.selected_mode)
                    user_email_exists = dm.verify_email(db_file_driver, new_email, st.session_state.selected_mode)
                    if user_exists:
                        st.error("Username already exists. Please choose another one.")
                    elif user_fullname_exists:
                        st.error("User already registered!!!")
                    elif user_email_exists:
                        st.error("Email already registered!!!")
                    elif user_phone_exists:
                        st.error("Phone number already registered!!!")
                    else:
                        # Check if the OTP is correct
                        if given_otp == st.session_state.generated_otp and st.session_state.paswd_matched:
                            st.success("OTP Matched!")
                            state = 1
                            while state == 1:
                                driver_id = fm.driverid()
                                if not dm.verify_driver_id(db_file_driver, driver_id):
                                    state = 0
                            # Store user data in the database
                            dm.insert_driver(db_file_driver, driver_id, new_full_name, new_username, new_password, dob, new_email, phone_number, dl_number, vehicle_type, vehicle_number)
                            dm.insert_driver_history(db_history_driver, driver_id, new_full_name, new_username)
                            dm.insert_book_cab(db_book_data, driver_id, new_username, home_location)
                            st.success(f"Account created successfully. Your driver id is {driver_id}")
                            message = f"Your driver id is {driver_id}"
                            with st.status("Sending Driver Id...") as status:
                                if fm.send_email(new_email, message, "Driver"):
                                    status.update(label="Driver Id sent on mail.", state="complete")
                                else:
                                    st.error("Can't send Driver Id!!!")
                            st.session_state.otp_flag = False
                            st.session_state.paswd_matched = False
                            st.session_state.signlog_selected_mode = "Log In"
                        elif given_otp != st.session_state.generated_otp:
                            st.error("OTP Mismatch!!")
                            st.session_state.otp_flag = False

            # creating the back option
            if st.button(":red[Back]", key="signup_page_driver"):
                st.session_state.signlog_selected_mode = None
                st.session_state.signlog_mode_selected = False

        # Handle log in mode selection & Authentication For Driver
        if st.session_state.signlog_mode_selected and st.session_state.signlog_selected_mode == "Log In":
            st.subheader(":green[Driver Log In]")

            #Log In
            username = st.text_input("Username/Driver Id", key="driver_login_username").strip()
            password = st.text_input("Password", type="password", key="driver_login_password").strip()

            logcol1, logcol2 = st.columns(2)
            #col for login
            with logcol1:
                if st.button(":green[Log In]"):
                    if not username or not password:
                        st.error("Please enter both username and password.")
                    else:
                        # Verify user credentials from the database
                        authenticated1 = dm.verify_user(db_file_driver, username, password, st.session_state.selected_mode)
                        authenticated2 = dm.verify_user_driverid(db_file_driver, username, password)
                        if authenticated1 or authenticated2:
                            st.session_state.authenticated = True
                            st.session_state.username = authenticated1 or authenticated2
                            st.session_state.full_name = dm.fullname_driver(db_file_driver, st.session_state.username)
                            st.success(f"Welcome, {authenticated1 or authenticated2}!")
                        else:
                            st.error("Authentication failed.")
            with logcol2:
                if st.button(":red[Forget Password]"):
                    st.session_state.signlog_selected_mode = "FrgtPswd"

            # creating the back option
            if st.button(":red[Back]", key="login_page_driver"):
                st.session_state.signlog_selected_mode = None
                st.session_state.signlog_mode_selected = False

        # Handle forget password mode selection & Authentication For Driver
        if st.session_state.signlog_mode_selected and st.session_state.signlog_selected_mode == "FrgtPswd":
            st.subheader(":red[Forget Password]")
            username = st.text_input("Username/Driver Id", key="driver_login_username_forgetpswd").strip()
            email = st.text_input("Email", key="driver_forgetpswd_email").strip()
            if dm.verify_user_forgetpswd(db_file_driver, username, email):
                if not st.session_state.otp_flag:
                    # sent OTP to email
                    generated_otp = fm.generate_otp()
                    st.session_state.generated_otp = generated_otp
                    st.session_state.otp_flag = True
                    message = f"Your OTP for CabOnTheGo is {generated_otp}"
                    with st.status("Sending OTP...") as status:
                        if fm.send_email(email, message, "OTP"):
                            status.update(label="OTP Sent Successfully!! Check mail.", state="complete", expanded=False)
                        else:
                            status.update(label="Can't send OTP!!!", state="error")
                given_otp = st.text_input("Enter The OTP!", key="driver_forgetpswd_otp").strip()
                #match the otps
                if given_otp == st.session_state.generated_otp:
                    st.success("OTP Matched!")
                    new_password = st.text_input("New Password", type="password", key="driver_frogetpswd_password").strip()
                    confirm_password = st.text_input("Confirm Password", type="password", key="driver_forgetpswd_cnfrmpassword")
                    if new_password and confirm_password:
                        if new_password != confirm_password:
                            st.warning("Passwords don't match!!!")
                        elif new_password == confirm_password:
                            st.success("Passwords matched!")
                            st.session_state.paswd_matched = True
                    if st.button("Submit"):
                        if st.session_state.paswd_matched:
                            if dm.change_password_driver(db_file_driver, username, new_password):
                                st.success("Password Changed Successfully!!")
                                st.session_state.otp_flag = False
                                st.session_state.paswd_matched = False
                                st.session_state.signlog_selected_mode = "Log In"
                            else:
                                st.error("Password Changing Failed!!!")
                                st.session_state.otp_flag = False
                                st.session_state.signlog_selected_mode = "Log In"
                elif given_otp and given_otp != st.session_state.generated_otp:
                    st.error("OTP Mismatch!!")
                    st.session_state.otp_flag = False
            elif email and not dm.verify_user_forgetpswd(db_file_driver, username, email):
                st.error("Username & Email are incorrect!!!")

            # creating the back option
            if st.button(":red[Back]", key="frgtpswd_page_driver"):
                st.session_state.signlog_selected_mode = None
                st.session_state.signlog_mode_selected = False

    #Handle Mode Selection For Rider
    if st.session_state.mode_selected and st.session_state.selected_mode == "Rider":
        st.header(f":green[{st.session_state.selected_mode} Authentication]")

        # Check if a sign up/log in mode is already selected
        if not st.session_state.signlog_mode_selected:
            col1, col2, col3 = st.columns(3, gap="medium")  # Create two columns
            # Sign Up Mode button in the first column
            with col1:
                if st.button(":orange[Sign Up]", key='rider_signup_button', use_container_width=True):
                    st.session_state.signlog_mode_selected = True
                    st.session_state.signlog_selected_mode = "Sign Up"

            # Rider Mode button in the second column
            with col2:
                if st.button(":green[Log In]", key='rider_login_button', use_container_width=True):
                    st.session_state.signlog_mode_selected = True
                    st.session_state.signlog_selected_mode = "Log In"

            # Forget Password Mode button in the third column
            with col3:
                if st.button(":red[Forget Password]", key='rider_frgtpswd_button', use_container_width=True):
                    st.session_state.signlog_mode_selected = True
                    st.session_state.signlog_selected_mode = "FrgtPswd"

            #creating the back option
            if st.button(":red[Back]", key="mode_selection_rider"):
                st.session_state.selected_mode = None
                st.session_state.mode_selected = False

        # Handle sign up mode selection & Authentication For Rider
        if st.session_state.signlog_mode_selected and st.session_state.signlog_selected_mode == "Sign Up":
            st.subheader(":orange[Rider Sign Up]")

            # Sign-up
            #Sign Up Details Section
            new_full_name = st.text_input("Full Name").strip()
            new_username = st.text_input("Username", key="rider_signup_username").strip()
            new_password = st.text_input("Password", type="password", key="rider_signup_password").strip()
            confirm_password = st.text_input("Confirm Password", type="password").strip()
            #check for matching of password & confirm password
            if new_password and confirm_password:
                if new_password != confirm_password:
                    st.warning("Passwords don't match!!!")
                elif new_password == confirm_password:
                    st.success("Passwords matched!")
                    st.session_state.paswd_matched = True
            dob = st.date_input("Date of Birth", format="DD/MM/YYYY", min_value=datetime(1900, 1, 1))
            #Check for valid age
            if fm.agecalc(dob) < 18:
                st.warning("The user must be 18 years of age!!")
            new_email = st.text_input("Email").strip()
            #check for a valid email
            if new_email and not fm.is_valid_email(new_email):
                st.warning("Enter a valid email!!!")
            if new_email and fm.is_valid_email(new_email) and not st.session_state.otp_flag:
                # sent OTP to email
                generated_otp = fm.generate_otp()
                st.session_state.generated_otp = generated_otp
                st.session_state.otp_flag = True
                message = f"Your OTP for CabOnTheGo is {generated_otp}"
                with st.status("Sending OTP...") as status:
                    if fm.send_email(new_email, message, "OTP"):
                        status.update(label="OTP Sent Successfully!! Check mail.", state="complete", expanded=True)
                    else:
                        status.update(label="Can't send OTP!!!", state="error")
            phone_number = st.text_input("Phone Number").strip()
            #check for a valid phone number
            if phone_number:
                if len(phone_number) != 10 or not phone_number.isdigit():
                    st.warning("Enter valid phone number!!!")
            given_otp = st.text_input("Enter The OTP!").strip()

            #Sign Up Action Section
            if st.button(":orange[Sign Up]"):
                if not new_full_name or not new_username or not new_password or not confirm_password or not dob or not new_email or not phone_number or not given_otp:
                    st.error("Please fill in all fields.")
                else:
                    # Check if the username already exists
                    user_exists = dm.verify_user(db_file_rider, new_username, new_password, st.session_state.selected_mode)
                    user_fullname_exists = dm.verify_fullname(db_file_rider, new_full_name, st.session_state.selected_mode)
                    user_phone_exists = dm.verify_phone_number(db_file_rider, phone_number, st.session_state.selected_mode)
                    user_email_exists = dm.verify_email(db_file_rider, new_email, st.session_state.selected_mode)
                    if user_exists:
                        st.error("Username already exists. Please choose another one.")
                    elif user_fullname_exists:
                        st.error("User already registered!!!")
                    elif user_email_exists:
                        st.error("Email already registered!!!")
                    elif user_phone_exists:
                        st.error("Phone number already registered!!!")
                    else:
                        #Check if the OTP is correct
                        if given_otp == st.session_state.generated_otp and st.session_state.paswd_matched:
                            st.success("OTP Matched!")
                            # Store user data in the database
                            dm.insert_rider(db_file_rider, new_full_name, new_username, new_password, dob, new_email, phone_number)
                            dm.insert_rider_history(db_history_rider, new_full_name, new_username)
                            st.success("Account created successfully. You can now log in.")
                            st.session_state.otp_flag = False
                            st.session_state.paswd_matched = False
                            st.session_state.signlog_selected_mode = "Log In"
                        elif given_otp != st.session_state.generated_otp:
                            st.error("OTP Mismatch!!")
                            st.session_state.otp_flag = False

            # creating the back option
            if st.button(":red[Back]", key="signup_page_rider"):
                st.session_state.signlog_selected_mode = None
                st.session_state.signlog_mode_selected = False

        # Handle log in mode selection & Authentication For Rider
        if st.session_state.signlog_mode_selected and st.session_state.signlog_selected_mode == "Log In":
            st.subheader(":green[Rider Log In]")

            #Log In
            username = st.text_input("Username", key="rider_login_username").strip()
            password = st.text_input("Password", type="password", key="rider_login_password").strip()

            logcol1, logcol2 = st.columns(2)
            with logcol1:
                if st.button(":green[Log In]"):
                    if not username or not password:
                        st.error("Please enter both username and password.")
                    else:
                        # Verify user credentials from the database
                        authenticated = dm.verify_user(db_file_rider, username, password, st.session_state.selected_mode)
                        if authenticated:
                            st.session_state.authenticated = True
                            st.session_state.username = username
                            st.session_state.full_name = dm.fullname_rider(db_file_rider, st.session_state.username)
                            st.success(f"Welcome, {username}!")
                        else:
                            st.error("Authentication failed.")
            with logcol2:
                if st.button(":red[Forget Password]"):
                    st.session_state.signlog_selected_mode = "FrgtPswd"

            # creating the back option
            if st.button(":red[Back]", key="login_page_rider"):
                st.session_state.signlog_selected_mode = None
                st.session_state.signlog_mode_selected = False

        # Handle forget password mode selection & Authentication For rider
        if st.session_state.signlog_mode_selected and st.session_state.signlog_selected_mode == "FrgtPswd":
            st.subheader(":red[Forget Password]")
            username = st.text_input("Username", key="rider_login_username_forgetpswd").strip()
            email = st.text_input("Email", key="rider_forgetpswd_email").strip()
            if dm.verify_user_rider_forgetpswd(db_file_rider, username, email):
                if not st.session_state.otp_flag:
                    # sent OTP to email
                    generated_otp = fm.generate_otp()
                    st.session_state.generated_otp = generated_otp
                    st.session_state.otp_flag = True
                    message = f"Your OTP for CabOnTheGo is {generated_otp}"
                    with st.status("Sending OTP...") as status:
                        if fm.send_email(email, message, "OTP"):
                            status.update(label="OTP Sent Successfully!! Check mail.", state="complete", expanded=True)
                        else:
                            status.update(label="Can't send OTP!!!", state="error")
                given_otp = st.text_input("Enter The OTP!", key="rider_forgetpswd_otp").strip()
                # match the otps
                if given_otp == st.session_state.generated_otp:
                    st.success("OTP Matched!")
                    new_password = st.text_input("New Password", type="password", key="rider_frogetpswd_password").strip()
                    confirm_password = st.text_input("Confirm Password", type="password", key="rider_forgetpswd_cnfrmpassword").strip()
                    if new_password and confirm_password:
                        if new_password != confirm_password:
                            st.warning("Passwords don't match!!!")
                        elif new_password == confirm_password:
                            st.success("Passwords matched!")
                            st.session_state.paswd_matched = True
                    if st.button("Submit"):
                        if st.session_state.paswd_matched:
                            if dm.change_password_rider(db_file_rider, username, new_password):
                                st.success("Password Changed Successfully!!")
                                st.session_state.otp_flag = False
                                st.session_state.paswd_matched = False
                                st.session_state.signlog_selected_mode = "Log In"
                            else:
                                st.error("Password Changing Failed!!!")
                                st.session_state.otp_flag = False
                                st.session_state.signlog_selected_mode = "Log In"
                elif given_otp and given_otp != st.session_state.generated_otp:
                    st.error("OTP Mismatch!!")
                    st.session_state.otp_flag = False
            elif email and not dm.verify_user_forgetpswd(db_file_rider, username, email):
                st.error("Username & Email are incorrect!!!")

            # creating the back option
            if st.button(":red[Back]", key="frgtpswd_page_rider"):
                st.session_state.signlog_selected_mode = None
                st.session_state.signlog_mode_selected = False

# Dashboard section (separate page)
if st.session_state.authenticated:
    #options for driver
    if st.session_state.selected_mode == "Driver":
        display_dashboard(st.session_state.full_name, st.session_state.selected_mode)
        with st.expander("Menu Options"):
            # Create tabs for menu navigation
            tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs(["Accept/Reject Rides", "Real-Time Tracking", "Booking History",
                "Rating & Feedback", "Safety & Security", "Earnings & Payment", "Account Details Edit", "Availability Status", "Performance Matrices", "Language Selection","Ride Cancellation"])
            with tab1:
                display_orders(st.session_state.username)
            with tab7:
                details_edit(st.session_state.full_name, st.session_state.selected_mode)


    #options for rider
    if st.session_state.selected_mode == "Rider":
        display_dashboard(st.session_state.full_name, st.session_state.selected_mode)
        with st.expander("Menu Options"):
            #creating tabs for each menu operations
            tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(["Cab Booking", "Real-Time Tracking", "Booking History",
                "Rating & Feedback", "Safety & Security", "Account Details Edit", "Help Centre", "Language Selection", "Ride Cancellation"])
            with tab1:
                display_book_cab(st.session_state.full_name)
            with tab6:
                details_edit(st.session_state.full_name, st.session_state.selected_mode)

    # defining log out button
    if st.button("Log Out", type="primary"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.full_name = None
        st.session_state.otp_flag = False
        st.session_state.generated_otp = None
        st.session_state.mode_selected = False
        st.session_state.selected_mode = None
        st.session_state.signlog_mode_selected = False
        st.session_state.signlog_selected_mode = None



