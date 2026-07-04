"""Click command handler with combo system"""
from telegram import Update
from telegram.ext import ContextTypes
from database.db_init import User
from localization.localization import i18n
from config import CLICK_REWARD, COMBO_CLICKS, COMBO_TIME_WINDOW, COMBO_REWARD
from loguru import logger
import time

# Store click timestamps for combo detection
user_clicks = {}

async def click_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /click command."""
    user_id = update.effective_user.id
    user_data = User.get(user_id)
    
    if not user_data:
        await update.message.reply_text("❌ Please /start first.")
        return
    
    language = user_data[4]
    current_time = time.time()
    
    # Initialize user click history if not exists
    if user_id not in user_clicks:
        user_clicks[user_id] = []
    
    # Remove old clicks outside the time window
    user_clicks[user_id] = [click_time for click_time in user_clicks[user_id] 
                            if current_time - click_time < COMBO_TIME_WINDOW]
    
    # Add current click
    user_clicks[user_id].append(current_time)
    
    tokens_earned = CLICK_REWARD
    bonus_earned = 0
    
    # Check for combo
    if len(user_clicks[user_id]) >= COMBO_CLICKS:
        bonus_earned = COMBO_REWARD
        tokens_earned += bonus_earned
        user_clicks[user_id] = []  # Reset combo counter
        combo_message = i18n.get_text('commands.click.combo', language, bonus=bonus_earned)
    else:
        combo_message = ""
    
    # Add tokens to user
    User.add_tokens(user_id, tokens_earned)
    
    # Update user data
    user_data = User.get(user_id)
    total_tokens = user_data[5]
    
    logger.info(f"🖱️ User {user_id} clicked - earned {tokens_earned} tokens")
    
    message = i18n.get_text('commands.click.success', language, 
                            tokens=tokens_earned, total_tokens=total_tokens)
    
    if bonus_earned > 0:
        message += f"\n{combo_message}"
    
    await update.message.reply_text(message)
