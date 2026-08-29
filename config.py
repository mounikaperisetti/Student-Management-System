# It is a abstraction layer of .env

from dotenv import load_dotenv
import os

load_dotenv()

class Config():
    db_host = os.getenv('DB_HOST')   # here db_host is a member varibale
    db_port = os.getenv('DB_PORT')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME') 
    from_email = os.getenv('FROM_EMAIL')
    email_app_password = os.getenv('EMAIL_APP_PASSWORD')

class emailTemplates():

    def send_otp_template(username:str, otp:int):  # here we are mentiontioning cls because if incase we want to use class attributes in future.
        template =  f"""
            Hello {username},
            Welcome to Student Notes System!
            Thank you for registering with us.
            Your OTP for email verification is:
            Your OTP: {otp}
            This OTP is valid for  10 minutes.
            Please do not share this OTP with anyone.

            If you did not create an account with Student Notes System,
            please ignore this email.

            Regards,
            SNS Team
            """
        return template

    def send_reset_password_template(username:str, url:str,time:int):

        template = f"""
                Hello {username},

                We received a request to reset the password for your
                Student Notes System account.

                Click the link below to reset your password:

                reset URL: {url}

                This password reset link is valid for {time} minutes.

                If you did not request a password reset, please ignore this email.

                Regards,
                SNS Team
                """

        return template