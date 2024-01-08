import numpy as np
import pandas as pd
import pickle
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
import smtplib
from email.mime.text import MIMEText
import datetime
import socket
import uuid

def preprocess_and_predict(model, new_data):
    new_data_clean = new_data.replace([np.inf, -np.inf], np.nan).dropna()
    new_data_clean = new_data_clean.dropna()

    scaler = MinMaxScaler()
    imputer = SimpleImputer(strategy='mean')

    # Fit the imputer and scaler to the data
    imputed_data = imputer.fit_transform(new_data_clean)
    scaler.fit(imputed_data)  # Fit scaler to the imputed data
    X_new_selected_scaled = scaler.transform(imputed_data)

    y_pred_new = model.predict(X_new_selected_scaled)
    return y_pred_new


def testing_csv():
    st.subheader(' IDS Prediction Model')
    # loading the saved model
    loaded_model = pickle.load(open('_14_model.sav', 'rb'))
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        new_data = pd.read_csv(uploaded_file)
        predictions = preprocess_and_predict(loaded_model, new_data)
        st.write(predictions)
        if predictions[0] == 1:
            pass
        else:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Get the hostname
            system_name = socket.gethostname()
            # Get the IP address
            ip_address = socket.gethostbyname(system_name)

            # Get the MAC address
            mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 2)][::-1])
            subject = "Urgent: Network Intrusion Detected - Immediate Investigation Required"
            body = f"""
            Dear IT Support Team,

            I hope this message finds you well. We have received an alert indicating a potential intrusion on our network. Immediate investigation and action are required to ensure the security and integrity of our systems.

            Details of the incident:

            Time of detection: {current_time}
            Systems affected: 
                System Name: {system_name}
                IP Address: {ip_address}
                MAC Address: {mac_address}
            We urgently need your expertise to:
            1. Investigate the detected intrusion to determine its scope and potential impact.
            2. Isolate and contain the affected systems or areas of the network to prevent further compromise.
            3. Implement necessary security measures or patches to mitigate vulnerabilities exploited in this intrusion.
            4. Conduct a thorough review of our network security protocols and systems to identify potential weak points.

            Please acknowledge this message and prioritize this issue. Time is of the essence in safeguarding our network and sensitive information. If you require any further information or assistance, please do not hesitate to contact me.

            Thank you for your immediate attention and swift action in addressing this critical matter.

            Best regards,

            [DINESH M]
            [FINAL YEAR IT]
            [dineshmoorthi27@gmail.com, 9789453361]
            """
            sender = "dineshmoorthi27@gmail.com"
            recipients = ["projecttestingfyp@gmail.com"]
            password = "wtai ayeq zfwa tiwr"

            def send_email(subject, body, sender, recipients, password):
                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = sender
                msg['To'] = ', '.join(recipients)
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                    smtp_server.login(sender, password)
                    smtp_server.sendmail(sender, recipients, msg.as_string())
                st.write("Message Alert sent successfully!")

            send_email(subject, body, sender, recipients, password)

