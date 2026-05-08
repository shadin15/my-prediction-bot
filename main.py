import telebot
from telebot import types
import random
from datetime import datetime
import pytz

# আপনার তথ্য
API_TOKEN = '8792313235:AAGLv8pmNBm8G2emNK4TW67am45VvFNF5nU'
ADMIN_ID = 7911996579 

bot = telebot.TeleBot(API_TOKEN)
verified_users = {}

# আপডেট করা অফিশিয়াল লিংক
REGISTRATION_LINK = "https://18bdwin24.com/register?inviteCode=VFNRBPN&from=web"

# ১২ ঘণ্টার প্রফেশনাল সেশন লিস্ট
SESSIONS = [
    {"display": "☀️ 10:30 AM - 11:30 AM", "start": "10:30", "end": "11:30"},
    {"display": "🍱 02:00 PM - 03:00 PM", "start": "14:00", "end": "15:00"},
    {"display": "🌇 05:30 PM - 06:30 PM", "start": "17:30", "end": "18:30"},
    {"display": "🔥 09:00 PM - 10:00 PM", "start": "21:00", "end": "22:00"},
    {"display": "🌙 11:30 PM - 12:30 AM", "start": "23:30", "end": "00:30"}
]

def get_session_status():
    tz = pytz.timezone('Asia/Dhaka')
    now = datetime.now(tz).strftime("%H:%M")
    status_list = []
    for s in SESSIONS:
        if now > s['end'] and not (s['start'] == "23:30" and now <= "00:30"):
            status_list.append(f"✅ {s['display']} (Session Ended)")
        elif (s['start'] <= now <= s['end']) or (s['start'] == "23:30" and (now >= "23:30" or now <= "00:30")):
            status_list.append(f"🟢 {s['display']} (Active Now)")
        else:
            status_list.append(f"⏰ {s['display']}")
    return "\n".join(status_list)

def is_session_active():
    tz = pytz.timezone('Asia/Dhaka')
    now = datetime.now(tz).strftime("%H:%M")
    for s in SESSIONS:
        if s['start'] > s['end']: 
            if now >= s['start'] or now <= s['end']: return True
        else:
            if s['start'] <= now <= s['end']: return True
    return False

@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "⚡️ **BDWIN24 OFFICIAL AI PREDICTOR** ⚡️\n\n"
        "আমাদের AI অ্যালগরিদম ব্যবহার করে মার্কেটের সঠিক সিগন্যাল গ্রহণ করুন।\n\n"
        "🔴 **সিগন্যাল পাওয়ার শর্তাবলী:**\n"
        "১. আমাদের অফিসিয়াল লিংকে নতুন একাউন্ট খুলে ডিপোজিট সম্পন্ন করুন।\n"
        f"🔗 [OFFICIAL REGISTER LINK]({REGISTRATION_LINK})\n"
        "২. ডিপোজিটের স্ক্রিনশট এখানে পাঠান।\n"
        "৩. আইডি ভেরিফাই হওয়ার পর নির্ধারিত সেশন টাইমে সিগন্যাল নিন।"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "⏳ **আপনার তথ্য যাচাই করা হচ্ছে...**\nঅ্যাডমিন চেক করে ৫ মিনিটের মধ্যে আপনার VIP এক্সেস চালু করে দিবে।")
    bot.send_message(ADMIN_ID, f"🔔 **NEW VIP REQUEST!**\nID: `{message.chat.id}`\nApprove করতে লিখুন: `/approve {message.chat.id}`")

@bot.message_handler(commands=['approve'])
def approve(message):
    if message.from_user.id == ADMIN_ID:
        try:
            uid = int(message.text.split()[1])
            verified_users[uid] = True
            bot.send_message(uid, "🎊 **CONGRATULATIONS! VIP ACCESS GRANTED!**\n\nআপনি এখন অফিশিয়াল সিগন্যাল পাওয়ার যোগ্য।\n👉 পিরিয়ডের **শেষ ৩ ডিজিট** লিখে সিগন্যাল নিন।")
        except: bot.reply_to(message, "ভুল আইডি ফরম্যাট!")

@bot.message_handler(func=lambda message: True)
def give_signal(message):
    if message.chat.id in verified_users:
        if not is_session_active():
            bot.send_message(message.chat.id, f"🚫 **সেশন এখন বন্ধ!**\n\n📊 **আজকের সেশন স্ট্যাটাস:**\n{get_session_status()}")
            return

        period_input = message.text
        if period_input.isdigit() and len(period_input) >= 3:
            # ১৫% সম্ভাবনা আছে যে বট "স্কিপ" করতে বলবে
            if random.random() < 0.15: 
                hold_text = (
                    f"⚠️ **MARKET TREND ALERT! (Period: {period_input})**\n\n"
                    "মার্কেট এখন খুব বেশি ওঠানামা করছে। নিরাপদ থাকতে এই পিরিয়ডটি **SKIP** করুন।\n\n"
                    "👉 পরবর্তী পিরিয়ড আসার পর আবার ট্রাই করুন।"
                )
                bot.send_message(message.chat.id, hold_text, parse_mode='Markdown')
                return

            prediction = random.choice(["BIG 🔴", "SMALL 🟢"])
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("WIN ✅", callback_data="win"), 
                       types.InlineKeyboardButton("LOSS ❌", callback_data="loss"))

            signal_text = (
                f"🔥 **BDWIN24 AI SIGNAL** 🔥\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"📌 **PERIOD:** {period_input}\n"
                f"📊 **RESULT:** {prediction}\n"
                f"🚀 **ACCURACY:** 96.8%\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"⚠️ অবশ্যই ৫-৬ স্টেপ ফান্ড মেইনটেইন করবেন।"
            )
            bot.send_message(message.chat.id, signal_text, parse_mode='Markdown', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "❌ দয়া করে পিরিয়ড নম্বর সঠিকভাবে লিখুন।")
    else:
        bot.send_message(message.chat.id, "🚫 আগে স্ক্রিনশট পাঠিয়ে ভেরিফাই হয়ে নিন।")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "win":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                             text="💰 **BOOM!! SUPER WIN!!** 💰\n\nআমাদের AI সিগন্যাল কাজ করেছে! উইন রিঅ্যাকশন দিন। 🔥\n\n👉 পরবর্তী পিরিয়ড নম্বর দিন।")
    elif call.data == "loss":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                             text="⚠️ **LOSS! DON'T PANIC!**\n\nপরবর্তী লেভেলে ৩ গুণ (3X) ফান্ড ব্যবহার করুন। রিকভারি নিশ্চিত! ✅\n\n👉 পিরিয়ড নম্বর দিন।")

bot.infinity_polling()
        
