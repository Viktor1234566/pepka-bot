"""Button callback handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_init import User
from localization.localization import i18n
from commands.combat import start_combat, OPPONENTS
from loguru import logger

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks."""
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data
    
    user_data = User.get(user_id)
    if not user_data:
        await query.answer("❌ User not found", show_alert=True)
        return
    
    language = user_data[4]
    
    logger.info(f"🔘 User {user_id} clicked: {data}")
    
    await query.answer()  # Acknowledge the button press
    
    # Language selection
    if data.startswith('lang_'):
        lang_code = data.split('_')[1]
        await handle_language_select(query, user_id, lang_code)
    
    # Navigation
    elif data == 'menu':
        keyboard = [
            [InlineKeyboardButton(i18n.get_text('buttons.click', language), callback_data='click'),
             InlineKeyboardButton(i18n.get_text('buttons.combat', language), callback_data='combat')],
            [InlineKeyboardButton(i18n.get_text('buttons.profile', language), callback_data='profile'),
             InlineKeyboardButton(i18n.get_text('buttons.inventory', language), callback_data='inventory')],
            [InlineKeyboardButton(i18n.get_text('buttons.leaderboard', language), callback_data='leaderboard'),
             InlineKeyboardButton(i18n.get_text('buttons.shop', language), callback_data='shop')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🎮 Main Menu", reply_markup=reply_markup)
    
    # Combat
    elif data.startswith('combat_'):
        opponent_name = data.split('_', 1)[1]
        await start_combat(query, context, opponent_name)
    
    # Shop
    elif data.startswith('buy_'):
        package = data.split('_')[1]
        await handle_shop_purchase(query, user_id, package, language, context)
    
    # Settings
    elif data.startswith('setting_'):
        setting = data.split('_')[1]
        await handle_setting(query, user_id, setting, language)
    
    else:
        logger.warning(f"Unknown callback: {data}")

async def handle_language_select(query, user_id, lang_code):
    """Handle language selection."""
    # Update language in database (not implemented in this version)
    await query.edit_message_text(f"✅ Language set to {lang_code}!")
    logger.info(f"🗣️ User {user_id} selected language: {lang_code}")

async def handle_shop_purchase(query, user_id, package, language, context):
    """Handle shop purchase."""
    from config import TOKEN_PACKAGES
    
    if package not in TOKEN_PACKAGES:
        await query.edit_message_text("❌ Invalid package")
        return
    
    package_data = TOKEN_PACKAGES[package]
    amount = package_data['amount']
    price = package_data['price']
    bonus = package_data['bonus']
    
    # Store purchase info in context for later use
    context.user_data['pending_purchase'] = {
        'package': package,
        'amount': amount,
        'bonus': bonus,
        'price': price,
        'user_id': user_id
    }
    
    confirm_text = f"""
📦 **Purchase Confirmation**

Package: {package.upper()}
Tokens: {amount}
Bonus: +{bonus}
Price: ${price}

Confirm purchase?
    """
    
    keyboard = [
        [InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_buy_{package}"),
         InlineKeyboardButton("❌ Cancel", callback_data="shop")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(confirm_text, parse_mode='Markdown', reply_markup=reply_markup)

async def handle_setting(query, user_id, setting, language):
    """Handle settings changes."""
    if setting == 'sound':
        await query.edit_message_text("🔊 Sound: Toggle feature not yet implemented")
    elif setting == 'notify':
        await query.edit_message_text("🔔 Notifications: Toggle feature not yet implemented")
    elif setting == 'theme':
        await query.edit_message_text("🎨 Theme: Toggle feature not yet implemented")
    elif setting == 'privacy':
        await query.edit_message_text("🔒 Privacy: Toggle feature not yet implemented")
