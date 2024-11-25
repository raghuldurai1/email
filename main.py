import cohere
import smtplib
import streamlit as st
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Hardcoded credentials for local testing
EMAIL_ADDRESS = "raghuldurai300@gmail.com"
EMAIL_PASSWORD = "ggqn sctj zjxf nzto"
COHERE_API_KEY = "o4SMHvCR9cSvNRtc2f8QtL6uEqXWfAo5mnNVF6Gn"

# Initialize the Cohere client
cohere_client = cohere.Client(COHERE_API_KEY)

# Function to generate text based on a prompt using Cohere
def generate_text(prompt):
    try:
        response = cohere_client.generate(
            prompt=prompt,
            max_tokens=300
        )
        return response.generations[0].text
    except Exception as e:
        st.error(f"Error generating text: {e}")
        return "Error generating text."

# Function to validate email
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

# Function to send an email
def send_email(to_email, subject, body):
    from_email = EMAIL_ADDRESS
    from_password = EMAIL_PASSWORD

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, msg.as_string())
        st.success(f"Email sent to {to_email} successfully.")
    except Exception as e:
        st.error(f"Failed to send email. Error: {e}")

# Streamlit application
def main():
    st.title("General Text Generator and Email Sender")

    # Step 1: Text Generation
    prompt = st.text_area("Enter your prompt:")
    if st.button("Generate Text"):
        if prompt:
            generated_text = generate_text(prompt)
            st.session_state['generated_text'] = generated_text
            st.subheader("Generated Text:")
            st.write(generated_text)
        else:
            st.error("Please enter a prompt.")

    # Step 2: Edit and Send Email
    if 'generated_text' in st.session_state:
        st.subheader("Edit Generated Text")
        # Make the text area larger for editing
        edited_text = st.text_area("Edit the generated text:", st.session_state['generated_text'], height=300)

        st.subheader("Email Details")
        recipient_email = st.text_input("Recipient's Email Address:")
        email_subject = st.text_input("Email Subject:")

        if st.button("Send Email"):
            if recipient_email and email_subject:
                if is_valid_email(recipient_email):
                    send_email(recipient_email, email_subject, edited_text)
                else:
                    st.error("Please enter a valid email address.")
            else:
                st.error("Please fill in all fields.")

if __name__ == "__main__":
    main()
