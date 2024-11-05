import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

def send_email_notification(name, email, user_type):
    """
    Sends an email notification after recognizing a face and marking attendance.
    
    :param name: Name of the person whose face was recognized
    :param email: Email address to which the notification will be sent
    :param user_type: 'Student' or 'Teacher' to customize the message
    """
    # Your Gmail credentials (replace with actual credentials)
    gmail_user = 'your_email@gmail.com'
    gmail_password = 'your_password_or_app_password'
    
    # Create the email content
    subject = f"{user_type} Attendance Notification"
    body = f"""
    Dear {name},

    This is to notify you that your attendance has been successfully marked.

    Date: {datetime.now().strftime('%Y-%m-%d')}
    Time: {datetime.now().strftime('%H:%M:%S')}

    Best regards,
    Face Recognition Attendance System
    """

    # Setting up the MIME structure for the email
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = email
    msg['Subject'] = subject

    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Establish connection to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(gmail_user, gmail_password)
        text = msg.as_string()
        
        # Send the email
        server.sendmail(gmail_user, email, text)
        print(f"Attendance notification email sent to {name} ({email})")
    except Exception as e:
        print(f"Failed to send email to {name} ({email}). Error: {str(e)}")
    finally:
        server.quit()

# Example usage after face recognition and marking attendance
def recognize_face_and_notify(details, user_type):
    """
    Simulates face recognition, marks attendance, and sends email notifications.
    
    :param details: Tuple containing (id, name, email)
    :param user_type: 'Student' or 'Teacher'
    """
    # Simulate attendance marking
    print(f"Attendance marked for {user_type}: {details[1]}")

    # Send email notification
    send_email_notification(details[1], details[2], user_type)

# Example details (id, name, email) of a student or teacher
student_details = (101, 'John Doe', 'caashish594@gmail.com')
teacher_details = (202, 'Jane Smith', 'chhetriaashish04@gmail.com')

# Simulate face recognition and send notification for both student and teacher
recognize_face_and_notify(student_details, "Student")
recognize_face_and_notify(teacher_details, "Teacher")
