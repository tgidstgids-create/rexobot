"""
Logging Module for OTP Bot
Sends purchase logs, OTP receipts, and recharge approvals to Telegram channel
WITH CUSTOM EMOJIS - DIRECT API CALLS
"""

import logging
import threading
from datetime import datetime
import requests
import json

logger = logging.getLogger(__name__)

class TelegramLogger:
    """Sends logs to Telegram channel with custom emojis using direct API calls"""
    
    def __init__(self, bot_token: str, log_channel_id: str, 
                 support_link: str = "https://t.me/+qJCnoSZgjocyODdl", 
                 buy_link: str = "https://t.me/CUTE_OTP_SELLER_BOT"):
        """
        Initialize Telegram logger
        """
        self.bot_token = bot_token
        self.log_channel_id = log_channel_id
        self.support_link = support_link
        self.buy_link = buy_link
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
        
        # Custom emoji IDs - fixed as requested
        self.TOP_EMOJI = "6120916334873153887"      # Upar wala emoji
        self.BOTTOM_EMOJI = "6170205375267082717"    # Niche wala emoji
        
        self._test_connection()
    
    def _test_connection(self):
        """Test Telegram API connection"""
        try:
            response = requests.get(f"{self.api_url}/getMe")
            if response.status_code == 200:
                bot_info = response.json()
                logger.info(f"✅ Logger initialized: @{bot_info['result']['username']}")
            else:
                logger.error("❌ Failed to connect to Telegram API")
        except Exception as e:
            logger.error(f"❌ Logger initialization failed: {e}")
    
    def _get_inline_buttons(self):
        """Create inline keyboard with Support and Buy buttons"""
        return {
            "inline_keyboard": [
                [
                    {"text": "🆘 Support", "url": self.support_link},
                    {"text": "🛒 Buy", "url": self.buy_link}
                ]
            ]
        }
    
    def _format_phone(self, phone: str) -> str:
        """Format phone number with masking"""
        if not phone:
            return "N/A"
        try:
            # Clean phone number
            digits = ''.join(filter(str.isdigit, str(phone)))
            if len(digits) >= 10:
                return f"{digits[:3]}****{digits[-2:]}"
            elif len(digits) >= 6:
                return f"{digits[:3]}****"
            else:
                return "****"
        except:
            return "****"
    
    def _format_user_id(self, user_id) -> str:
        """Format user ID with masking"""
        try:
            user_str = str(user_id)
            if len(user_str) > 6:
                return f"{user_str[:3]}***{user_str[-2:]}"
            elif len(user_str) > 4:
                return f"{user_str[:2]}***{user_str[-1:]}"
            else:
                return f"{user_str[:1]}***"
        except:
            return "***"
    
    def _send_message(self, text: str, entities: list = None) -> bool:
        """
        Send message to Telegram channel with optional entities
        """
        try:
            # Get inline keyboard
            keyboard = self._get_inline_buttons()
            
            # Prepare payload
            payload = {
                "chat_id": self.log_channel_id,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
                "reply_markup": json.dumps(keyboard)
            }
            
            # Add entities if provided
            if entities:
                payload["entities"] = entities
            
            # Send message
            response = requests.post(
                f"{self.api_url}/sendMessage",
                json=payload
            )
            
            if response.status_code == 200:
                logger.debug(f"Message sent successfully")
                return True
            else:
                logger.error(f"API Error: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False
    
    def log_purchase(self, user_id: int, country: str, price: float, phone: str) -> bool:
        """
        Log when user buys an account
        Format: Exactly as requested
        """
        # Format data
        formatted_phone = self._format_phone(phone)
        formatted_user = self._format_user_id(user_id)
        
        # Create message WITHOUT emojis in text (placeholders for entities)
        text = (
            f"🔝\n\n"
            f"<b>🔥 NEW ACCOUNT SOLD! 🔥</b>\n\n"
            f"<b>✚ Category:</b> {country}\n"
            f"<b>✚ Region:</b> {country}\n"
            f"<b>✚ Number:</b> {formatted_phone}📞\n"
            f"<b>✚ User:</b> {formatted_user}👤\n"
            f"<b>✚ Status:</b> Verified & Delivered ✅\n\n"
            f"<b>🤖 @CUTE_OTP_SELLER_BOT</b>\n\n"
            f"🔝"
        )
        
        # Create entities for custom emojis
        entities = [
            {
                "type": "custom_emoji",
                "offset": 0,  # First character (first 🔝)
                "length": 1,
                "custom_emoji_id": self.TOP_EMOJI
            },
            {
                "type": "custom_emoji",
                "offset": len(text) - 1,  # Last character (last 🔝)
                "length": 1,
                "custom_emoji_id": self.BOTTOM_EMOJI
            }
        ]
        
        return self._send_message(text, entities)
    
    def log_otp_received(self, user_id: int, phone: str, otp_code: str, 
                         country: str, price: float) -> bool:
        """
        Log when OTP is received
        Format: Exactly as requested
        """
        # Format data
        formatted_phone = self._format_phone(phone)
        formatted_user = self._format_user_id(user_id)
        
        # Create message WITHOUT emojis in text (placeholders for entities)
        text = (
            f"🔝\n\n"
            f"<b>🔐 OTP RECEIVED! 🔐</b>\n\n"
            f"<b>━ Category:</b> {country}\n"
            f"<b>━ Region:</b> {country}\n"
            f"<b>━ Number:</b> {formatted_phone}📞\n"
            f"<b>━ OTP:</b> <code>{otp_code}</code>💬\n"
            f"<b>━ User:</b> {formatted_user}👤\n"
            f"<b>━ Status:</b> OTP Delivered ✅\n\n"
            f"<b>🤖 @CUTE_OTP_SELLER_BOT</b>\n\n"
            f"🔝"
        )
        
        # Create entities for custom emojis
        entities = [
            {
                "type": "custom_emoji",
                "offset": 0,
                "length": 1,
                "custom_emoji_id": self.TOP_EMOJI
            },
            {
                "type": "custom_emoji",
                "offset": len(text) - 1,
                "length": 1,
                "custom_emoji_id": self.BOTTOM_EMOJI
            }
        ]
        
        return self._send_message(text, entities)
    
    def log_recharge_approved(self, user_id: int, amount: float, 
                             method: str = "UPI", utr: str = None) -> bool:
        """
        Log when recharge is approved
        """
        # Format data
        formatted_user = self._format_user_id(user_id)
        utr_display = f" | UTR: {utr[:4]}****{utr[-2:]}" if utr and len(utr) > 6 else ""
        
        # Create message
        text = (
            f"🔝\n\n"
            f"<b>💰 RECHARGE APPROVED! 💰</b>\n\n"
            f"<b>User:</b> {formatted_user}\n"
            f"<b>Amount:</b> ₹{amount:,.0f}\n"
            f"<b>Method:</b> {method}{utr_display}\n"
            f"<b>Status:</b> Balance Updated ✅\n\n"
            f"🔝"
        )
        
        # Entities for custom emojis
        entities = [
            {"type": "custom_emoji", "offset": 0, "length": 1, "custom_emoji_id": self.TOP_EMOJI},
            {"type": "custom_emoji", "offset": len(text) - 1, "length": 1, "custom_emoji_id": self.BOTTOM_EMOJI}
        ]
        
        return self._send_message(text, entities)
    
    def log_withdrawal_approved(self, user_id: int, amount: float, 
                                method: str = "UPI", account: str = None) -> bool:
        """
        Log when withdrawal is approved
        """
        # Format data
        formatted_user = self._format_user_id(user_id)
        
        # Mask account details
        if account and len(account) > 4:
            account = f"{account[:4]}****{account[-2:]}"
        
        # Create message
        text = (
            f"🔝\n\n"
            f"<b>💸 WITHDRAWAL APPROVED! 💸</b>\n\n"
            f"<b>User:</b> {formatted_user}\n"
            f"<b>Amount:</b> ₹{amount:,.0f}\n"
            f"<b>Method:</b> {method}\n"
            f"<b>Account:</b> {account if account else 'N/A'}\n"
            f"<b>Status:</b> Processed ✅\n\n"
            f"🔝"
        )
        
        # Entities for custom emojis
        entities = [
            {"type": "custom_emoji", "offset": 0, "length": 1, "custom_emoji_id": self.TOP_EMOJI},
            {"type": "custom_emoji", "offset": len(text) - 1, "length": 1, "custom_emoji_id": self.BOTTOM_EMOJI}
        ]
        
        return self._send_message(text, entities)
    
    def log_custom(self, title: str, emoji: str = "📌", **kwargs) -> bool:
        """
        Send custom log with key-value pairs
        """
        # Format data
        formatted_data = []
        for key, value in kwargs.items():
            if "user" in key.lower() and value:
                value = self._format_user_id(value)
            elif "phone" in key.lower() and value:
                value = self._format_phone(value)
            formatted_data.append(f"<b>{key}:</b> {value}")
        
        # Create message
        text = (
            f"🔝\n\n"
            f"<b>{emoji} {title} {emoji}</b>\n\n"
            f"{chr(10).join(formatted_data)}\n\n"
            f"🔝"
        )
        
        # Entities for custom emojis
        entities = [
            {"type": "custom_emoji", "offset": 0, "length": 1, "custom_emoji_id": self.TOP_EMOJI},
            {"type": "custom_emoji", "offset": len(text) - 1, "length": 1, "custom_emoji_id": self.BOTTOM_EMOJI}
        ]
        
        return self._send_message(text, entities)


# Global instance
_telegram_logger = None

def init_logger(bot_token: str, log_channel_id: str, 
                support_link: str = "https://t.me/+qJCnoSZgjocyODdl", 
                buy_link: str = "https://t.me/CUTE_OTP_SELLER_BOT"):
    """Initialize the global telegram logger"""
    global _telegram_logger
    _telegram_logger = TelegramLogger(bot_token, log_channel_id, support_link, buy_link)
    return _telegram_logger

def get_logger():
    """Get the global telegram logger instance"""
    global _telegram_logger
    if _telegram_logger is None:
        raise ValueError("Logger not initialized. Call init_logger() first.")
    return _telegram_logger

# Async logging functions
def log_purchase_async(user_id: int, country: str, price: float, phone: str):
    """Log purchase in background thread"""
    def _log():
        try:
            logger = get_logger()
            logger.log_purchase(user_id, country, price, phone)
        except Exception as e:
            logging.error(f"Async purchase log failed: {e}")
    
    threading.Thread(target=_log, daemon=True).start()

def log_otp_received_async(user_id: int, phone: str, otp_code: str, country: str, price: float):
    """Log OTP receipt in background thread"""
    def _log():
        try:
            logger = get_logger()
            logger.log_otp_received(user_id, phone, otp_code, country, price)
        except Exception as e:
            logging.error(f"Async OTP log failed: {e}")
    
    threading.Thread(target=_log, daemon=True).start()

def log_recharge_approved_async(user_id: int, amount: float, method: str = "UPI", utr: str = None):
    """Log recharge approval in background thread"""
    def _log():
        try:
            logger = get_logger()
            logger.log_recharge_approved(user_id, amount, method, utr)
        except Exception as e:
            logging.error(f"Async recharge log failed: {e}")
    
    threading.Thread(target=_log, daemon=True).start()

def log_withdrawal_approved_async(user_id: int, amount: float, method: str = "UPI", account: str = None):
    """Log withdrawal approval in background thread"""
    def _log():
        try:
            logger = get_logger()
            logger.log_withdrawal_approved(user_id, amount, method, account)
        except Exception as e:
            logging.error(f"Async withdrawal log failed: {e}")
    
    threading.Thread(target=_log, daemon=True).start()

def log_custom_async(title: str, emoji: str = "📌", **kwargs):
    """Send custom log in background thread"""
    def _log():
        try:
            logger = get_logger()
            logger.log_custom(title, emoji, **kwargs)
        except Exception as e:
            logging.error(f"Async custom log failed: {e}")
    
    threading.Thread(target=_log, daemon=True).start()

# Export everything
__all__ = [
    'TelegramLogger',
    'init_logger',
    'get_logger',
    'log_purchase_async',
    'log_otp_received_async',
    'log_recharge_approved_async',
    'log_withdrawal_approved_async',
    'log_custom_async'
    ]
