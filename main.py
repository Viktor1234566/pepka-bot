"""Main entry point for Pepka Bot"""
import asyncio
import logging
from loguru import logger
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from handlers.message_handler import handle_message
from handlers.button_handler import handle_button
from commands.start import start_command
from commands.help import help_command
from commands.profile import profile_command
from commands.click import click_command
from commands.combat import combat_command
from commands.inventory import inventory_command
from commands.leaderboard import leaderboard_command
from commands.stats import stats_command
from commands.settings import settings_command
from commands.shop import shop_command
from database.db_init import initialize_database
from config import BOT_TOKEN, LOG_FILE, LOG_LEVEL
import os

# Configure logging
logger.remove()
logger.add(
    LOG_FILE,
    level=LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    rotation="500 MB",
    retention="10 days"
)
logger.add(
    lambda msg: print(msg, end=''),
    level=LOG_LEVEL,
    format="{time:HH:mm:ss} | {level: <8} | {message}"
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def main():
    """Start the bot."""
    logger.info("🐸 Starting Pepka Bot...")
    
    # Initialize database
    logger.info("📊 Initializing database...")
    initialize_database()
    logger.info("✅ Database initialized!")
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    logger.info("⚙️  Registering command handlers...")
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("profile", profile_command))
    app.add_handler(CommandHandler("click", click_command))
    app.add_handler(CommandHandler("combat", combat_command))
    app.add_handler(CommandHandler("inventory", inventory_command))
    app.add_handler(CommandHandler("leaderboard", leaderboard_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("settings", settings_command))
    app.add_handler(CommandHandler("shop", shop_command))
    
    # Add callback handlers for buttons
    app.add_handler(CallbackQueryHandler(handle_button))
    
    # Add message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("✅ All handlers registered!")
    logger.info("🐸 Pepka Bot is running!")
    
    # Start the bot
    await app.run_polling()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
