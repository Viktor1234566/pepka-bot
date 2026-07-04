"""Profile command handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_init import User
from localization.localization import i18n
from loguru import logger

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /profile command."""
    user_id = update.effective_user.id
    user_data = User.get(user_id)
    
    if not user_data:
        await update.message.reply_text("❌ User not found. Please /start first.")
        return
    
    user_id, username, first_name, last_name, language, tokens, level, experience, hp, max_hp = user_data[:10]
    
    logger.info(f"👤 User {username} viewed profile")
    
    profile_text = f"""
🎮 **Pepka Profile**

👤 Name: {first_name} {last_name}
🏷️ Username: @{username}
💰 Tokens: {tokens}
📊 Level: {level}
⭐ Experience: {experience}
❤️ HP: {hp}/{max_hp}

🏆 Stats:
• Account created: [timestamp]
• Total combats: [stats]
• Wins: [stats]
• Quests completed: [stats]
"""
    
    keyboard = [
        [InlineKeyboardButton(i18n.get_text('buttons.inventory', language), callback_data='inventory')],
        [InlineKeyboardButton(i18n.get_text('buttons.stats', language), callback_data='stats')],
        [InlineKeyboardButton(i18n.get_text('buttons.settings', language), callback_data='settings')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(profile_text, parse_mode='Markdown', reply_markup=reply_markup)
