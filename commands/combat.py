"""Combat command handler"""
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_init import User
from localization.localization import i18n
from config import COMBAT_MIN_REWARD, COMBAT_MAX_REWARD, COMBAT_COOLDOWN
from loguru import logger

OPPONENTS = [
    {'name': 'Goblin', 'hp': 30, 'damage': 5, 'reward': 10},
    {'name': 'Orc', 'hp': 50, 'damage': 10, 'reward': 20},
    {'name': 'Dragon', 'hp': 100, 'damage': 20, 'reward': 50},
    {'name': 'Shadow Knight', 'hp': 75, 'damage': 15, 'reward': 35},
    {'name': 'Dark Wizard', 'hp': 60, 'damage': 18, 'reward': 40},
]

async def combat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /combat command."""
    user_id = update.effective_user.id
    user_data = User.get(user_id)
    
    if not user_data:
        await update.message.reply_text("❌ Please /start first.")
        return
    
    language = user_data[4]
    
    logger.info(f"⚔️ User {user_id} started combat")
    
    # Create opponent selection keyboard
    keyboard = []
    for opponent in OPPONENTS:
        keyboard.append([InlineKeyboardButton(
            f"{opponent['name']} (HP: {opponent['hp']})",
            callback_data=f"combat_{opponent['name'].lower()}"
        )])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = i18n.get_text('commands.combat.select_opponent', language)
    await update.message.reply_text(message, reply_markup=reply_markup)

async def start_combat(update, context, opponent_name):
    """Start actual combat."""
    user_id = update.effective_user.id
    user_data = User.get(user_id)
    
    if not user_data:
        return
    
    language = user_data[4]
    user_hp = user_data[8]
    
    # Find opponent
    opponent = next((o for o in OPPONENTS if o['name'].lower() == opponent_name), None)
    if not opponent:
        return
    
    # Simulate combat
    opponent_hp = opponent['hp']
    rounds = 0
    
    while user_hp > 0 and opponent_hp > 0 and rounds < 20:
        # User attack
        user_damage = random.randint(5, 20)
        opponent_hp -= user_damage
        
        if opponent_hp <= 0:
            break
        
        # Opponent attack
        opponent_damage = random.randint(opponent['damage'] - 5, opponent['damage'] + 5)
        user_hp -= opponent_damage
        
        rounds += 1
    
    # Determine winner
    if user_hp > 0:
        result = "WIN"
        tokens_earned = opponent['reward']
        User.add_tokens(user_id, tokens_earned)
        message = f"🎉 Victory! You defeated {opponent['name']}!\n💰 Earned {tokens_earned} tokens"
    else:
        result = "LOSE"
        message = f"💀 Defeat! {opponent['name']} was too strong.\n😢 No tokens earned"
    
    logger.info(f"⚔️ Combat: User {user_id} vs {opponent_name} - {result}")
    await update.callback_query.edit_message_text(message)
