"""Start command handler"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_init import User
from localization.localization import i18n
from config import SUPPORTED_LANGUAGES
from loguru import logger

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user = update.effective_user
    user_id = user.id
    username = user.username or f"user_{user_id}"
    
    logger.info(f"👤 User {username} started the bot")
    
    # Create user if not exists
    User.create(user_id, username, user.first_name, user.last_name or '')
    
    # Get user data
    user_data = User.get(user_id)
    language = user_data[4] if user_data else 'en'
    
    # Language selection keyboard
    keyboard = []
    for i, lang_code in enumerate(SUPPORTED_LANGUAGES):
        if i % 2 == 0:
            keyboard.append([])
        lang_name = get_language_name(lang_code)
        keyboard[-1].append(InlineKeyboardButton(lang_name, callback_data=f"lang_{lang_code}"))
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = i18n.get_text('commands.start.message', language)
    await update.message.reply_text(message, reply_markup=reply_markup)

def get_language_name(lang_code):
    """Get language name from code."""
    languages = {
        'uk': '🇺🇦 Українська',
        'ru': '🇷🇺 Русский',
        'en': '🇺🇸 English',
        'pl': '🇵🇱 Polski',
        'de': '🇩🇪 Deutsch',
        'it': '🇮🇹 Italiano',
        'zh-cn': '🇨🇳 中文 (简体)',
        'zh-tw': '🇹🇼 中文 (繁體)',
        'ja': '🇯🇵 日本語',
        'ko': '🇰🇷 한국어',
        'es': '🇪🇸 Español',
        'fr': '🇫🇷 Français',
        'hu': '🇭🇺 Magyar',
        'el': '🇬🇷 Ελληνικά',
        'pt': '🇵🇹 Português',
        'nl': '🇳🇱 Nederlands',
        'sv': '🇸🇪 Svenska',
        'da': '🇩🇰 Dansk',
        'no': '🇳🇴 Norsk',
        'fi': '🇫🇮 Suomi',
        'ro': '🇷🇴 Română',
        'bg': '🇧🇬 Български',
        'hr': '🇭🇷 Hrvatski',
        'sk': '🇸🇰 Slovenčina',
        'cs': '🇨🇿 Čeština',
        'tr': '🇹🇷 Türkçe',
        'ar': '🇸🇦 العربية',
        'he': '🇮🇱 עברית',
        'th': '🇹🇭 ไทย',
        'vi': '🇻🇳 Tiếng Việt',
        'id': '🇮🇩 Bahasa Indonesia',
        'ms': '🇲🇾 Bahasa Melayu',
    }
    return languages.get(lang_code, lang_code)
