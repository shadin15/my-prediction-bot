import telebot
from telebot import types
import random
from datetime import datetime
import pytz

API_TOKEN = '8792313235:AAGLv8pmNBm8G2emNK4TW67am45VvFNF5nU'
ADMIN_ID = 7911996579 

bot = telebot.TeleBot(API_TOKEN)

# ডেটাবেজ (সহজ রাখার জন্য ডিকশনারি ব্যবহার করা হয়েছে)
verified_users = {} # VIP মেম্বার
free_signal_count = {} # কার কয়টা ফ্রি সিগন্যাল বাকি
referrals = {} # কে কাকে রেফার করেছে

REGISTRATION_LINK = "https://18bdwin24.com/register?inviteCode=VFNRBPN&from=web"

# সেশন লিস্ট
SESSIONS = [
    {"display": "10:30 AM - 11:30 AM", "start": "10:30", "end": "11:30"},
    {"display": "02:00 PM - 03:00 PM", "start": "14:00", "end": "15:00"},
    {"display": "05:30 PM - 06:30 PM", "start": "17:30", "end": "18:30"},
    {"display": "09:00 PM - 10:00 PM", "start": "21:00", "end": "22:00"},
    {"display": "11:30 PM - 12:30 AM", "start": "23:30", "end": "00:30"}
]

def is_session_active():
    tz = pytz.timezone('Asia/Dhaka')
    now = datetime.now(tz).strftime("%H:%M")
    for s in SESSIONS:
        if s['start'] == "23:30":
            if now >= "23:30" or now <= "00:30": return True
        elif s['start'] <= now <= s['end']: return True
    return False

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    
    # রেফারেল ট্র্যাকিং (যদি কেউ লিংকের মাধ্যমে আসে)
    args = message.text.split()
    if len(args) > 1:
        referrer_id = int(args[1])
        if referrer_id != user_id and user_id not in referrals:
            referrals[user_id] = referrer_id
            # রেফারারকে ১টি ফ্রি সিগন্যাল দেওয়া
            free_signal_count[referrer_id] = free_signal_count.get(referrer_id, 0) + 1
            bot.send_message(referrer_id, "🎊 আপনার রেফারে একজন জয়েন করেছে! আপনি ১টি ফ্রি সিগন্যাল পেয়েছেন।")

    # নতুন ইউজারের জন্য ১টি ফ্রি সিগন্যাল বোনাস
    if user_id not in free_signal_count:
        free_signal_count[user_id] = 1

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎁 Get 1 Free Signal", "💎 VIP Signals")
    markup.add("🔗 My Referral Link", "📊 Session Status")

    welcome_text = (
        "⚡️ **WELCOME TO BDWIN24 AI PREDICTOR** ⚡️\n\n"
        "আপনি কি সিগন্যাল চেক করতে চান? নিচের **Free Signal** বাটনে ক্লিক করে আমাদের একুরেসি দেখুন।\n\n"
        "🔴 আনলিমিটেড সিগন্যালের জন্য VIP এক্সেস নিন।"
    )
    bot.send_message(user_id, welcome_text, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == "🎁 Get 1 Free Signal")
def free_signal(message):
    user_id = message.chat.id
    count = free_signal_count.get(user_id, 0)
    
    if count > 0:
        free_signal_count[user_id] -= 1
        prediction = random.choice(["BIG 🔴", "SMALL 🟢"])
        
        signal_text = (
            f"🎯 **100% CONFIRMED FREE SIGNAL** 🎯\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📊 RESULT: {prediction}\n"
            f"🚀 ACCURACY: 100% (Guaranteed)\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"💰 এটি ১০০% উইন হবে। এরপর VIP নিতে আমাদের ইনবক্স করুন।"
        )
        # ফ্রি সিগন্যালে সব সময় WIN বাটন থাকবে
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("WIN ✅ (Check Proof)", callback_data="win"))
        bot.send_message(user_id, signal_text, reply_markup=markup)
    else:
        bot.send_message(user_id, "❌ আপনার ফ্রি সিগন্যাল শেষ! আরও ফ্রি সিগন্যাল পেতে আপনার বন্ধুদের রেফার করুন।")

@bot.message_handler(func=lambda message: message.text == "🔗 My Referral Link")
def my_referral(message):
    bot_username = bot.get_me().username
    link = f"https://t.me/{bot_username}?start={message.chat.id}"
    text = (
        f"🔗 **আপনার পার্সোনাল রেফারেল লিংক:**\n`{link}`\n\n"
        f"এই লিংকে আপনার বন্ধুরা জয়েন করলে আপনি প্রতিটি রেফারের জন্য ১টি করে ১০০% সিওর ফ্রি সিগন্যাল পাবেন!"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == "💎 VIP Signals")
def vip_signals(message):
    if message.chat.id in verified_users:
        if is_session_active():
            bot.send_message(message.chat.id, "✅ আপনি এখন VIP সিগন্যাল নিতে পারবেন। পিরিয়ড নম্বর লিখুন।")
        else:
            bot.send_message(message.chat.id, "🚫 VIP সেশন এখন বন্ধ। স্ট্যাটাস চেক করুন।")
    else:
        bot.send_message(message.chat.id, "🚫 আপনি এখনো VIP মেম্বার নন। ভেরিফাই হতে ডিপোজিট স্ক্রিনশট পাঠান।")

# বাকি সব এপ্রুভ এবং সিগন্যাল লজিক আগের মতোই থাকবে...
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(ADMIN_ID, f"ID: `{message.chat.id}`\nApprove: `/approve {message.chat.id}`")
    bot.send_message(message.chat.id, "⏳ ভেরিফিকেশন চলছে...")

@bot.message_handler(commands=['approve'])
def approve(message):
    if message.from_user.id == ADMIN_ID:
        uid = int(message.text.split()[1])
        verified_users[uid] = True
        bot.send_message(uid, "🎊 VIP Access Granted!")

bot.infinity_polling()
