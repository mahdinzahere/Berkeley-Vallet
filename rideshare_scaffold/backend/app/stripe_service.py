import stripe
from typing import Optional
from .config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeService:
    @staticmethod
    def create_connect_account(email: str, phone: str) -> dict:
        """Create Stripe Connect Express account for driver"""
        try:
            account = stripe.Account.create(
                type="express",
                country="US",
                email=email,
                phone=phone,
                capabilities={
                    "card_payments": {"requested": True},
                    "transfers": {"requested": True},
                },
            )
            return {"account_id": account.id}
        except stripe.error.StripeError as e:
            raise Exception(f"Failed to create Stripe account: {str(e)}")

    @staticmethod
    def create_account_link(account_id: str, refresh_url: str, return_url: str) -> str:
        """Create account link for driver onboarding"""
        try:
            account_link = stripe.AccountLink.create(
                account=account_id,
                refresh_url=refresh_url,
                return_url=return_url,
                type="account_onboarding",
            )
            return account_link.url
        except stripe.error.StripeError as e:
            raise Exception(f"Failed to create account link: {str(e)}")

    @staticmethod
    def create_payment_intent(
        amount: int,
        currency: str = "usd",
        driver_account_id: Optional[str] = None,
        application_fee_amount: int = 0,
        metadata: Optional[dict] = None
    ) -> dict:
        """Create PaymentIntent for ride payment"""
        try:
            payment_intent_data = {
                "amount": amount,
                "currency": currency,
                "automatic_payment_methods": {"enabled": True},
            }
            
            if driver_account_id:
                payment_intent_data["transfer_data"] = {
                    "destination": driver_account_id
                }
                payment_intent_data["application_fee_amount"] = application_fee_amount
            
            if metadata:
                payment_intent_data["metadata"] = metadata
            
            payment_intent = stripe.PaymentIntent.create(**payment_intent_data)
            return {
                "payment_intent_id": payment_intent.id,
                "client_secret": payment_intent.client_secret
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Failed to create payment intent: {str(e)}")

    @staticmethod
    def capture_payment_intent(payment_intent_id: str) -> dict:
        """Capture authorized PaymentIntent"""
        try:
            payment_intent = stripe.PaymentIntent.capture(payment_intent_id)
            return {"status": payment_intent.status}
        except stripe.error.StripeError as e:
            raise Exception(f"Failed to capture payment intent: {str(e)}")

    @staticmethod
    def cancel_payment_intent(payment_intent_id: str) -> dict:
        """Cancel PaymentIntent"""
        try:
            payment_intent = stripe.PaymentIntent.cancel(payment_intent_id)
            return {"status": payment_intent.status}
        except stripe.error.StripeError as e:
            raise Exception(f"Failed to cancel payment intent: {str(e)}")

    @staticmethod
    def create_tip_payment_intent(
        amount: int,
        driver_account_id: str,
        currency: str = "usd",
        metadata: Optional[dict] = None
    ) -> dict:
        """Create PaymentIntent for tip payment"""
        try:
            payment_intent_data = {
                "amount": amount,
                "currency": currency,
                "automatic_payment_methods": {"enabled": True},
                "transfer_data": {
                    "destination": driver_account_id
                },
                "application_fee_amount": 0,  # 0% platform fee for tips
            }
            
            if metadata:
                payment_intent_data["metadata"] = metadata
            
            payment_intent = stripe.PaymentIntent.create(**payment_intent_data)
            return {
                "payment_intent_id": payment_intent.id,
                "client_secret": payment_intent.client_secret
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Failed to create tip payment intent: {str(e)}")

    @staticmethod
    def verify_webhook_signature(payload: bytes, signature: str) -> dict:
        """Verify webhook signature"""
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, settings.STRIPE_WEBHOOK_SECRET
            )
            return event
        except ValueError as e:
            raise Exception("Invalid payload")
        except stripe.error.SignatureVerificationError as e:
            raise Exception("Invalid signature")
