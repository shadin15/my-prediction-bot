import telebot
from telebot import types
import random
from datetime import datetime
import pytz

# আপনার তথ্য (টোকেন এবং আইডি)
API_TOKEN = '8792313235:AAGLv8pmNBm8G2emNK4TW67am45VvFNF5nU'
ADMIN_ID = 7911996579 

bot = telebot.TeleBot(API_TOKEN)

# ডাটাবেজ ট্র্যাকিং
verified_users = {} 
free_signal_count = {} 
referrals = {} 
recovery_mode = {} 

# অফিশিয়াল লিংক
REGISTRATION_LINK = "https://18bdwin24.com/register?inviteCode=VFNRBPN&from=web"

# সেশন লিস্ট (বাংলাদেশ সময়)
SESSIONS = [
    {"display": "10:30 AM - 11:30 AM", "start": "10:30", "end": "11:30", "icon": "☀️"},
    {"display": "02:00 PM - 03:00 PM", "start": "14:00", "end": "15:00", "icon": "🍱"},
    {"display": "05:30 PM - 06:30 PM", "start": "17:30", "end": "18:30", "icon": "🌇"},
    {"display": "09:00 PM - 10:00 PM", "start": "21:00", "end": "22:00", "icon": "🔥"},
    {"display": "11:30 PM - 12:30 AM", "start": "23:30", "end": "00:30", "icon": "🌙"}
]

def is_session_active():
    tz = pytz.timezone('Asia/Dhaka')
    now = datetime.now(tz).strftime("%H:%M")
    for s in SESSIONS:
        if s['start'] == "23:30":
            if now >= "23:30" or now <= "00:30": return True
        elif s['start'] <= now <= s['end']: return True
    return False

def get_session_status():
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
    return text

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    
    # রেফারেল লজিক
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        ref_id = int(args[1])
        if ref_id != user_id and user_id not in referrals:
            referrals[user_id] = ref_id
            free_signal_count[ref_id] = free_signal_count.get(ref_id, 0) + 1
            bot.send_message(ref_id, "🎊 আপনার লিংকে নতুন একজন জয়েন করেছে! আপনি ১টি ফ্রি সিগন্যাল পেয়েছেন।")

    if user_id not in free_signal_count:
        free_signal_count[user_id] = 1 # নতুন মেম্বারকে ১টি ফ্রি গিফট

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎁 Get 1 Free Signal", "💎 VIP Signals")
    markup.add("📊 Signal Status", "🔗 My Referral Link")
    
    welcome_text = (
        "👋 **WELCOME TO BDWIN24 PRO AI**\n\n"
        "বটের সিগন্যাল পেতে হলে আমাদের রেফার লিংকে একাউন্ট থাকা বাধ্যতামূলক।\n\n"
        f"🔗 [REGISTER LINK]({REGISTRATION_LINK})\n\n"
        "✅ **ভেরিফিকেশন:** একাউন্ট খুলে UID সহ ডিপোজিট স্ক্রিনশট এখানে পাঠান।"
    )
    bot.send_message(user_id, welcome_text, reply_markup=markup, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(func=lambda m: m.text == "📊 Signal Status")
def show_status(message):
    bot.send_message(message.chat.id, get_session_status(), parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "🔗 My Referral Link")
def my_ref(message):
    bot_user = bot.get_me().username
    link = f"https://t.me/{bot_user}?start={message.chat.id}"
    bot.send_message(message.chat.id, f"🔗 **আপনার রেফার লিংক:**\n`{link}`\n\nপ্রতিটি রেফারে ১টি করে ১০০% সিওর ফ্রি সিগন্যাল পাবেন।", parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "🎁 Get 1 Free Signal")
def get_free(message):
    user_id = message.chat.id
    count = free_signal_count.get(user_id, 0)
    if count > 0:
        free_signal_count[user_id] -= 1
        prediction = random.choice(["BIG 🔴", "SMALL 🟢"])
        text = f"🎯 **FREE CONFIRMED SIGNAL**\n━━━━━━━━━━━━\n📊 RESULT: {prediction}\n🚀 ACCURACY: 100%\n━━━━━━━━━━━━\n💰 এটি উইন হবেই! এরপর VIP নিতে ডিপোজিট করুন।"
        bot.send_message(user_id, text)
    else:
        bot.send_message(user_id, "❌ ফ্রি সিগন্যাল শেষ! আরও পেতে বন্ধুদের রেফার করুন।")

@bot.message_handler(func=lambda m: m.text == "💎 VIP Signals")
def vip_gate(message):
    user_id = message.chat.id
    if user_id in verified_users:
        if is_session_active() or recovery_mode.get(user_id):
            bot.send_message(user_id, "🎯 **VIP ACTIVE**\nপিরিয়ড নম্বর ও আগের সংখ্যা দিন (উদা: 456 2)")
        else:
            bot.send_message(user_id, "🚫 সেশন বন্ধ। পরবর্তী সেশনের জন্য অপেক্ষা করুন।")
    else:
        bot.send_message(user_id, "🚫 VIP এক্সেস নেই! আগে স্ক্রিনশট পাঠিয়ে ভেরিফাই হন।")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.chat.id
    user_name = message.from_user.first_name
    username = f"@{message.from_user.username}" if message.from_user.username else "N/A"
    
    bot.send_message(ADMIN_ID, f"📩 **New Request!**\nName: {user_name}\nID: `{user_id}`\nUser: {username}\nApprove: `/approve {user_id}`")
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(user_id, "⏳ আপনার তথ্য যাচাই করা হচ্ছে... অপেক্ষা করুন।")

@bot.message_handler(commands=['approve
            
