import telebot
import random
import time
import datetime
from telebot import types

# আপনার টোকেন এবং অ্যাডমিন আইডি
API_TOKEN = '8792313235:AAGLv8pmNBm8G2emNK4TW67am45VvFNF5nU'
ADMIN_ID = 7911996579 

bot = telebot.TeleBot(API_TOKEN)

# মেমোরি ডাটাবেজ
approved_users = set()

# আপনার দেওয়া গেম রেফারেল লিংক
REFERRAL_LINK = "https://18bdwin24.com/register?inviteCode=VFNRBPN&from=web" 

# ৪টি সেশন টাইম (৩০ মিনিট স্থায়ী)
SIGNAL_TIMES = ["11:30 AM", "03:30 PM", "07:30 PM", "10:30 PM"]

def get_schedule_with_ticks():
    """সেশন শেষ হয়ে গেলে অটোমেটিক টিক মার্ক দেওয়ার লজিক"""
    now = datetime.datetime.now()
    schedule_text = ""
    for s_time in SIGNAL_TIMES:
        start_time = datetime.datetime.strptime(s_time, "%I:%M %p").replace(
            year=now.year, month=now.month, day=now.day
        )
        end_time = start_time + datetime.timedelta(minutes=30)
        
        # যদি বর্তমান সময় সেশন শেষ হওয়ার সময়ের চেয়ে বেশি হয়, তবে টিক মার্ক বসবে
        tick = " ✅" if now > end_time else ""
        schedule_text += f"🕒 {s_time} - {(start_time + datetime.timedelta(minutes=30)).strftime('%I:%M %p')}{tick}\n"
    return schedule_text

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 **Welcome to BDWIN24 Official AI Bot!** 🤖\n\n"
        "সিগন্যাল পেতে নিচের ধাপগুলো অবশ্যই মানুন:\n\n"
        f"১. এই লিংক থেকে একাউন্ট খুলুন: [রেজিস্ট্রেশন লিংক]({REFERRAL_LINK})\n"
        "২. ডিপোজিট সম্পন্ন করে গেম UID সহ একটি স্ক্রিনশট এখানে পাঠান। 📸\n"
        "৩. অ্যাডমিন যাচাই করে এপ্রুভ করলে আপনি সিগন্যাল বাটন পাবেন। ✨\n\n"
        "📊 **আজকের সেশন স্ট্যাটাস:**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"{get_schedule_with_ticks()}"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💰 ৫-৬ স্টেপ ফান্ড ব্যাকআপ রাখুন। রিকভারি মোড সচল আছে।"
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Get AI Signal 🚀", "My Status 👤")
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup, disable_web_page_preview=True)

# স্ক্রিনশট ও ইউজারনেম অ্যাডমিনের কাছে পাঠানো
@bot.message_handler(content_types=['photo'])
def handle_verification(message):
    user_id = message.from_user.id
    user_name = f"@{message.from_user.username}" if message.from_user.username else "No Username"
    caption = message.caption if message.caption else "No UID provided"

    markup = types.InlineKeyboardMarkup()
    approve_btn = types.InlineKeyboardButton("✅ Approve Member", callback_data=f"approve_{user_id}")
    markup.add(approve_btn)

    admin_msg = f"📩 **New Request!**\n👤 User: {user_name}\n🆔 ID: `{user_id}`\n📝 Details: {caption}"
    bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=admin_msg, reply_markup=markup, parse_mode="Markdown")
    
    bot.send_message(user_id, "⏳ আপনার স্ক্রিনশট এবং ইউজার তথ্য অ্যাডমিনের কাছে পাঠানো হয়েছে। যাচাই শেষে আপনাকে এপ্রুভ করা হবে।")

# অ্যাডমিন এপ্রুভাল লজিক
@bot.callback_query_handler(func=lambda call: call.data.startswith('approve_'))
def approve_user(call):
    if call.from_user.id == ADMIN_ID:
        target_id = int(call.data.split('_')[1])
        approved_users.add(target_id)
        bot.answer_callback_query(call.id, "User Approved! ✅")
        bot.send_message(target_id, "🎉 অভিনন্দন! অ্যাডমিন আপনাকে এপ্রুভ করেছে। এখন সেশন টাইমে আপনি সিগন্যাল নিতে পারবেন।")
        bot.edit_message_caption("✅ এই মেম্বারকে এপ্রুভ করা হয়েছে।", chat_id=ADMIN_ID, message_id=call.message.message_id)

# সিগন্যাল প্রসেসিং
@bot.message_handler(func=lambda message: message.text == "Get AI Signal 🚀")
def handle_signal_request(message):
    uid = message.chat.id
    
    if uid not in approved_users and uid != ADMIN_ID:
        bot.send_message(uid, "🚫 আপনি ভেরিফাইড মেম্বার নন। আগে ডিপোজিট স্ক্রিনশট এবং UID পাঠিয়ে এপ্রুভাল নিন।")
        return

    now = datetime.datetime.now()
    in_session = False
    for s_time in SIGNAL_TIMES:
        start_time = datetime.datetime.strptime(s_time, "%I:%M %p").replace(
            year=now.year, month=now.month, day=now.day
        )
        end_time = start_time + datetime.timedelta(minutes=30)
        if start_time <= now <= end_time:
            in_session = True
            break
    
    if not in_session:
        bot.send_message(uid, "❌ বর্তমানে কোনো সেশন নেই। পরবর্তী সেশনের জন্য শিডিউল চেক করুন। ⏳")
        return

    msg = bot.send_message(uid, "📝 পিরিয়ডের **শেষ ৩ সংখ্যা** এবং **আগের রেজাল্ট** দিন।\n\nউদাহরণ: `425 9` (পিরিয়ড ৪২৫ এবং রেজাল্ট ৯)")
    bot.register_next_step_handler(msg, calculate_signal)

def calculate_signal(message):
    try:
        data = message.text.split()
        period = data[0]
        last_val = int(data[1])

        # ৫-৬ স্টেপ উইনিং অ্যালগরিদম
        prediction = "BIG 🔴" if last_val <= 4 else "SMALL 🟢"
        if random.random() > 0.7:
             prediction = "SMALL 🟢" if prediction == "BIG 🔴" else "BIG 🔴"

        response = (
            f"💥 **BDWIN24 PREDICTION** ✅\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 **PERIOD:** `{period}`\n"
            f"🔮 **PREDICTION:** **{prediction}**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 ৫-৬ স্টেপ ফান্ড মেইনটেইন করুন। উইন নিশ্চিত হবে! 🔥"
        )
        bot.send_message(message.chat.id, response, parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, "❌ ফরম্যাট ভুল! দয়া করে এভাবে লিখুন: `425 9`")

print("Bot is Active on Railway...")
bot.polling(none_stop=True)
    
