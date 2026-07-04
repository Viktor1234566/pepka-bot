"""Settings command handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_init import User
from localization.localization import i18n
from loguru import logger

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /settings command."""
    user_id = update.effective_user.id
    user_data = User.get(user_id)
    
    if not user_data:
        await update.message.reply_text("❌ Please /start first.")
        return
    
    language = user_data[4]
    
    logger.info(f"⚙️ User {user_id} opened settings")
    
    settings_text = """
⚙️ **Settings**

🔊 Sound: ON
🔔 Notifications: ON
🎨 Theme: Light
🔒 Privacy: Public
"""
    
    keyboard = [
        [InlineKeyboardButton("🔊 Sound", callback_data='setting_sound'),
         InlineKeyboardButton("🔔 Notifications", callback_data='setting_notify')],
        [InlineKeyboardButton("🎨 Theme", callback_data='setting_theme'),
         InlineKeyboardButton("🔒 Privacy", callback_data='setting_privacy')],
        [InlineKeyboardButton(i18n.get_text('buttons.back', language), callback_data='menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(settings_text, parse_mode='Markdown', reply_markup=reply_markup)
