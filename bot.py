# =============================
# Telegram Attendance / Break Bot
# =============================
# প্রয়োজনীয় লাইব্রেরি:
# pip install pyTelegramBotAPI

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import time

# 🔴 এখানে তোমার BOT TOKEN বসাও
BOT_TOKEN = "8573872197:AAF-WlyLsqOxsuZmh7nd8tXhAuCWvnlOsZs"

bot = telebot.TeleBot(BOT_TOKEN)

# user অনুযায়ী timer রাখার জন্য
user_timers = {}

# -----------------------------
# /start কমান্ড
# -----------------------------
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton("🚻 WC (10 min)", callback_data="wc_10"),
        InlineKeyboardButton("🍽 Eat (30 min)", callback_data="eat_30"),
    )
    keyboard.add(
        InlineKeyboardButton("🚬 Smoke (5 min)", callback_data="smoke_5"),
        InlineKeyboardButton("☕ TW / OW (12 hours)", callback_data="tw_12"),
    )
    keyboard.add(
        InlineKeyboardButton("🔙 Back to site", callback_data="back"),
    )

    bot.send_message(
        message.chat.id,
        "⏰ Select your break:",
        reply_markup=keyboard
    )

# -----------------------------
# Timer function
# -----------------------------
def start_timer(chat_id, user_id, seconds, label):
    time.sleep(seconds)

    # যদি user আগেই back করে দেয়
    if user_id not in user_timers:
        return

    bot.send_message(
        chat_id,
        f"⏰ {label} finished! Please return to site."
    )

    user_timers.pop(user_id, None)

# -----------------------------
# Callback handler
# -----------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    user_name = call.from_user.first_name

    # WC 10 min
    if call.data == "wc_10":
        bot.answer_callback_query(call.id, "WC reminder set (10 min)")
        bot.send_message(chat_id, f"🚻 {user_name} went to WC for 10 minutes")

        t = threading.Thread(
            target=start_timer,
            args=(chat_id, user_id, 10 * 60, "WC break")
        )
        user_timers[user_id] = t
        t.start()

    # Eat 30 min
    elif call.data == "eat_30":
        bot.answer_callback_query(call.id, "Eat reminder set (30 min)")
        bot.send_message(chat_id, f"🍽 {user_name} went to Eat for 30 minutes")

        t = threading.Thread(
            target=start_timer,
            args=(chat_id, user_id, 30 * 60, "Eat break")
        )
        user_timers[user_id] = t
        t.start()

    # Smoke 5 min
    elif call.data == "smoke_5":
        bot.answer_callback_query(call.id, "Smoke reminder set (5 min)")
        bot.send_message(chat_id, f"🚬 {user_name} went to Smoke for 5 minutes")

        t = threading.Thread(
            target=start_timer,
            args=(chat_id, user_id, 5 * 60, "Smoke break")
        )
        user_timers[user_id] = t
        t.start()

    # TW / OW 12 hours
    elif call.data == "tw_12":
        bot.answer_callback_query(call.id, "TW/OW started (12 hours)")
        bot.send_message(chat_id, f"☕ {user_name} started TW / OW for 12 hours")

        t = threading.Thread(
            target=start_timer,
            args=(chat_id, user_id, 12 * 60 * 60, "TW / OW")
        )
        user_timers[user_id] = t
        t.start()

    # Back to site
    elif call.data == "back":
        if user_id in user_timers:
            user_timers.pop(user_id, None)
            bot.answer_callback_query(call.id, "Welcome back!")
            bot.send_message(chat_id, f"✅ {user_name} is back to site")
        else:
            bot.answer_callback_query(call.id, "No active break")

# -----------------------------
# Bot start
# -----------------------------
print("🤖 Bot is running...")
bot.infinity_polling()
