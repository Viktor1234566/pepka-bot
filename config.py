import os
from dotenv import load_dotenv

load_dotenv()

# ========== BOT CONFIGURATION ==========
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
BOT_USERNAME = 'pepka_bot'

# ========== DATABASE ==========
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///pepka.db')
DATABASE_PATH = 'pepka.db'

# ========== PAYMENTS ==========
STRIPE_API_KEY = os.getenv('STRIPE_API_KEY', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')

PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID', '')
PAYPAL_SECRET = os.getenv('PAYPAL_SECRET', '')

CRYPTO_WALLET_ADDRESS = os.getenv('CRYPTO_WALLET_ADDRESS', '')
WEB3_PROVIDER = os.getenv('WEB3_PROVIDER', '')

# ========== ADMIN SETTINGS ==========
ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_IDS', '').split(',') if x] or [123456789]  # Replace with your ID
SUPPORT_CHAT_ID = os.getenv('SUPPORT_CHAT_ID', '-1001234567890')

# ========== GAME SETTINGS ==========
CLICK_REWARD = 1  # Tokens per click
COMBO_CLICKS = 5  # Clicks needed for combo
COMBO_TIME_WINDOW = 5  # Seconds
COMBO_REWARD = 10  # Bonus tokens

COMBAT_MIN_REWARD = 5
COMBAT_MAX_REWARD = 50
COMBAT_COOLDOWN = 30  # Seconds

QUEST_REWARD_MIN = 20
QUEST_REWARD_MAX = 100

LEVEL_UP_REWARD = 50
LEVEL_UP_REQUIREMENT = 100  # Tokens needed to level up

MAX_LEVEL = 100
START_HP = 100
START_TOKENS = 50

# ========== REFERRAL SYSTEM ==========
REFERRAL_BONUS = 100  # Tokens for referrer
REFERRAL_BONUS_FRIEND = 50  # Tokens for new player

# ========== PRICES ==========
TOKEN_PACKAGES = {
    'small': {'amount': 100, 'price': 0.99, 'bonus': 0},
    'medium': {'amount': 500, 'price': 4.99, 'bonus': 50},
    'large': {'amount': 1000, 'price': 8.99, 'bonus': 100},
    'mega': {'amount': 5000, 'price': 39.99, 'bonus': 500},
    'ultra': {'amount': 10000, 'price': 69.99, 'bonus': 1500},
}

# ========== LOCALIZATION ==========
DEFAULT_LANGUAGE = 'en'
SUPPORTED_LANGUAGES = [
    'uk', 'ru', 'en', 'pl', 'de', 'it', 'zh-cn', 'zh-tw',
    'ja', 'ko', 'es', 'fr', 'hu', 'el', 'pt', 'nl',
    'sv', 'da', 'no', 'fi', 'ro', 'bg', 'hr', 'sk',
    'cs', 'tr', 'ar', 'he', 'th', 'vi', 'id', 'ms'
]

# ========== LOGGING ==========
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = 'logs/pepka_bot.log'
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5

# ========== API ENDPOINTS ==========
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')
API_PORT = int(os.getenv('API_PORT', 5000))

# ========== CACHE ==========
CACHE_ENABLED = True
CACHE_TTL = 3600  # 1 hour

# ========== FEATURES ==========
FEATURE_COMBAT = True
FEATURE_QUESTS = True
FEATURE_INVENTORY = True
FEATURE_LEADERBOARD = True
FEATURE_PAYMENTS = True
FEATURE_REFERRAL = True
FEATURE_MULTIPLAYER = True

# ========== SECURITY ==========
MAX_REQUEST_SIZE = 1024 * 1024  # 1 MB
RATE_LIMIT_CLICKS = 10  # Clicks per minute
RATE_LIMIT_REQUESTS = 30  # Requests per minute

# ========== MAINTENANCE ==========
MAINTENANCE_MODE = False
MAINTENANCE_MESSAGE = "Pepka Bot is under maintenance. Please try again later!"

# ========== WEBHOOK ==========
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', 8443))
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'secret')

# ========== TIMEZONE ==========
TIMEZONE = 'UTC'

# ========== VERSION ==========
BOT_VERSION = '1.0.0'
API_VERSION = 'v1'
