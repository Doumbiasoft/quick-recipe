import smtplib
import ssl
import logging
from email.message import EmailMessage
from config import Config

app_config=Config

logger = logging.getLogger(__name__)


def Send_Email(recipient:str,subject:str,message:str,content_type:str="html"):

    msg = EmailMessage()
    msg['From'] = app_config.MAIL_DEFAULT_SENDER
    msg['To'] = recipient
    msg['Subject'] = subject
    if content_type =='html':
        msg.set_content(message, subtype="html")
    if content_type =='text':
         msg.set_content(message)

    try:
        if str(app_config.MAIL_PORT) == str(465):
            # Add SSL (layer of security)
            context = ssl.create_default_context()
            # Log in and send the email
            with smtplib.SMTP_SSL(app_config.MAIL_SMTP, app_config.MAIL_PORT, context=context, timeout=10) as smtp:
                smtp.login(app_config.MAIL_USERNAME, app_config.MAIL_PASSWORD)
                data = smtp.sendmail(app_config.MAIL_USERNAME, recipient, msg.as_string())

        elif str(app_config.MAIL_PORT) == str(587):
            with smtplib.SMTP(app_config.MAIL_SMTP, app_config.MAIL_PORT, timeout=10) as smtp:
                smtp.starttls()
                smtp.login(app_config.MAIL_USERNAME, app_config.MAIL_PASSWORD)
                data = smtp.sendmail(app_config.MAIL_USERNAME, recipient, msg.as_string())
        else:
            logger.error(f"Unsupported MAIL_PORT: {app_config.MAIL_PORT}. Must be 465 or 587.")
            raise ValueError(f"Unsupported MAIL_PORT: {app_config.MAIL_PORT}")

        logger.info(f"Email sent successfully to {recipient} | subject: '{subject}'")
        return data

    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP authentication failed for {recipient} | subject: '{subject}' | error: {e}")
        raise
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error while sending to {recipient} | subject: '{subject}' | error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while sending email to {recipient} | subject: '{subject}' | error: {e}")
        raise
