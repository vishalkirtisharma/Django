import smtplib


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'vishalkirtisharma@gmail.com'
EMAIL_HOST_PASSWORD = 'txuhxpoplrkoxkwg'  # This should be your 16-character App Password
       # Replace with your App Password

# EMAIL_HOST = 'smtp.mail.yahoo.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'vishalkirtisharma@yahoo.com'  # Replace with your Yahoo email
# EMAIL_HOST_PASSWORD = 'wrytegoaocudfrwg' 

try:
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.ehlo()
    server.starttls()  # Enable TLS
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    print("✅ Login successful! Email and password are correct.")
    server.quit()
except smtplib.SMTPAuthenticationError:
    print("❌ Login failed! Check your email or password (App Password needed).")
except Exception as e:
    print(f"❌ An error occurred: {e}")
