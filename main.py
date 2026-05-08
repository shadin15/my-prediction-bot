import telebot
from telebot import types
import random
from datetime import datetime
import pytz
import os

# --- কনফিগারেশন ---
API_TOKEN = '8792313235:AAG29kHCokBMvH5GSPcKsO1tZcWo9dzdjBs'
ADMIN_ID = 7911996579 
REGISTRATION_LINK = "https://18bdwin24.com/register?inviteCode=VFNRBPN&from=web"

bot = telebot.TeleBot(API_TOKEN)

# --- ডাটাবেজ ট্র্যাকিং ---
verified_users = {} 
free_signal_count = {} 
referrals = {} 
recovery_mode = {} 
user_db = "users.txt" 

# --- সেশন লিস্ট ---
SESSIONS = [
    {"display": "10:30 AM - 11:30 AM", "start": "10:30", "end": "11:30", "icon": "☀️"},
    {"display": "02:00 PM - 03:00 PM", "start": "14:00", "end": "15:00", "icon": "🍱"},
    {"display": "05:30 PM - 06:30 PM", "start": "17:30", "end": "18:30", "icon": "🌇"},
    {"display": "09:00 PM - 10:00 PM", "start": "21:00", "end": "22:00", "icon": "🔥"},
    {"display": "11:30 PM - 12:30 AM", "start": "23:30", "end": "00:30", "icon": "🌙"}
]

def save_user_info(user_id, first_name, username):
    entry = f"ID: {user_id} | Name: {first_name} | Username: @{username}\n"
    if not os.path.exists(user_db):
        with open(user_db, "w") as f: f.write(entry)
    else:
        with open(user_db, "r") as f:
            if str(user_id) in f.read(): return
        with open(user_db, "a") as f: f.write(entry)

def is_session_active():
    tz = pytz.timezone('Asia/Dhaka')
    now = datetime.now(tz).strftime("%H:%M")
    for s in SESSIONS:
        if s['start'] == "23:30":
            if now >= "23:30" or now <= "00:30": return True
        elif s['start'] <= now <= s['end']: return True
    return False

