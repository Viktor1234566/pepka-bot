"""Shop command handler for token purchases"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_init import User
from localization.localization import i18n
from config import TOKEN_PACKAGES
from loguru import logger

async def shop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /shop command."""
    user_id = update.effective_user.id
    user_data = User.get(user_id)
    
    if not user_data:
        await update.message.reply_text("❌ Please /start first.")
        return
    
    language = user_data[4]
    
    logger.info(f"🛍️ User {user_id} opened shop")
    
    shop_text = i18n.get_text('commands.shop.select_package', language) + "\n\n"
    
    keyboard = []
    for package_name, package_data in TOKEN_PACKAGES.items():
        amount = package_data['amount']
        price = package_data['price']
        bonus = package_data['bonus']
        
        bonus_text = f" + {bonus}🎁" if bonus > 0 else ""
        button_text = f"{amount} 💰 - ${price}{bonus_text}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"buy_{package_name}")])
        
        shop_text += f"📦 **{package_name.upper()}**: {amount} tokens - ${price}{bonus_text}\n"
    
    keyboard.append([InlineKeyboardButton(i18n.get_text('buttons.back', language), callback_data='menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(shop_text, parse_mode='Markdown', reply_markup=reply_markup)
