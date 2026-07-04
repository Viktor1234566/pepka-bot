"""Database initialization and models"""
import sqlite3
from datetime import datetime
from pathlib import Path
from config import DATABASE_PATH
from loguru import logger

def initialize_database():
    """Initialize the SQLite database with all required tables."""
    db_path = Path(DATABASE_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            first_name TEXT,
            last_name TEXT,
            language TEXT DEFAULT 'en',
            tokens INTEGER DEFAULT 50,
            level INTEGER DEFAULT 1,
            experience INTEGER DEFAULT 0,
            hp INTEGER DEFAULT 100,
            max_hp INTEGER DEFAULT 100,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_banned BOOLEAN DEFAULT 0,
            referrer_id INTEGER,
            referral_bonus_received BOOLEAN DEFAULT 0
        )
    ''')
    
    # Daily stats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date DATE DEFAULT CURRENT_DATE,
            clicks INTEGER DEFAULT 0,
            combats INTEGER DEFAULT 0,
            quests_completed INTEGER DEFAULT 0,
            tokens_earned INTEGER DEFAULT 0,
            tokens_spent INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            UNIQUE(user_id, date)
        )
    ''')
    
    # Inventory table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            item_type TEXT NOT NULL,
            quantity INTEGER DEFAULT 1,
            rarity TEXT DEFAULT 'common',
            acquired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Combat history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS combat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            opponent_name TEXT NOT NULL,
            user_hp INTEGER,
            opponent_hp INTEGER,
            user_damage INTEGER,
            opponent_damage INTEGER,
            result TEXT,
            tokens_earned INTEGER DEFAULT 0,
            experience_earned INTEGER DEFAULT 0,
            combat_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Quests table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            quest_name TEXT NOT NULL,
            description TEXT,
            difficulty TEXT DEFAULT 'normal',
            status TEXT DEFAULT 'active',
            reward_tokens INTEGER,
            reward_experience INTEGER,
            progress INTEGER DEFAULT 0,
            required_progress INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            transaction_type TEXT,
            amount INTEGER,
            currency TEXT DEFAULT 'tokens',
            payment_method TEXT,
            status TEXT DEFAULT 'completed',
            reference_id TEXT UNIQUE,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Referrals table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_id INTEGER NOT NULL,
            referred_user_id INTEGER NOT NULL,
            bonus_tokens_given INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(referrer_id) REFERENCES users(user_id),
            FOREIGN KEY(referred_user_id) REFERENCES users(user_id),
            UNIQUE(referrer_id, referred_user_id)
        )
    ''')
    
    # Achievements table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            achievement_name TEXT NOT NULL,
            achievement_icon TEXT,
            description TEXT,
            points INTEGER DEFAULT 10,
            unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Leaderboard snapshot table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard_snapshot (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            rank INTEGER,
            tokens INTEGER,
            level INTEGER,
            combat_wins INTEGER,
            snapshot_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            notifications_enabled BOOLEAN DEFAULT 1,
            sound_enabled BOOLEAN DEFAULT 1,
            language TEXT DEFAULT 'en',
            theme TEXT DEFAULT 'light',
            privacy_level TEXT DEFAULT 'public',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Admin logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            target_user_id INTEGER,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    logger.info("✅ Database initialized successfully!")
    conn.close()

class User:
    """User model for database operations."""
    
    @staticmethod
    def create(user_id, username, first_name, last_name='', language='en'):
        """Create a new user."""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (user_id, username, first_name, last_name, language)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name, language))
            conn.commit()
            logger.info(f"👤 User {username} created")
            return True
        except sqlite3.IntegrityError:
            logger.warning(f"User {user_id} already exists")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def get(user_id):
        """Get user data by ID."""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    @staticmethod
    def add_tokens(user_id, amount):
        """Add tokens to user."""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET tokens = tokens + ? WHERE user_id = ?
        ''', (amount, user_id))
        conn.commit()
        conn.close()
        logger.info(f"💰 {amount} tokens added to user {user_id}")
    
    @staticmethod
    def add_experience(user_id, amount):
        """Add experience to user."""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET experience = experience + ? WHERE user_id = ?
        ''', (amount, user_id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def level_up(user_id):
        """Level up user."""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET level = level + 1, experience = 0, 
            max_hp = max_hp + 10 WHERE user_id = ?
        ''', (user_id,))
        conn.commit()
        conn.close()
        logger.info(f"⬆️ User {user_id} leveled up")
    
    @staticmethod
    def get_leaderboard(limit=10):
        """Get top users by tokens."""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT user_id, username, tokens, level FROM users 
            WHERE is_banned = 0
            ORDER BY tokens DESC LIMIT ?
        ''', (limit,))
        leaderboard = cursor.fetchall()
        conn.close()
        return leaderboard
