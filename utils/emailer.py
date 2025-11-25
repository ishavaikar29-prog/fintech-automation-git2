import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from utils.error_handler import log_info, log_error, attachable_log_exists

logger = logging.getLogger(__name__)

def build_email_body(cnts):
    body = (
        "Hello,\n\n"
        "Automated multi-API report.\n\n"
    )
    body += "\n".join([f"{k}: {v}" for k, v in cnts.items()]) + "\n\n"
    return body

def send_email_with_attachments(smtp_host, smtp_port, smtp_user, smtp_pass, to_email, subject, body, attachments):
    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    for fpath in attachments:
        if not os.path.exists(fpath):
            continue
        part = MIMEBase("application", "octet-stream")
        with open(fpath, "rb") as f:
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(fpath)}"')
        msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        log_info("Email sent successfully")
    except Exception as e:
        log_error("EMAIL SEND FAILED", e)
        raise
