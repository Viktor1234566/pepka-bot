"""Telegram Payments integration with Stripe backend"""
from telegram import Update, LabeledPrice, ShippingOption
from telegram.ext import ContextTypes
from database.db_init import User
from payments.stripe_integration import StripePayment
from config import TOKEN_PACKAGES, STRIPE_API_KEY
from loguru import logger
from typing import Dict

class TelegramPayments:
    """Handle Telegram Payments with Stripe."""
    
    @staticmethod
    async def send_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE, package: str):
        """
        Send a payment invoice to the user.
        
        Args:
            update: Telegram update
            context: Bot context
            package: Token package name
        """
        user_id = update.effective_user.id
        
        # Validate package
        if package not in TOKEN_PACKAGES:
            await update.callback_query.edit_message_text("❌ Invalid package")
            return
        
        package_data = TOKEN_PACKAGES[package]
        amount = package_data['amount']
        price = int(package_data['price'] * 100)  # Convert to cents
        bonus = package_data['bonus']
        
        logger.info(f"💳 Sending invoice to user {user_id} for {package} (${package_data['price']})")
        
        # Prepare invoice
        title = f"Pepka Tokens - {package.upper()}"
        description = f"{amount} tokens + {bonus} bonus tokens"
        payload = f"{user_id}_{package}_{amount}_{bonus}"
        
        prices = [
            LabeledPrice(
                label=f"{amount} Pepka Tokens",
                amount=price
            ),
        ]
        
        # If bonus, show it separately
        if bonus > 0:
            prices.append(
                LabeledPrice(
                    label=f"+{bonus} Bonus Tokens",
                    amount=0
                )
            )
        
        try:
            await update.callback_query.from_user.send_invoice(
                title=title,
                description=description,
                payload=payload,
                provider_token=STRIPE_API_KEY,
                currency='USD',
                prices=prices,
                start_parameter=f"pay_{package}",
                is_flexible=False
            )
            logger.info(f"✅ Invoice sent to user {user_id}")
        except Exception as e:
            logger.error(f"❌ Error sending invoice: {e}")
            await update.callback_query.edit_message_text(
                f"❌ Error sending invoice. Please try again.\n\nError: {str(e)}"
            )
    
    @staticmethod
    async def handle_pre_checkout_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle pre-checkout query from Telegram.
        
        Args:
            update: Telegram update
            context: Bot context
        """
        query = update.pre_checkout_query
        user_id = query.from_user.id
        
        logger.info(f"✓ Pre-checkout query from user {user_id}")
        
        # Parse payload
        try:
            payload_parts = query.invoice_payload.split('_')
            package = payload_parts[1]
            
            # Validate package
            if package not in TOKEN_PACKAGES:
                await query.answer(ok=False, error_message="Invalid package")
                return
            
            # Approve payment
            await query.answer(ok=True)
            logger.info(f"✅ Pre-checkout approved for user {user_id}")
        except Exception as e:
            logger.error(f"❌ Error in pre-checkout: {e}")
            await query.answer(ok=False, error_message="Payment error")
    
    @staticmethod
    async def handle_successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle successful payment from Telegram.
        
        Args:
            update: Telegram update
            context: Bot context
        """
        payment_info = update.message.successful_payment
        user_id = update.effective_user.id
        
        logger.info(f"💰 Successful payment from user {user_id}: {payment_info.total_amount} {payment_info.currency}")
        
        try:
            # Parse payload to get package info
            payload_parts = payment_info.invoice_payload.split('_')
            user_id_from_payload = int(payload_parts[0])
            package = payload_parts[1]
            amount = int(payload_parts[2])
            bonus = int(payload_parts[3])
            
            # Validate user
            if user_id != user_id_from_payload:
                logger.error(f"User ID mismatch: {user_id} vs {user_id_from_payload}")
                await update.message.reply_text("❌ Payment verification failed")
                return
            
            # Validate package
            if package not in TOKEN_PACKAGES:
                logger.error(f"Invalid package: {package}")
                await update.message.reply_text("❌ Invalid package")
                return
            
            # Add tokens to user
            total_tokens = amount + bonus
            User.add_tokens(user_id, total_tokens)
            
            # Confirm to user
            confirmation_msg = f"""
🎉 **Payment Successful!**

💰 Package: {package.upper()}
�꩐ Base Tokens: +{amount}
🎁 Bonus: +{bonus}
📈 Total: +{total_tokens}

✅ Tokens added to your account!
            """
            
            await update.message.reply_text(confirmation_msg, parse_mode='Markdown')
            logger.info(f"✅ Tokens added to user {user_id}: {total_tokens}")
        except Exception as e:
            logger.error(f"❌ Error processing payment: {e}")
            await update.message.reply_text(
                f"❌ Error processing your payment.\n\nError: {str(e)}"
            )
