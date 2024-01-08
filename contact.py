import streamlit as st
import mysql.connector
# Establish connection to your local MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Enter your MySQL password here
    database="ids"
)
cursor = conn.cursor()
# Function to create the table
def create_form_submissions_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS form_submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    """)
    conn.commit()
create_form_submissions_table()
def cont():
    st.header("Get in touch with me!")
    # Define form inputs
    form_name = st.text_input("Your name")
    form_email = st.text_input("Your email")
    form_message = st.text_area("Your message here")
    submit_button = st.button("Send")
    if submit_button:
        # Insert form data into the database
        query = "INSERT INTO form_submissions (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(query, (form_name, form_email, form_message))
        conn.commit()
        # Display a link to navigate back to the home page
        st.success("Form submitted successfully!")
        st.balloons()