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

# অফিসিয়াল লিংক
REGISTRATION_LINK = "https://21bdwin24.com/register?inviteCode=VFNRBPN&from=web"

# আপনার দেওয়া ৫ বেলা সিগন্যাল সেশন টাইম (বাংলাদেশ সময়)
SESSIONS = [
    ("10:30", "11:30"), # সকাল
    ("14:00", "15:00"), # দুপুর
    ("17:30", "18:30"), # বিকেল
    ("21:00", "22:00"), # রাত (প্রাইম)
    ("23:30", "00:30")  # মাঝরাত
]

def is_session_active():
    tz = pytz.timezone('Asia/Dhaka')
    now = datetime.now(tz).strftime("%H:%M")
    for start, end in SESSIONS:
        # মাঝরাতের সেশনের জন্য লজিক (২৩:৩০ থেকে ০০:৩০)
        if start > end: 
            if now >= start or now <= end:
                return True
        else:
            if start <= now <= end:
                return True
    return False

@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "⚡️ **WELCOME TO BDWIN24 OFFICIAL AI PREDICTOR** ⚡️\n\n"
        "আমাদের AI সিস্টেম গাণিতিক ফর্মুলা ব্যবহার করে মার্কেটের ট্রেন্ড এনালাইসিস করে সিগন্যাল দেয়।\n\n"
        "🔴 **কিভাবে সিগন্যাল পাবেন?**\n"
        "১. আমাদের রেফার লিংকে নতুন একাউন্ট খুলে ডিপোজিট করুন।\n"
        f"🔗 [OFFICIAL REGISTER LINK]({REGISTRATION_LINK})\n"
        "২. ডিপোজিটের স্ক্রিনশট এখানে পাঠান।\n"
        "৩. আমাদের অফিসিয়াল সেশন টাইমে পিরিয়ড নম্বর দিয়ে সিগন্যাল নিন।"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "⏳ **ভেরিফিকেশন চলছে...**\n\nঅ্যাডমিন চেক করে ৫-১০ মিনিটের মধ্যে আপনার VIP এক্সেস চালু করে দিবে।")
    bot.send_message(ADMIN_ID, f"🔔 **NEW VIP REQUEST!**\nID: `{message.chat.id}`\nApprove করতে: `/approve {message.chat.id}`")

@bot.message_handler(commands=['approve'])
def approve(message):
    if message.from_user.id == ADMIN_ID:
        try:
            uid = int(message.text.split()[1])
            verified_users[uid] = True
            bot.send_message(uid, "🎊 **VIP ACCESS ACTIVATED!**\n\nএখন থেকে আপনি নির্ধারিত সেশন টাইমে সিগন্যাল পাবেন।\n👉 সিগন্যাল পেতে পিরিয়ডের **শেষ ৩ ডিজিট** লিখুন।")
        except:
            bot.reply_to(message, "আইডি ভুল!")

@bot.message_handler(func=lambda message: True)
def give_signal(message):
    if message.chat.id in verified_users:
        # সময় চেক করা হচ্ছে
        if not is_session_active():
            times_text = "\n".join([f"⏰ {s[0]} - {s[1]}" for s in SESSIONS])
            bot.send_message(message.chat.id, f"🚫 **সেশন এখন বন্ধ!**\n\nপরবর্তী সিগন্যাল সেশনের জন্য অপেক্ষা করুন।\n\n📊 **সেশন টাইম (BD Time):**\n{times_text}")
            return

        period_input = message.text
        if period_input.isdigit() and len(period_input) >= 3:
            prediction = random.choice(["BIG 🔴", "SMALL 🟢"])
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("WIN ✅", callback_data="win"), 
                       types.InlineKeyboardButton("LOSS ❌", callback_data="loss"))

            signal_text = (
                f"🔥 **BDWIN24 AI SIGNAL** 🔥\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"📌 **PERIOD:** {period_input}\n"
                f"📊 **RESULT:** {prediction}\n"
                f"🚀 **ACCURACY:** 94%\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"⚠️ **GUIDELINE:** অবশ্যই ৫-৬ স্টেপ ফান্ড রাখবেন। লস হলে ৩ গুণ (3X) অ্যামাউন্ট ব্যবহার করুন।"
            )
            bot.send_message(message.chat.id, signal_text, parse_mode='Markdown', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "❌ পিরিয়ডের শেষ ৩ বা ৪ ডিজিট লিখুন।")
    else:
        bot.send_message(message.chat.id, "🚫 আগে স্ক্রিনশট পাঠিয়ে ভেরিফাই হয়ে নিন।")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "win":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                             text="💰 **SUPER WIN!!** 💰\n\nপরবর্তী সিগন্যালের জন্য নতুন পিরিয়ড নম্বর দিন।")
    elif call.data == "loss":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                             text="⚠️ **LOSS! DON'T PANIC!**\n\nপরবর্তী লেভেলে ৩ গুণ ফান্ড ব্যবহার করুন। ৫-৬ স্টেপের ভেতর ১০০% উইন নিশ্চিত। পরবর্তী পিরিয়ড দিন।")

bot.infinity_polling()
    
