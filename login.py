import streamlit as st
import mysql.connector
from PIL import Image
from io import BytesIO
import uuid

# Establish connection to your local MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ids"
)
mycursor = mydb.cursor()

def create_session_id():
    return str(uuid.uuid4())

# Check if session exists and return session ID
def get_session_id():
    if 'session_id' not in st.session_state:
        st.session_state.session_id = create_session_id()
    return st.session_state.session_id

def creation():
    def create_user_table():
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS ACCOUNT (
                email VARCHAR(255) PRIMARY KEY,
                password VARCHAR(255) NOT NULL,
                username VARCHAR(255) NOT NULL UNIQUE,
                name VARCHAR(255) NOT NULL,
                phone VARCHAR(25) NOT NULL,
                profile_picture LONGBLOB
            )
        """)
        mydb.commit()

    create_user_table()
    img_login = Image.open("images/bg.jpg").resize((300, 300))

    def display_profile_picture(profile_pic):
        try:
            if profile_pic:
                image = Image.open(BytesIO(profile_pic))
                image = image.resize((300, 300))
                st.image(image)
            else:
                st.image(img_login)
        except Exception as e:
            st.error(f"Error loading profile picture: {e}")

    def user_authentication():
        st.title("User Authentication")
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False

        if not st.session_state.logged_in:
            choice = st.selectbox("Login/Signup", ["Login", "Register"])
            if choice == "Login":
                # Login Section
                st.subheader("Login Section")
                email = st.text_input("Email")
                password = st.text_input("Password", type='password')

                if st.button("Login"):
                    try:
                        query = "SELECT * FROM ACCOUNT WHERE email = %s"
                        values = (email,)
                        mycursor.execute(query, values)
                        user = mycursor.fetchone()

                        if user:
                            if user[1] == password:  # Check if fetched password matches input password
                                st.success("Login successful")
                                st.session_state.username = user[2]  # Assuming username is at index 3
                                st.session_state.useremail = user[0]  # Assuming email is at index 1
                                st.session_state.logged_in = True
                                profile_pic = user[5]
                                display_profile_picture(profile_pic)
                            else:
                                st.warning("Login failed. Incorrect password.")
                        else:
                            st.warning("Login failed. Incorrect email.")
                    except Exception as e:
                        st.error(f"Error: {e}")

            else:
                # Create New Account Section
                st.subheader("Create New Account")
                new_email = st.text_input("Email")
                new_password = st.text_input("Password", type='password')
                new_username = st.text_input("Unique Username")
                new_name = st.text_input("Full Name")
                new_phone = st.text_input("Phone Number")
                new_profile_pic = st.file_uploader("Upload Profile Picture", type=['jpg', 'png', 'jpeg'])

                if st.button("Register"):
                    mycursor.execute(f"SELECT * FROM ACCOUNT WHERE username='{new_username}'")
                    existing_user = mycursor.fetchone()
                    if existing_user:
                        st.warning("Username already exists! Try a different one.")
                    else:
                        try:
                            query = "INSERT INTO ACCOUNT (email, password, username, name, phone, profile_picture) VALUES (%s, %s, %s, %s, %s, %s)"
                            values = (new_email, new_password, new_username, new_name, new_phone,
                                      new_profile_pic.read() if new_profile_pic else None)
                            mycursor.execute(query, values)
                            mydb.commit()
                            st.success('Account created successfully!')
                            st.balloons()
                            st.markdown("Login using your email and password")
                        except Exception as e:
                            st.warning("Account creation failed.")
                            st.error(f"Error: {e}")

    # Run the authentication function
    user_authentication()

def ma():
    creation()  # Run creation function

    if st.session_state.logged_in:
        # Display logged-in user's information
        st.write("User is logged in.")
        # Add the content you want to display for logged-in users here
        st.subheader(f"Welcome, {st.session_state.username}")
        st.write(f"Email: {st.session_state.useremail}")

        # Add a logout button
        if st.button("Logout"):
            st.session_state.logged_in = False
            # Clear session on logout
            if 'username' in st.session_state:
                del st.session_state.username
            if 'useremail' in st.session_state:
                del st.session_state.useremail
            st.write("Logged out successfully.")
