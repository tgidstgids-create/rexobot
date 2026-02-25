"""
Fixed Telegram Logging Module for OTP Bot
Custom Emoji Supported
No HTML Parsing Errors
"""

import logging
import threading
from typing import Optional

logger = logging.getLogger(__name__)


class TelegramLogger:
    def __init__(
        self,
        bot_token: str,
        log_channel_id: str,
        support_link: str = "https://t.me/+qJCnoSZgjocyODdl",
        buy_link: str = "https://t.me/CUTE_OTP_SELLER_BOT",
    ):
        self.bot_token = bot_token
        self.log_channel_id = log_channel_id
        self.support_link = support_link.strip()
        self.buy_link = buy_link.strip()
        self._bot = None
        self._init_bot()

    def _init_bot(self):
        try:
            import telebot
            from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

            self._bot = telebot.TeleBot(self.bot_token, parse_mode="HTML")
            self.InlineKeyboardMarkup = InlineKeyboardMarkup
            self.InlineKeyboardButton = InlineKeyboardButton

            logger.info("✅ Telegram logger initialized successfully")

        except Exception as e:
            logger.error(f"❌ Telegram logger init failed: {e}")
            self._bot = None

    def _get_buttons(self):
        markup = self.InlineKeyboardMarkup(row_width=2)
        markup.add(
            self.InlineKeyboardButton("🆘 Support", url=self.support_link),
            self.InlineKeyboardButton("🛒 Buy", url=self.buy_link),
        )
        return markup

    def send_log(self, message: str) -> bool:
        if not self._bot:
            logger.error("Telegram bot not initialized")
            return False

        try:
            self._bot.send_message(
                self.log_channel_id,
                message,
                disable_web_page_preview=True,
                reply_markup=self._get_buttons(),
            )
            return True
        except Exception as e:
            logger.error(f"❌ Failed to send Telegram log: {e}")
            return False

    # ==========================
    # PURCHASE LOG
    # ==========================
    def log_purchase(self, user_id: int, country: str, price: float, phone: str):

        TOP_EMOJI = 6120916334873153887
        BOTTOM_EMOJI = 6170205375267082717

        formatted_phone = self._mask_phone(phone)
        formatted_user = self._mask_user(user_id)

        message = (
            f"<emoji id='{TOP_EMOJI}'></emoji>\n\n"
            f"<b>🔥 NEW ACCOUNT SOLD! 🔥</b>\n\n"
            f"<b>✚ Category:</b> {country}\n"
            f"<b>✚ Region:</b> {country}\n"
            f"<b>✚ Number:</b> {formatted_phone} 📞\n"
            f"<b>✚ User:</b> {formatted_user} 👤\n"
            f"<b>✚ Status:</b> Verified & Delivered ✅\n\n"
            f"<b>🤖 @CUTE_OTP_SELLER_BOT</b>\n\n"
            f"<emoji id='{BOTTOM_EMOJI}'></emoji>"
        )

        return self.send_log(message)

    # ==========================
    # OTP RECEIVED LOG
    # ==========================
    def log_otp_received(
        self, user_id: int, phone: str, otp_code: str, country: str, price: float
    ):

        TOP_EMOJI = 6120916334873153887
        BOTTOM_EMOJI = 6170205375267082717

        formatted_phone = self._mask_phone(phone)
        formatted_user = self._mask_user(user_id)

        message = (
            f"<emoji id='{TOP_EMOJI}'></emoji>\n\n"
            f"<b>🔐 OTP RECEIVED! 🔐</b>\n\n"
            f"<b>━ Category:</b> {country}\n"
            f"<b>━ Region:</b> {country}\n"
            f"<b>━ Number:</b> {formatted_phone} 📞\n"
            f"<b>━ OTP:</b> <code>{otp_code}</code>\n"
            f"<b>━ User:</b> {formatted_user} 👤\n"
            f"<b>━ Status:</b> OTP Delivered ✅\n\n"
            f"<b>🤖 @CUTE_OTP_SELLER_BOT</b>\n\n"
            f"<emoji id='{BOTTOM_EMOJI}'></emoji>"
        )

        return self.send_log(message)

    # ==========================
    # RECHARGE APPROVED LOG
    # ==========================
    def log_recharge_approved(
        self, user_id: int, amount: float, method: str = "UPI", utr: Optional[str] = None
    ):

        TOP_EMOJI = 6120916334873153887
        BOTTOM_EMOJI = 6170205375267082717

        formatted_user = self._mask_user(user_id)
        utr_display = f"\n<b>UTR:</b> {utr}" if utr else ""

        message = (
            f"<emoji id='{TOP_EMOJI}'></emoji>\n\n"
            f"<b>💰 RECHARGE APPROVED! 💰</b>\n\n"
            f"<b>User:</b> {formatted_user}\n"
            f"<b>Amount:</b> ₹{amount:,.0f}\n"
            f"<b>Method:</b> {method}"
            f"{utr_display}\n"
            f"<b>Status:</b> Balance Updated ✅\n\n"
            f"<emoji id='{BOTTOM_EMOJI}'></emoji>"
        )

        return self.send_log(message)

    # ==========================
    # HELPER FUNCTIONS
    # ==========================
    def _mask_phone(self, phone: str) -> str:
        try:
            digits = "".join(filter(str.isdigit, str(phone)))
            if len(digits) >= 10:
                return digits[:3] + "****" + digits[-2:]
            return digits[:3] + "****"
        except:
            return "N/A"

    def _mask_user(self, user_id: int) -> str:
        try:
            s = str(user_id)
            if len(s) > 4:
                return s[:3] + "***" + s[-2:]
            return s[:2] + "***"
        except:
            return "User"


# ==========================
# GLOBAL INSTANCE
# ==========================

telegram_logger = None


def init_logger(bot_token: str, log_channel_id: str):
    global telegram_logger
    telegram_logger = TelegramLogger(bot_token, log_channel_id)
    return telegram_logger


def get_logger():
    if telegram_logger is None:
        raise ValueError("Logger not initialized")
    return telegram_logger


# ==========================
# ASYNC HELPERS
# ==========================

def log_purchase_async(user_id, country, price, phone):
    threading.Thread(
        target=lambda: get_logger().log_purchase(user_id, country, price, phone),
        daemon=True,
    ).start()


def log_otp_received_async(user_id, phone, otp_code, country, price):
    threading.Thread(
        target=lambda: get_logger().log_otp_received(
            user_id, phone, otp_code, country, price
        ),
        daemon=True,
    ).start()


def log_recharge_approved_async(user_id, amount, method="UPI", utr=None):
    threading.Thread(
        target=lambda: get_logger().log_recharge_approved(
            user_id, amount, method, utr
        ),
        daemon=True,
    ).start()
