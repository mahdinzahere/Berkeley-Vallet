from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from .config import settings
import logging

logger = logging.getLogger(__name__)

class SendGridService:
    def __init__(self):
        self.api_key = settings.SENDGRID_API_KEY
        self.from_email = settings.SENDGRID_FROM_EMAIL
        self.client = None
        
        if self.api_key:
            try:
                self.client = SendGridAPIClient(api_key=self.api_key)
                logger.info("SendGrid client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize SendGrid client: {e}")
    
    def send_email(self, to_email: str, subject: str, content: str, content_type: str = "text/html") -> bool:
        """Send email via SendGrid"""
        if not self.client:
            logger.error("SendGrid client not initialized")
            return False
        
        try:
            from_email = Email(self.from_email)
            to_email = To(to_email)
            content = Content(content_type, content)
            
            mail = Mail(from_email, to_email, subject, content)
            response = self.client.send(mail)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email to {to_email}: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Unexpected error sending email to {to_email}: {e}")
            return False
    
    def send_welcome_email(self, email: str, name: str, role: str) -> bool:
        """Send welcome email to new user"""
        subject = "Welcome to Valey!"
        content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #1a0b2e; color: white; padding: 2rem; text-align: center;">
                <h1 style="color: #e6b3ff; margin: 0;">Welcome to Valey!</h1>
            </div>
            <div style="padding: 2rem; background: #f9f9f9;">
                <h2>Hi {name}!</h2>
                <p>Welcome to Valey, your trusted rideshare partner. We're excited to have you on board as a {role}!</p>
                
                <h3>What's next?</h3>
                <ul>
                    <li>Complete your profile setup</li>
                    <li>Verify your phone number</li>
                    <li>Start using Valey for safe, reliable transportation</li>
                </ul>
                
                <p>If you have any questions, feel free to reach out to our support team.</p>
                
                <div style="text-align: center; margin-top: 2rem;">
                    <a href="https://valey.com" style="background: #e6b3ff; color: #1a0b2e; padding: 1rem 2rem; text-decoration: none; border-radius: 5px; font-weight: bold;">Get Started</a>
                </div>
            </div>
            <div style="background: #0a0a0a; color: #ccc; padding: 1rem; text-align: center;">
                <p>&copy; 2024 Valey. All rights reserved.</p>
            </div>
        </body>
        </html>
        """
        return self.send_email(email, subject, content)
    
    def send_ride_receipt(self, email: str, ride_details: dict) -> bool:
        """Send ride receipt email"""
        subject = "Your Valey Ride Receipt"
        content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #1a0b2e; color: white; padding: 2rem; text-align: center;">
                <h1 style="color: #e6b3ff; margin: 0;">Ride Receipt</h1>
            </div>
            <div style="padding: 2rem; background: #f9f9f9;">
                <h2>Thank you for riding with Valey!</h2>
                
                <div style="background: white; padding: 1.5rem; border-radius: 5px; margin: 1rem 0;">
                    <h3>Ride Details</h3>
                    <p><strong>From:</strong> {ride_details.get('pickup_address', 'N/A')}</p>
                    <p><strong>To:</strong> {ride_details.get('dropoff_address', 'N/A')}</p>
                    <p><strong>Date:</strong> {ride_details.get('date', 'N/A')}</p>
                    <p><strong>Driver:</strong> {ride_details.get('driver_name', 'N/A')}</p>
                    <p><strong>Distance:</strong> {ride_details.get('distance', 'N/A')} miles</p>
                    <p><strong>Duration:</strong> {ride_details.get('duration', 'N/A')}</p>
                </div>
                
                <div style="background: white; padding: 1.5rem; border-radius: 5px; margin: 1rem 0;">
                    <h3>Payment Summary</h3>
                    <p><strong>Base Fare:</strong> ${ride_details.get('base_fare', 0):.2f}</p>
                    <p><strong>Distance:</strong> ${ride_details.get('distance_fare', 0):.2f}</p>
                    <p><strong>Total:</strong> ${ride_details.get('total_fare', 0):.2f}</p>
                </div>
                
                <p>Thank you for choosing Valey for your transportation needs!</p>
            </div>
            <div style="background: #0a0a0a; color: #ccc; padding: 1rem; text-align: center;">
                <p>&copy; 2024 Valey. All rights reserved.</p>
            </div>
        </body>
        </html>
        """
        return self.send_email(email, subject, content)
    
    def send_verification_email(self, email: str, verification_code: str) -> bool:
        """Send email verification code"""
        subject = "Verify your Valey account"
        content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #1a0b2e; color: white; padding: 2rem; text-align: center;">
                <h1 style="color: #e6b3ff; margin: 0;">Verify Your Account</h1>
            </div>
            <div style="padding: 2rem; background: #f9f9f9;">
                <h2>Almost there!</h2>
                <p>Please verify your email address to complete your Valey account setup.</p>
                
                <div style="background: white; padding: 1.5rem; border-radius: 5px; margin: 1rem 0; text-align: center;">
                    <h3 style="color: #1a0b2e;">Your verification code:</h3>
                    <div style="font-size: 2rem; font-weight: bold; color: #e6b3ff; letter-spacing: 0.5rem;">{verification_code}</div>
                </div>
                
                <p>This code will expire in 10 minutes.</p>
                <p>If you didn't request this verification, please ignore this email.</p>
            </div>
            <div style="background: #0a0a0a; color: #ccc; padding: 1rem; text-align: center;">
                <p>&copy; 2024 Valey. All rights reserved.</p>
            </div>
        </body>
        </html>
        """
        return self.send_email(email, subject, content)

# Global instance
sendgrid_service = SendGridService()
