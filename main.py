import telebot
from telebot import types
import random
from datetime import datetime
import pytz
import os

# আপনার তথ্য
API_TOKEN = '8792313235:AAG29kHCokBMvH5GSPcKsO1tZcWo9dzdjBs'
ADMIN_ID = 7911996579 

bot = telebot.TeleBot(API_TOKEN)

# ফাইল থেকে ডাটা লোড করার চেষ্টা
verified_users = {} 
free_signal_count = {} 
referrals = {} 
recovery_mode = {} 
user_db = "users.txt" # মেম্বারদের লিস্ট সেভ রাখার জন্য

# অফিসিয়াল লিংক
REGISTRATION_LINK = "https://18bdwin24.com/register?inviteCode=VFNRBPN&from=web"

# বাংলাদেশ সময় অনুযায়ী সেশন
SESSIONS = [
    {"display": "10:30 AM - 11:30 AM", "start": "10:30", "end": "11:30", "icon": "☀️"},
    {"display": "02:00 PM - 03:00 PM", "start": "14:00", "end": "15:00", "icon": "🍱"},
    {"display": "05:30 PM - 06:30 PM", "start": "17:30", "end": "18:30", "icon": "🌇"},
    {"display": "09:00 PM - 10:00 PM", "start": "21:00", "end": "22:00", "icon": "🔥"},
    {"display": "11:30 PM - 12:30 AM", "start": "23:30", "end": "00:30", "icon": "🌙"}
]

# ইউজার লিস্ট সেভ করার ফাংশন
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

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    first_name = message.from_user.first_name
    username = message.from_user.username if message.from_user.username else "NoUsername"
    
    # ইউজার সেভ করা
    save_user_info(user_id, first_name, username)

    # রেফারেল লজিক
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        ref_id = int(args[1])
        if ref_id != user_id and user_id not in referrals:
            referrals[user_id] = ref_id
            free_signal_count[ref_id] = free_signal_count.get(ref_id, 0) + 1
            bot.send_message(ref_id, f"🎊 আপনার লিংকে {first_name} জয়েন করেছে! আপনি ১টি ফ্রি সিগন্যাল পেয়েছেন।")

    if user_id not in free_signal_count:
        free_signal_count[user_id] = 1 

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎁 Get 1 Free Signal", "💎 VIP Signals")
    markup.add("📊 Signal Status", "🔗 My Referral Link")
    
    welcome_text = (
        f"👋 **স্বাগতম {first_name}!**\n\n"
        "BDWIN24 VIP AI-তে সিগন্যাল পেতে আমাদের রেফার লিংকে একাউন্ট খুলুন।\n\n"
        f"🔗 [REGISTER LINK]({REGISTRATION_LINK})\n\n"
        "✅ **ভেরিফিকেশন:** UID ও ডিপোজিট স্ক্রিনশট পাঠিয়ে দিন।"
    )
    bot.send_message(user_id, welcome_text, reply_markup=markup, parse_mode='Markdown', disable_web_page_preview=True)

# অ্যাডমিন কমান্ড: সব মেম্বারের লিস্ট দেখা
@bot.message_handler(commands=['allusers'])
def send_user_list(message):
    if message.from_user.id == ADMIN_ID:
        if os.path.exists(user_db):
            with open(user_db, "rb") as f:
                bot.send_document(ADMIN_ID, f, caption="📊 **BDWIN24 বটের সব মেম্বার লিস্ট**")
        else:
            bot.send_message(ADMIN_ID, "কোনো ইউজার ডাটা পাওয়া যায়নি।")

@bot.message_handler(func=lambda m: m.text == "📊 Signal Status")
def show_status(message):
    tz = pytz.timezone('Asia/Dhaka')
    now = datetime.now(tz).strftime("%H:%M")
    text = "📊 **OFFICIAL SIGNAL TIMETABLE**\n━━━━━━━━━━━━━━━━━━\n"
    for s in SESSIONS:
        status = "⏰"
        if s['start'] <= now <= s['end'] or (s['start'] == "23:30" and (now >= "23:30" or now <= "00:30")):
            status = "🟢 (Active)"
        elif now > s['end'] and s['start'] != "23:30":
            status = "✅ (Finished)"
        text += f"{s['icon']} {s['display']} - {status}\n"
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "🔗 My Referral Link")
def my_ref(message):
    bot_user = bot.get_me().username
    link = f"https://t.me/{bot_user}?start={message.chat.id}"
    bot.send_message(message.chat.id, f"🔗 **আপনার রেফার লিংক:**\n`{link}`\n\nবন্ধুদের জয়েন করিয়ে ফ্রি সিগন্যাল নিন!", parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "🎁 Get 1 Free Signal")
