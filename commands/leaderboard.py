"""Leaderboard command handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_init import User
from localization.localization import i18n
from loguru import logger

async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /leaderboard command."""
    user_id = update.effective_user.id
    user_data = User.get(user_id)
    
    if not user_data:
        await update.message.reply_text("❌ Please /start first.")
        return
    
    language = user_data[4]
    
    logger.info(f"🏆 User {user_id} viewed leaderboard")
    
    # Get top 10 users
    leaderboard = User.get_leaderboard(10)
    
    leaderboard_text = i18n.get_text('leaderboard.title', language) + "\n\n"
    leaderboard_text += i18n.get_text('leaderboard.header', language) + "\n"
    leaderboard_text += "━" * 40 + "\n"
    
    for idx, (uid, username, tokens, level) in enumerate(leaderboard, 1):
        medal = '🥇' if idx == 1 else '🥈' if idx == 2 else '🥉' if idx == 3 else f'{idx}.'
        leaderboard_text += f"{medal} {username} | {tokens} 💰 | Lvl {level}\n"
    
    keyboard = [
        [InlineKeyboardButton(i18n.get_text('buttons.back', language), callback_data='menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(leaderboard_text, reply_markup=reply_markup)
