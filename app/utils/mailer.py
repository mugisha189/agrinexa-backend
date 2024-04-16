from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from typing import List
from decouple import config
import os



conf = ConnectionConfig(
    MAIL_USERNAME=config("MAIL_USERNAME"),
    MAIL_PASSWORD=config("MAIL_PASSWORD"),
    MAIL_FROM=config("MAIL_FROM"),
    MAIL_PORT=config("MAIL_PORT"),
    MAIL_SERVER=config("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

fast_mail = FastMail(conf)


async def send_email(recipients: List[EmailStr], subject: str, body: str, template=None):
    if template:
        body = template
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype="html"
    )
    print(message)
    try:
        await fast_mail.send_message(message)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to send email. Please try again later.")
