"""Inventory command handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_init import User
from localization.localization import i18n
from loguru import logger

async def inventory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /inventory command."""
    user_id = update.effective_user.id
    user_data = User.get(user_id)
    
    if not user_data:
        await update.message.reply_text("❌ Please /start first.")
        return
    
    language = user_data[4]
    
    logger.info(f"🎒 User {user_id} opened inventory")
    
    inventory_text = """
🎒 **Your Inventory**

🗡️ Weapons:
• Iron Sword (Common)
• Steel Blade (Rare)

🛡️ Armor:
• Leather Armor (Common)
• Steel Plate (Epic)

🧪 Potions:
• Health Potion x5
• Mana Potion x3

💎 Special Items:
• Ancient Amulet (Legendary)
"""
    
    keyboard = [
        [InlineKeyboardButton(i18n.get_text('buttons.back', language), callback_data='menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(inventory_text, parse_mode='Markdown', reply_markup=reply_markup)
