"""
Logging Module for OTP Bot
Sends purchase logs, OTP receipts, and recharge approvals to Telegram channel
"""

import logging
import time
from datetime import datetime
from typing import Optional, Dict, Any
import threading

logger = logging.getLogger(__name__)

class TelegramLogger:
    """Sends logs to Telegram channel"""
    
    def __init__(self, bot_token: str, log_channel_id: str):
        """
        Initialize Telegram logger
        
        Args:
            bot_token: Telegram bot token
            log_channel_id: Channel ID where logs will be sent (e.g., "@your_log_channel")
        """
        self.bot_token = bot_token
        self.log_channel_id = log_channel_id
        self._bot = None
        self._init_bot()
        
    def _init_bot(self):
        """Initialize Telegram bot for logging"""
        try:
            import telebot
            self._bot = telebot.TeleBot(self.bot_token)
            logger.info(f"✅ Telegram logger initialized for channel: {self.log_channel_id}")
        except ImportError:
            logger.error("❌ Failed to import telebot. Install with: pip install pyTelegramBotAPI")
            self._bot = None
        except Exception as e:
            logger.error(f"❌ Failed to initialize Telegram logger: {e}")
            self._bot = None
    
    def send_log(self, message: str, parse_mode: str = "HTML") -> bool:
        """
        Send log message to Telegram channel
        
        Args:
            message: The message to send
            parse_mode: HTML or Markdown
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self._bot:
            logger.error("Telegram bot not initialized")
            return False
        
        try:
            # Send message to channel
            self._bot.send_message(
                self.log_channel_id,
                message,
                parse_mode=parse_mode,
                disable_web_page_preview=True
            )
            return True
        except Exception as e:
            logger.error(f"Failed to send log to Telegram: {e}")
            return False
    
    def log_purchase(self, user_id: int, country: str, price: float, phone: str) -> bool:
        """
        Log when user buys an account with stylish UI
        
        Args:
            user_id: User ID who made purchase
            country: Country of account
            price: Price paid
            phone: Phone number purchased
            
        Returns:
            bool: Success status
        """
        # Extract first 3-4 digits
        first_digits = ""
        if phone:
            try:
                # Get last 10 digits and then first 4 of those
                digits = phone[-10:] if len(phone) >= 10 else phone
                first_digits = digits[:4]
            except:
                first_digits = phone[:4] if len(phone) > 4 else phone
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%d-%m-%Y")
        
        message = (
            f"<blockquote>🛒 <b>NEW ACCOUNT PURCHASE</b> 🛒\n\n"
            f"🌍 <b>Country:</b> {country}\n"
            f"💰 <b>Price:</b> ₹{price}\n"
            f"📱 <b>Number:</b> <code>{first_digits}XXX</code>\n"
            f"👤 <b>User:</b> <a href='tg://user?id={user_id}'>{user_id}</a>\n"
            f"⏰ <b>Time:</b> {timestamp}\n"
            f"📅 <b>Date:</b> {date}\n"
            f"</blockquote>\n\n"
            f"✅ Purchase completed successfully!"
        )
        
        return self.send_log(message)
    
    def log_otp_received(self, user_id: int, phone: str, otp_code: str, 
                         country: str, price: float) -> bool:
        """
        Log when OTP is received for a purchase with stylish UI
        
        Args:
            user_id: User ID who purchased
            phone: Phone number
            otp_code: OTP code received
            country: Country of account
            price: Price paid
            
        Returns:
            bool: Success status
        """
        # Extract first 3-4 digits
        first_digits = ""
        if phone:
            try:
                digits = phone[-10:] if len(phone) >= 10 else phone
                first_digits = digits[:4]
            except:
                first_digits = phone[:4] if len(phone) > 4 else phone
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%d-%m-%Y")
        
        message = (
            f"<blockquote>🔐 <b>OTP RECEIVED</b> 🔐\n\n"
            f"📱 <b>Number:</b> <code>{first_digits}XXX</code>\n"
            f"🌍 <b>Country:</b> {country}\n"
            f"💰 <b>Price:</b> ₹{price}\n"
            f"🔢 <b>OTP:</b> <code>{otp_code}</code>\n"
            f"👤 <b>User:</b> <a href='tg://user?id={user_id}'>{user_id}</a>\n"
            f"⏰ <b>Time:</b> {timestamp}\n"
            f"📅 <b>Date:</b> {date}\n"
            f"</blockquote>\n\n"
            f"⚡ OTP delivered successfully!"
        )
        
        return self.send_log(message)
    
    def log_recharge_approved(self, user_id: int, amount: float, 
                             method: str = "UPI", utr: str = None) -> bool:
        """
        Log when recharge is approved with stylish UI
        
        Args:
            user_id: User ID who recharged
            amount: Amount recharged
            method: Payment method (UPI/Crypto)
            utr: UTR number (for UPI payments)
            
        Returns:
            bool: Success status
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%d-%m-%Y")
        
        utr_display = f" | UTR: <code>{utr}</code>" if utr else ""
        
        message = (
            f"<blockquote>💰 <b>RECHARGE APPROVED</b> 💰\n\n"
            f"👤 <b>User:</b> <a href='tg://user?id={user_id}'>{user_id}</a>\n"
            f"💵 <b>Amount:</b> ₹{amount}\n"
            f"💳 <b>Method:</b> {method}{utr_display}\n"
            f"⏰ <b>Time:</b> {timestamp}\n"
            f"📅 <b>Date:</b> {date}\n"
            f"</blockquote>\n\n"
            f"✅ Balance updated successfully!"
        )
        
        return self.send_log(message)

# Create global instance
telegram_logger = None

def init_logger(bot_token: str, log_channel_id: str = "@your_log_channel"):
    """Initialize the global telegram logger"""
    global telegram_logger
    telegram_logger = TelegramLogger(bot_token, log_channel_id)
    return telegram_logger

def get_logger() -> TelegramLogger:
    """Get the global telegram logger instance"""
    global telegram_logger
    if telegram_logger is None:
        raise ValueError("Telegram logger not initialized. Call init_logger() first.")
    return telegram_logger

# Helper functions for common logging scenarios
def log_purchase_async(user_id: int, country: str, price: float, phone: str):
    """Log purchase in background thread"""
    def _log():
        try:
            logger = get_logger()
            logger.log_purchase(user_id, country, price, phone)
        except Exception as e:
            logging.error(f"Failed to log purchase: {e}")
    
    thread = threading.Thread(target=_log, daemon=True)
    thread.start()

def log_otp_received_async(user_id: int, phone: str, otp_code: str, country: str, price: float):
    """Log OTP receipt in background thread"""
    def _log():
        try:
            logger = get_logger()
            logger.log_otp_received(user_id, phone, otp_code, country, price)
        except Exception as e:
            logging.error(f"Failed to log OTP: {e}")
    
    thread = threading.Thread(target=_log, daemon=True)
    thread.start()

def log_recharge_approved_async(user_id: int, amount: float, method: str = "UPI", utr: str = None):
    """Log recharge approval in background thread"""
    def _log():
        try:
            logger = get_logger()
            logger.log_recharge_approved(user_id, amount, method, utr)
        except Exception as e:
            logging.error(f"Failed to log recharge: {e}")
    
    thread = threading.Thread(target=_log, daemon=True)
    thread.start()

# Export everything
__all__ = [
    'TelegramLogger',
    'init_logger',
    'get_logger',
    'log_purchase_async',
    'log_otp_received_async',
    'log_recharge_approved_async',
    'telegram_logger'
]
