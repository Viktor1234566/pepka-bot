"""Message handler for general messages"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_init import User
from localization.localization import i18n
from loguru import logger

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle general messages."""
    user_id = update.effective_user.id
    message_text = update.message.text
    
    user_data = User.get(user_id)
    if not user_data:
        await update.message.reply_text("❌ Please /start first.")
        return
    
    language = user_data[4]
    
    logger.info(f"💬 User {user_id} sent: {message_text}")
    
    # Show main menu
    if message_text.lower() in ['menu', '🎮 menu', 'main']:
        await show_main_menu(update, context, language)
    else:
        await update.message.reply_text("�ꩀ I don't understand. Type /help for commands.")

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, language: str):
    """Show main menu keyboard."""
    keyboard = [
        [InlineKeyboardButton(i18n.get_text('buttons.click', language), callback_data='click'),
         InlineKeyboardButton(i18n.get_text('buttons.combat', language), callback_data='combat')],
        [InlineKeyboardButton(i18n.get_text('buttons.profile', language), callback_data='profile'),
         InlineKeyboardButton(i18n.get_text('buttons.inventory', language), callback_data='inventory')],
        [InlineKeyboardButton(i18n.get_text('buttons.leaderboard', language), callback_data='leaderboard'),
         InlineKeyboardButton(i18n.get_text('buttons.shop', language), callback_data='shop')],
        [InlineKeyboardButton(i18n.get_text('buttons.stats', language), callback_data='stats'),
         InlineKeyboardButton(i18n.get_text('buttons.settings', language), callback_data='settings')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎮 **Main Menu**", parse_mode='Markdown', reply_markup=reply_markup)
