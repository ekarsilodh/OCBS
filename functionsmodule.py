import streamlit as st
import random
import string
from email_validator import validate_email, EmailNotValidError
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from PIL import Image
import io
import requests

#function for log out
def log_out():
    st.session_state.username = None
    st.session_state.full_name = None
    st.session_state.authenticated = False
    st.session_state.otp_flag = False
    st.session_state.generated_otp = None
    st.session_state.mode_selected = False
    st.session_state.selected_mode = None
    st.session_state.signlog_mode_selected = False
    st.session_state.signlog_selected_mode = None

#Email Checker Function
def is_valid_email(email):
    try:
        # Validate the email address
        v = validate_email(email)
        return True
    except EmailNotValidError as e:
        return False

#Function to generate the OTP
def generate_otp():
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(6))
    return random_string

#Function to email OTP
def send_email(recipient_email, message, mode):
    try:
        # Set up the SMTP server
        smtp_server = 'smtp.gmail.com'  # Change this if using a different email provider
        smtp_port = 587  # Change this if using a different port
        sender_email = 'cabonthegoo@gmail.com'  # Your email address
        sender_password = 'jwmxdrigshwulotu'  # Your email password
        if mode == "OTP":
            subject = 'OTP for CabOnTheGo'
        elif mode == "Driver":
            subject = 'Driver Id for CabOnTheGo'

        # Create a message object
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach the message to the email
        # Create HTML-formatted message
        html_message = f'<html><body><p style="font-size: 16px; font-weight: bold;">{message}</p></body></html>'
        msg.attach(MIMEText(html_message, 'html'))

        # Create a SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

        # Return True if email sent successfully
        return True
    except Exception as e:
        # Print the error for debugging (optional)
        print(f"An error occurred: {e}")
        # Return False if there was an error sending the email
        return False

#Driver Id Generator
def driverid():
    random_number = random.randint(1000000000, 9999999999)
    return random_number

#Age Calculation
def agecalc(dob):
    # Get the current date
    current_date = datetime.now().date()
    # Calculate the age
    age = current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day))
    return age

#Age Calculation for dashboard
def agecalc_dashboard(dob):
    #convert the dob to datetime format
    birth_date = datetime.strptime(dob, '%Y-%m-%d')
    # Get the current date
    current_date = datetime.now().date()
    # Calculate the age
    age = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))
    return age

#function to get the dp
def fetchdp(image_binary):
    try:
        # Generating the profile pic
        image_bytes = io.BytesIO(image_binary)
        # Open the image using Pillow
        img = Image.open(image_bytes)
        return img
    except Exception as e:
        # Handle exceptions, e.g., if the binary data is not a valid image format
        return None

#function to calculate the distance
def distance_calculator(pickup, destination):
    url = "https://distanceto.p.rapidapi.com/get"

    # Define the query parameters as a dictionary
    query_params = {
        "route": f'[{{"t": "{pickup}" }}, {{"t": "{destination}"}}]',  # Define the route as a JSON string
    }

    headers = {
        "X-RapidAPI-Key": "f75c19832dmsh653241ab25b92fdp1915f8jsnbff0113f5a00",
        "X-RapidAPI-Host": "distanceto.p.rapidapi.com"
    }

    # Make the GET request with query parameters
    response = requests.get(url, headers=headers, params=query_params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()  # Parse the response as JSON
        # Handle the response data and find distance
        distance = round(data["steps"][0]["distance"]["haversine"], 2)
        return distance

#function to calculate fare
def fare_calculator(distance, num_passengers, cab_type):
    #create a dictionary for fare per km for each type of cabs
    fare_multiplier = {"Mini": 15, "Sedan": 20, "SUV": 25, "Bike": 11}

    #calculate the fare
    fare = distance * fare_multiplier[cab_type] + (num_passengers * 0.10)
    fare_rounded = round(fare, 0)
    return fare_rounded
