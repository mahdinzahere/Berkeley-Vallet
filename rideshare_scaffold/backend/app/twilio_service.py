from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from .config import settings
import logging

logger = logging.getLogger(__name__)

class TwilioService:
    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.phone_number = settings.TWILIO_PHONE_NUMBER
        self.client = None
        
        if self.account_sid and self.auth_token:
            try:
                self.client = Client(self.account_sid, self.auth_token)
                logger.info("Twilio client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Twilio client: {e}")
    
    def send_sms(self, to_phone: str, message: str) -> bool:
        """Send SMS message"""
        if not self.client:
            logger.error("Twilio client not initialized")
            return False
        
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.phone_number,
                to=to_phone
            )
            logger.info(f"SMS sent successfully to {to_phone}: {message.sid}")
            return True
        except TwilioException as e:
            logger.error(f"Failed to send SMS to {to_phone}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending SMS to {to_phone}: {e}")
            return False
    
    def send_verification_code(self, phone: str, code: str) -> bool:
        """Send verification code via SMS"""
        message = f"Your Valey verification code is: {code}. This code expires in 10 minutes."
        return self.send_sms(phone, message)
    
    def send_ride_confirmation(self, phone: str, driver_name: str, driver_phone: str, eta: str) -> bool:
        """Send ride confirmation SMS"""
        message = f"Your Valey ride is confirmed! Driver: {driver_name} ({driver_phone}). ETA: {eta}"
        return self.send_sms(phone, message)
    
    def send_ride_update(self, phone: str, status: str, details: str = "") -> bool:
        """Send ride status update SMS"""
        message = f"Valey ride update: {status}"
        if details:
            message += f" - {details}"
        return self.send_sms(phone, message)
    
    def send_driver_alert(self, phone: str, pickup_address: str, fare: float) -> bool:
        """Send new ride request alert to driver"""
        message = f"New Valey ride request! Pickup: {pickup_address}. Fare: ${fare:.2f}"
        return self.send_sms(phone, message)

# Global instance
twilio_service = TwilioService()
