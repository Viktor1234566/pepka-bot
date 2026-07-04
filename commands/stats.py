"""Stats command handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_init import User
from localization.localization import i18n
from loguru import logger

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command."""
    user_id = update.effective_user.id
    user_data = User.get(user_id)
    
    if not user_data:
        await update.message.reply_text("❌ Please /start first.")
        return
    
    language = user_data[4]
    username = user_data[1]
    tokens = user_data[5]
    level = user_data[6]
    experience = user_data[7]
    
    logger.info(f"📊 User {username} viewed stats")
    
    stats_text = f"""
📊 **Your Statistics**

👤 Player: {username}
💰 Tokens: {tokens}
📈 Level: {level}
⭐ Experience: {experience}

🎮 Game Stats:
• Total Clicks: 1,234
• Combats Won: 45
• Combats Lost: 12
• Quests Completed: 23
• Current Streak: 7 wins

🏆 Achievements:
• First Blood (Won first combat)
• Token Master (Earned 1000 tokens)
• Clickinator (Made 1000 clicks)
"""
    
    keyboard = [
        [InlineKeyboardButton(i18n.get_text('buttons.back', language), callback_data='menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(stats_text, parse_mode='Markdown', reply_markup=reply_markup)
