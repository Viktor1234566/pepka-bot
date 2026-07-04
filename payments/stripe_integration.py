"""Stripe payment integration"""
import stripe
from config import STRIPE_API_KEY, STRIPE_SECRET_KEY
from loguru import logger
from typing import Dict, Optional

# Initialize Stripe
stripe.api_key = STRIPE_SECRET_KEY

class StripePayment:
    """Handle Stripe payments."""
    
    @staticmethod
    def create_payment_intent(amount_cents: int, user_id: int, package: str) -> Optional[Dict]:
        """
        Create a Stripe payment intent.
        
        Args:
            amount_cents: Amount in cents (e.g., 999 for $9.99)
            user_id: Telegram user ID
            package: Token package name
        
        Returns:
            Payment intent data or None
        """
        try:
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency='usd',
                metadata={
                    'user_id': user_id,
                    'package': package,
                    'bot': 'pepka'
                },
                description=f"Pepka Tokens - {package} package"
            )
            logger.info(f"💳 Payment intent created: {intent.id} for user {user_id}")
            return intent
        except stripe.error.StripeError as e:
            logger.error(f"❌ Stripe error creating intent: {e}")
            return None
    
    @staticmethod
    def create_checkout_session(amount_cents: int, user_id: int, package: str, success_url: str, cancel_url: str) -> Optional[Dict]:
        """
        Create a Stripe checkout session for Telegram.
        
        Args:
            amount_cents: Amount in cents
            user_id: Telegram user ID
            package: Token package name
            success_url: URL to redirect after successful payment
            cancel_url: URL to redirect after cancelled payment
        
        Returns:
            Checkout session data or None
        """
        try:
            from config import TOKEN_PACKAGES
            package_data = TOKEN_PACKAGES.get(package, {})
            
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Pepka Tokens - {package.upper()}',
                            'description': f"{package_data.get('amount', 0)} tokens + {package_data.get('bonus', 0)} bonus",
                            'images': [],
                        },
                        'unit_amount': amount_cents,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    'user_id': user_id,
                    'package': package,
                    'bot': 'pepka'
                }
            )
            logger.info(f"💳 Checkout session created: {session.id} for user {user_id}")
            return session
        except stripe.error.StripeError as e:
            logger.error(f"❌ Stripe error creating session: {e}")
            return None
    
    @staticmethod
    def verify_payment(payment_intent_id: str) -> Optional[Dict]:
        """
        Verify a payment intent status.
        
        Args:
            payment_intent_id: Stripe payment intent ID
        
        Returns:
            Payment intent data or None
        """
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            logger.info(f"💳 Payment verified: {intent.id} - Status: {intent.status}")
            return intent
        except stripe.error.StripeError as e:
            logger.error(f"❌ Stripe error verifying payment: {e}")
            return None
    
    @staticmethod
    def handle_webhook(payload: Dict, sig_header: str, webhook_secret: str) -> Optional[Dict]:
        """
        Handle Stripe webhook events.
        
        Args:
            payload: Webhook payload
            sig_header: Webhook signature header
            webhook_secret: Webhook secret
        
        Returns:
            Event data or None
        """
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
            logger.info(f"🔔 Stripe webhook event: {event['type']}")
            return event
        except ValueError:
            logger.error("❌ Invalid webhook payload")
            return None
        except stripe.error.SignatureError:
            logger.error("❌ Invalid webhook signature")
            return None
    
    @staticmethod
    def process_successful_payment(intent_id: str) -> bool:
        """
        Process a successful payment and add tokens to user.
        
        Args:
            intent_id: Stripe payment intent ID
        
        Returns:
            True if processing was successful
        """
        from database.db_init import User
        from config import TOKEN_PACKAGES
        
        try:
            intent = stripe.PaymentIntent.retrieve(intent_id)
            
            if intent.status != 'succeeded':
                logger.warning(f"Payment not succeeded: {intent.status}")
                return False
            
            # Get metadata
            user_id = int(intent.metadata.get('user_id'))
            package = intent.metadata.get('package')
            
            # Get package info
            package_data = TOKEN_PACKAGES.get(package)
            if not package_data:
                logger.error(f"Invalid package: {package}")
                return False
            
            tokens = package_data['amount'] + package_data['bonus']
            
            # Add tokens to user
            User.add_tokens(user_id, tokens)
            
            logger.info(f"✅ Payment processed: User {user_id} received {tokens} tokens")
            return True
        except Exception as e:
            logger.error(f"❌ Error processing payment: {e}")
            return False
    
    @staticmethod
    def get_payment_status(payment_intent_id: str) -> Optional[str]:
        """
        Get payment status.
        
        Args:
            payment_intent_id: Stripe payment intent ID
        
        Returns:
            Payment status or None
        """
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return intent.status
        except stripe.error.StripeError as e:
            logger.error(f"❌ Error getting payment status: {e}")
            return None
