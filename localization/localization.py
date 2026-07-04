"""Localization and i18n support for multiple languages"""
import json
from pathlib import Path
from config import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE
from loguru import logger

class Localization:
    """Handles multi-language support for Pepka Bot."""
    
    def __init__(self):
        self.translations = {}
        self.load_all_languages()
    
    def load_all_languages(self):
        """Load all language files."""
        lang_dir = Path('localization/languages')
        lang_dir.mkdir(parents=True, exist_ok=True)
        
        for lang in SUPPORTED_LANGUAGES:
            lang_file = lang_dir / f'{lang}.json'
            if lang_file.exists():
                try:
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        self.translations[lang] = json.load(f)
                    logger.info(f"✅ Loaded language: {lang}")
                except Exception as e:
                    logger.error(f"Failed to load {lang}: {e}")
            else:
                logger.warning(f"Language file not found: {lang_file}")
    
    def get_text(self, key, language=DEFAULT_LANGUAGE, **kwargs):
        """Get translated text by key."""
        if language not in self.translations:
            language = DEFAULT_LANGUAGE
        
        text = self.translations.get(language, {}).get(key, key)
        
        # Format with kwargs if provided
        try:
            if kwargs:
                text = text.format(**kwargs)
        except KeyError as e:
            logger.warning(f"Missing format key: {e}")
        
        return text
    
    def get_button_text(self, button_key, language=DEFAULT_LANGUAGE):
        """Get button text."""
        return self.get_text(f'buttons.{button_key}', language)
    
    def get_command_text(self, command, key, language=DEFAULT_LANGUAGE):
        """Get command-specific text."""
        return self.get_text(f'commands.{command}.{key}', language)
    
    def get_menu_text(self, menu, key, language=DEFAULT_LANGUAGE):
        """Get menu-specific text."""
        return self.get_text(f'menus.{menu}.{key}', language)

# Global instance
i18n = Localization()
