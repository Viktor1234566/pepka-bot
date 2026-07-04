"""Help command handler"""
from telegram import Update
from telegram.ext import ContextTypes
from database.db_init import User
from localization.localization import i18n
from loguru import logger

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    user_id = update.effective_user.id
    user_data = User.get(user_id)
    language = user_data[4] if user_data else 'en'
    
    logger.info(f"📖 User {user_id} requested help")
    
    help_text = i18n.get_text('commands.help.message', language)
    await update.message.reply_text(help_text, parse_mode='Markdown')
