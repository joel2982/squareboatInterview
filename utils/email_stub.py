import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
import asyncio

MAIL_USERNAME=os.getenv("MAIL_USERNAME")
MAIL_PASSWORD=os.getenv("MAIL_PASSWORD")
MAIL_FROM=os.getenv("MAIL_FROM")
MAIL_PORT=int(os.getenv("MAIL_PORT", 587))
MAIL_SERVER=os.getenv("MAIL_SERVER")
MAIL_TLS=os.getenv("MAIL_TLS", "True")
MAIL_SSL=os.getenv("MAIL_SSL", "False")
USE_CREDENTIALS=os.getenv("USE_CREDENTIALS", "True")

def send_email_stub(to_email: str, subject: str, body: str):
    conf = ConnectionConfig(
        MAIL_USERNAME=MAIL_USERNAME,
        MAIL_PASSWORD=MAIL_PASSWORD,
        MAIL_FROM=MAIL_FROM,
        MAIL_PORT=MAIL_PORT,
        MAIL_SERVER=MAIL_SERVER,
        MAIL_TLS=MAIL_TLS,
        MAIL_SSL=MAIL_SSL,
        USE_CREDENTIALS=USE_CREDENTIALS
    )

    message = MessageSchema(
        subject=subject,
        recipients=[EmailStr(to_email)],
        body=body,
        subtype="plain"
    )

    fm = FastMail(conf)
    asyncio.run(fm.send_message(message))
    print(f"Sending email to {to_email}: {subject}\n{body}")
