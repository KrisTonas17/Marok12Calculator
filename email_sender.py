import streamlit as st
import json
from datetime import datetime

def send_contact_email(name, district, email):
    """
    Handle contact form information to Kris at Maro
    
    Parameters:
    -----------
    name : str
        Contact person's name
    district : str
        School district name
    email : str
        Contact person's email address
    
    Returns:
    --------
    bool
        True if email was processed successfully, False otherwise
    """
    try:
        # For Streamlit Cloud deployment, we'll log and store contact info
        contact_info = {
            "name": name,
            "district": district,
            "email": email,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # In a real deployment, you would use Streamlit Secrets to configure email
        # https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management
        
        # Option 1: Save to session state for demo purposes
        if "contacts" not in st.session_state:
            st.session_state.contacts = []
        
        st.session_state.contacts.append(contact_info)
        
        # Option 2: In a real deployment with email configured:
        # if "email" in st.secrets:
        #     # Send email using configured SMTP settings from secrets.toml
        #     # recipient_email = "kris@meetmaro.com"
        #     # Code for sending email would go here using st.secrets["email"]["username"], etc.
        #     pass
            
        print(f"Contact request saved: {name} from {district}, Email: {email}")
        return True
        
    except Exception as e:
        print(f"Error processing contact: {e}")
        return False