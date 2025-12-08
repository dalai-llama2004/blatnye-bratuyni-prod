import httpx
import os

NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://notification-service:8003")

async def send_email_notification(email: str, subject: str, text: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{NOTIFICATION_SERVICE_URL}/notify/email",
            json={
                "email": email,
                "subject": subject,
                "text": text,
            }
        )