# --- টাইম টেবিল ফরম্যাট (আপনার রিকোয়েস্ট অনুযায়ী) ---
def get_session_status_text():
    tz = pytz.timezone('Asia/Dhaka')
    now = datetime.now(tz).strftime("%H:%M")
    text = "📊 **OFFICIAL SIGNAL TIMETABLE**\n━━━━━━━━━━━━━━━━━━\n"
    
    for s in SESSIONS:
        status = "⏰ (Upcoming)"
        if s['start'] <= now <= s['end'] or (s['start'] == "23:30" and (now >= "23:30" or now <= "00:30")):
            status = "🟢 Active Now"
        elif now > s['end'] and s['start'] != "23:30":
            status = "✅ Finished"
        text += f"{s['icon']} {s['display']} - {status}\n"
    
    # নির্দেশিকা অংশ
    text += "\n━━━━━━━━━━━━━━━━━━\n"
    text += "📖 **কিভাবে বুঝবেন সেশন শুরু কি না?**\n\n"
    text += "🟢 **Active Now:** এর মানে সিগন্যাল এখন চলছে, দ্রুত সিগন্যাল নিন।\n"
    text += "✅ **Finished:** এর মানে এই সময়ের সিগন্যাল দেওয়া শেষ হয়ে গেছে।\n"
    text += "⏰ **Upcoming:** এর মানে এই সেশনটি এখনো শুরু হয়নি, অপেক্ষা করুন।\n\n"
    text += "💡 সেশন চলাকালীন সময়েই কেবল VIP সিগন্যাল কাজ করবে।"
    return text

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    save_user_info(user_id, message.from_user.first_name, message.from_user.username if message.from_user.username else "NoUsername")
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎁 Get 1 Free Signal", "💎 VIP Signals")
    markup.add("📊 Session Status", "🔗 My Referral Link")
    
    welcome_text = (
        f"👋 **স্বাগতম {message.from_user.first_name}!**\n\n"
        "BDWIN24 VIP AI-তে সিগন্যাল পেতে আমাদের রেফার লিংকে একাউন্ট থাকা জরুরি।\n\n"
        f"🔗 [REGISTER LINK]({REGISTRATION_LINK})\n\n"
        "✅ **ভেরিফিকেশন:** UID ও ডিপোজিট স্ক্রিনশট পাঠিয়ে দিন।"
    )
    bot.send_message(user_id, welcome_text, reply_markup=markup, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(func=lambda m: m.text == "📊 Session Status")
def show_status(message):
    bot.send_message(message.chat.id, get_session_status_text(), parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "🔗 My Referral Link")
def my_ref(message):
    bot_username = bot.get_me().username
    link = f"https://t.me/{bot_username}?start={message.chat.id}"
    bot.send_message(message.chat.id, f"🔗 **আপনার রেফারেল লিংক:**\n`{link}`\n\nবন্ধুদের জয়েন করিয়ে ফ্রি সিগন্যাল নিন!", parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "🎁 Get 1 Free Signal")
def free_sig(message):
    user_id = message.chat.id
    count = free_signal_count.get(user_id, 0)
    if count > 0:
        free_signal_count[user_id] -= 1
        res = random.choice(["BIG 🔴", "SMALL 🟢"])
        text = f"🎯 **FREE CONFIRMED SIGNAL**\n━━━━━━━━━━━━\n📊 RESULT: {res}\n🚀 ACCURACY: 100%\n━━━━━━━━━━━━\n💰 এটি ১০০% উইন হবে। VIP নিতে ডিপোজিট করুন।"
        bot.send_message(user_id, text)
    else:
        bot.send_message(user_id, "❌ ফ্রি সিগন্যাল শেষ! বন্ধুদের রেফার করুন।")

@bot.message_handler(func=lambda m: m.text == "💎 VIP Signals")
def vip_check(message):
    user_id = message.chat.id
    if user_id in verified_users:
        if is_session_active() or recovery_mode.get(user_id, False):
            bot.send_message(user_id, "🎯 **VIP সেশন সক্রিয়!**\nপিরিয়ড নম্বর ও আগের সংখ্যা দিন (উদা: 456 2)")
        else:
            bot.send_message(user_id, "🚫 সেশন এখন বন্ধ। সময়সূচী চেক করুন।")
    else:
        bot.send_message(user_id, "🚫 VIP এক্সেস নেই! আগে স্ক্রিনশট পাঠিয়ে ভেরিফাই হন।")

@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    user_id = message.chat.id
    username = f"@{message.from_user.username}" if message.from_user.username else "No UserID"
    bot.send_message(ADMIN_ID, f"📩 **New VIP Request!**\nName: {message.from_user.first_name}\nID: `{user_id}`\nUsername: {username}\n\nApprove: `/approve {user_id}`")
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(user_id, "⏳ আপনার স্ক্রিনশট অ্যাডমিন চেক করছে। ভেরিফাই হলে মেসেজ পাবেন।")

@bot.message_handler(commands=['approve'])
def approve_user(message):
    if message.from_user.id == ADMIN_ID:
        try:
            uid = int(message.text.split()[1])
            verified_users[uid] = True
            bot.send_message(uid, "🎊 **CONGRATULATIONS!**\nআপনার VIP এক্সেস এখন একটিভ। আপনি এখন সিগন্যাল নিতে পারবেন।")
            bot.send_message(ADMIN_ID, f"✅ User {uid} Approved.")
        except: bot.reply_to(message, "ভুল ফরম্যাট! /approve ID দিন।")

@bot.message_handler(commands=['allusers'])
def list_users(message):
    if message.from_user.id == ADMIN_ID:
        if os.path.exists(user_db):
            with open(user_db, "rb") as f:
                bot.send_document(ADMIN_ID, f, caption="📊 **All Bot Members List**")
        else: bot.send_message(ADMIN_ID, "No users found.")

@bot.message_handler(func=lambda message: True)
def process_vip_signals(message):
    user_id = message.chat.id
    if user_id in verified_users:
        if not is_session_active() and not recovery_mode.get(user_id, False):
            bot.send_message(user_id, "⏰ সেশন শেষ!")
            return
        data = message.text.split()
        if len(data) >= 1 and data[0].isdigit():
            period = data[0]
            if random.random() < 0.15:
                bot.send_message(user_id, f"⚠️ **MARKET UNSTABLE!**\nপিরিয়ড {period} এ ট্রেড নিবেন না।\n🛑 **HOLD করুন!**")
                return
            prediction = random.choice(["BIG 🔴", "SMALL 🟢"])
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("WIN ✅", callback_data="win"), 
                       types.InlineKeyboardButton("LOSS ❌", callback_data="loss"))
            mode_label = "🔄 RECOVERY" if recovery_mode.get(user_id, False) else "🚀 VIP SIGNAL"
            text = f"🔥 **BDWIN24 VIP** 🔥\n━━━━━━━━━━━━\n📌 PERIOD: {period}\n📊 TARGET: {prediction}\n━━━━━━━━━━━━\n💎 {mode_label}\n⚠️ ৫-৬ স্টেপ ফান্ড মেইনটেইন করুন।"
            bot.send_message(user_id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.message.chat.id
    if call.data == "win":
        recovery_mode[user_id] = False
        bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text="💰 **BOOM WIN!!** 💰\n\n✅ পরবর্তী পিরিয়ড ও লাস্ট সংখ্যা দিন।")
    elif call.data == "loss":
        recovery_mode[user_id] = True
        bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text="⚠️ **LOSS!** পরবর্তী পিরিয়ডে **৩ গুণ (3X)** ফান্ড ব্যবহার করুন।")

bot.infinity_polling()
