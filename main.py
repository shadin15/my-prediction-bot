import telebot
from telebot import types
import random
from datetime import datetime
import pytz

API_TOKEN = '8792313235:AAGLv8pmNBm8G2emNK4TW67am45VvFNF5nU'
ADMIN_ID = 7911996579 

bot = telebot.TeleBot(API_TOKEN)
verified_users = {}

REGISTRATION_LINK = "https://18bdwin24.com/register?inviteCode=VFNRBPN&from=web"

# সেশন ডাটা (বাংলাদেশ সময় অনুযায়ী)
SESSIONS = [
    {"display": "10:30 AM - 11:30 AM", "start": "10:30", "end": "11:30", "icon": "☀️"},
    {"display": "02:00 PM - 03:00 PM", "start": "14:00", "end": "15:00", "icon": "🍱"},
    {"display": "05:30 PM - 06:30 PM", "start": "17:30", "end": "18:30", "icon": "🌇"},
    {"display": "09:00 PM - 10:00 PM", "start": "21:00", "end": "22:00", "icon": "🔥"},
    {"display": "11:30 PM - 12:30 AM", "start": "23:30", "end": "00:30", "icon": "🌙"}
]

def get_live_status():
    tz = pytz.timezone('Asia/Dhaka')
    now = datetime.now(tz).strftime("%H:%M")
    status_text = "📊 **আজকের সেশন স্ট্যাটাস:**\n\n"
    
    for s in SESSIONS:
        start_time = s['start']
        end_time = s['end']
        
        # সেশন শেষ হয়েছে কিনা চেক (মাঝরাতের সেশন হ্যান্ডেলিং সহ)
        is_ended = False
        if start_time == "23:30": # লাস্ট সেশন
            if "00:30" < now < "10:30": is_ended = True
        else:
            if now > end_time: is_ended = True
            
        # সেশন বর্তমানে চলছে কিনা
        is_active = False
        if start_time == "23:30":
            if now >= "23:30" or now <= "00:30": is_active = True
        else:
            if start_time <= now <= end_time: is_active = True

        # সিম্বল সেট করা
        if is_ended:
            symbol = "✅" # সেশন শেষ
            label = "(Finished)"
        elif is_active:
            symbol = "🟢" # সেশন চলছে
            label = "(Active Now)"
        else:
            symbol = "⏰" # সেশন সামনে আসবে
            label = "(Upcoming)"
            
        status_text += f"{symbol} {s['icon']} **{s['display']}** {label}\n"
    
    return status_text

def is_session_active():
    tz = pytz.timezone('Asia/Dhaka')
    now = datetime.now(tz).strftime("%H:%M")
    for s in SESSIONS:
        if s['start'] == "23:30":
            if now >= "23:30" or now <= "00:30": return True
        elif s['start'] <= now <= s['end']:
            return True
    return False

@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "⚡️ **BDWIN24 OFFICIAL AI PREDICTOR** ⚡️\n\n"
        "মার্কেটের সবথেকে নিখুঁত AI সিগন্যাল পেতে আমাদের সাথেই থাকুন।\n\n"
        f"🔗 [OFFICIAL REGISTER LINK]({REGISTRATION_LINK})\n\n"
        "✅ **ভেরিফিকেশন:** একাউন্ট খুলে আপনার UID প্রোফাইল ও ডিপোজিটের স্ক্রিনশট এখানে পাঠান।"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.chat.id
    username = f"@{message.from_user.username}" if message.from_user.username else "N/A"
    
    bot.send_message(ADMIN_ID, f"📩 **New Request!**\nID: `{user_id}`\nUsername: {username}\nApprove: `/approve {user_id}`")
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "⏳ আপনার স্ক্রিনশট অ্যাডমিনের কাছে পাঠানো হয়েছে। যাচাই শেষে আপনাকে এপ্রুভ করা হবে।")

@bot.message_handler(commands=['approve'])
def approve(message):
    if message.from_user.id == ADMIN_ID:
        try:
            uid = int(message.text.split()[1])
            verified_users[uid] = True
            bot.send_message(uid, "🎊 **VIP ACCESS ACTIVATED!**\n\nআপনি এখন অফিশিয়াল সিগন্যাল পাওয়ার যোগ্য।\n👉 পিরিয়ডের **শেষ ৩ ডিজিট** লিখে মেসেজ দিন।")
            bot.send_message(ADMIN_ID, f"✅ User `{uid}` Approved!")
        except: bot.reply_to(message, "ব্যবহার করুন: `/approve ID`")

@bot.message_handler(func=lambda message: True)
def give_signal(message):
    if message.chat.id in verified_users:
        if not is_session_active():
            # সেশন বন্ধ থাকলে সুন্দর করে লিস্ট দেখাবে
            bot.send_message(message.chat.id, f"🚫 **সেশন এখন বন্ধ!**\n\n{get_live_status()}", parse_mode='Markdown')
            return
        
        period_input = message.text
        if period_input.isdigit() and len(period_input) >= 3:
            # ১০% চান্স স্কিপ করার (মার্কেট রিস্ক দেখানোর জন্য)
            if random.random() < 0.10:
                bot.send_message(message.chat.id, f"⚠️ **MARKET RISK!**\nপিরিয়ড {period_input} স্কিপ করুন। মার্কেট এখন রিস্কি।")
                return

            prediction = random.choice(["BIG 🔴", "SMALL 🟢"])
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("WIN ✅", callback_data="win"), types.InlineKeyboardButton("LOSS ❌", callback_data="loss"))
            
            signal_text = (
                f"🔥 **AI SIGNAL** 🔥\n"
                f"━━━━━━━━━━━━\n"
                f"📌 PERIOD: {period_input}\n"
                f"📊 RESULT: {prediction}\n"
                f"━━━━━━━━━━━━\n"
                f"⚠️ অবশ্যই ৫-৬ স্টেপ ফান্ড রাখবেন।"
            )
            bot.send_message(message.chat.id, signal_text, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "🚫 আগে স্ক্রিনশট পাঠিয়ে ভেরিফাই হয়ে নিন।")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "win":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="💰 **SUPER WIN!!** 💰\nউইন রিঅ্যাকশন দিন। 🔥\n\n👉 পরবর্তী পিরিয়ড দিন।")
    elif call.data == "loss":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="⚠️ **LOSS!**\nপরবর্তী লেভেলে ৩ গুণ (3X) ফান্ড ব্যবহার করুন।")

bot.infinity_polling()
        