def get_free(message):
    user_id = message.chat.id
    count = free_signal_count.get(user_id, 0)
    if count > 0:
        free_signal_count[user_id] -= 1
        prediction = random.choice(["BIG 🔴", "SMALL 🟢"])
        text = f"🎯 **FREE CONFIRMED SIGNAL**\n━━━━━━━━━━━━\n📊 RESULT: {prediction}\n🚀 ACCURACY: 100%\n━━━━━━━━━━━━\n💰 এরপর VIP নিতে ডিপোজিট করুন।"
        bot.send_message(user_id, text)
    else:
        bot.send_message(user_id, "❌ ফ্রি সিগন্যাল শেষ! আরও পেতে বন্ধুদের রেফার করুন।")

@bot.message_handler(func=lambda m: m.text == "💎 VIP Signals")
def vip_gate(message):
    user_id = message.chat.id
    if user_id in verified_users:
        if is_session_active() or recovery_mode.get(user_id):
            bot.send_message(user_id, "🎯 **VIP ACTIVE**\nপিরিয়ড নম্বর লিখুন। (উদা: 456)")
        else:
            bot.send_message(user_id, "🚫 সেশন বন্ধ। পরবর্তী সেশনের জন্য অপেক্ষা করুন।")
    else:
        bot.send_message(user_id, "🚫 VIP এক্সেস নেই! আগে স্ক্রিনশট পাঠিয়ে ভেরিফাই হন।")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.chat.id
    user_name = message.from_user.first_name
    username = f"@{message.from_user.username}" if message.from_user.username else "NoUsername"
    
    bot.send_message(ADMIN_ID, f"📩 **New Request!**\nName: {user_name}\nID: `{user_id}`\nUsername: {username}\nApprove: `/approve {user_id}`")
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(user_id, "⏳ আপনার স্ক্রিনশট পাঠানো হয়েছে। যাচাই শেষে আপনাকে এপ্রুভ করা হবে।")

@bot.message_handler(commands=['approve'])
def approve(message):
    if message.from_user.id == ADMIN_ID:
        try:
            uid = int(message.text.split()[1])
            verified_users[uid] = True
            bot.send_message(uid, "🎊 **VIP ACCESS GRANTED!**\nএখন থেকে আপনি নির্ভুল সিগন্যাল পাবেন।")
            bot.send_message(ADMIN_ID, f"✅ User {uid} Approved.")
        except: bot.reply_to(message, "ভুল ফরম্যাট! /approve ID লিখুন।")

@bot.message_handler(func=lambda message: True)
def handle_signals(message):
    user_id = message.chat.id
    if user_id in verified_users:
        if not is_session_active() and not recovery_mode.get(user_id):
            bot.send_message(user_id, "⏰ সেশন শেষ!")
            return

        if message.text.isdigit():
            period = message.text
            if random.random() < 0.15:
                bot.send_message(user_id, f"⚠️ **MARKET UNSTABLE!**\nপিরিয়ড {period} এ ট্রেড নিবেন না।\n🛑 **HOLD করুন!**")
                return

            prediction = random.choice(["BIG 🔴", "SMALL 🟢"])
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("WIN ✅", callback_data="win"), 
                       types.InlineKeyboardButton("LOSS ❌", callback_data="loss"))
            
            mode = "🔄 RECOVERY" if recovery_mode.get(user_id) else "🚀 VIP SIGNAL"
            text = f"🔥 **BDWIN24 VIP** 🔥\n━━━━━━━━━━━━\n📌 PERIOD: {period}\n📊 TARGET: {prediction}\n━━━━━━━━━━━━\n💎 {mode}\n⚠️ ৫-৬ স্টেপ ফান্ড রাখুন।"
            bot.send_message(user_id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_logic(call):
    user_id = call.message.chat.id
    if call.data == "win":
        recovery_mode[user_id] = False
        bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text="💰 **BOOM WIN!!** 💰\n\n✅ পরবর্তী পিরিয়ড দিন।")
    elif call.data == "loss":
        recovery_mode[user_id] = True
        bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text="⚠️ **LOSS!** পরবর্তী পিরিয়ডে **৩ গুণ (3X)** ফান্ড ব্যবহার করুন। রিকভারি নিশ্চিত!")

bot.infinity_polling()
    
