import telebot
import random
import time
import datetime

# আপনার দেওয়া আসল টোকেন
API_TOKEN = '8792313235:AAGLv8pmNBm8G2emNK4TW67am45VvFNF5nU' 
# ⚠️ আপনার নিজের টেলিগ্রাম ইউজার আইডি এখানে দিন (যেখানে স্ক্রিনশটগুলো যাবে)
ADMIN_ID = 'YOUR_TELEGRAM_USER_ID' 

bot = telebot.TeleBot(API_TOKEN)

# ১২ ঘণ্টার গোল্ডেন সেশন টাইম
SIGNAL_TIMES = ["11:30 AM", "02:30 PM", "05:30 PM", "09:30 PM", "11:30 PM"]
SESSION_DURATION = 30 

user_status = {} 
loss_count = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 **Welcome to BDWIN24 Official AI Bot!** 🤖\n\n"
        "📊 **আজকের সেশন শিডিউল:**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🕒 ১১:৩০ AM - ১২:০০ PM\n"
        "🕒 ০২:৩০ PM - ০৩:০০ PM\n"
        "🕒 ০৫:৩০ PM - ০৬:০০ PM\n"
        "🕒 ০৯:৩০ PM - ১০:০০ PM 🌟\n"
        "🕒 ১১:৩০ PM - ১২:০০ AM 🌙\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✅ প্রতিটি সেশন **৩০ মিনিট** চলবে।\n"
        "💰 ৫-৬ স্টেপ ফান্ড মেইনটেইন করুন। 🛡️\n\n"
        "📌 **ডিপোজিট করেছেন?** সিগন্যাল অ্যাক্টিভ করতে আপনার ডিপোজিট স্ক্রিনশট এবং ইউ আইডি (UID) এই বটে সেন্ড করুন। 📸"
    )
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Get AI Signal 🚀", "Submit Deposit 💳")
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

# ডিপোজিট সাবমিট করার প্রসেস
@bot.message_handler(func=lambda message: message.text == "Submit Deposit 💳")
def ask_screenshot(message):
    bot.send_message(message.chat.id, "📸 দয়া করে আপনার ডিপোজিটের **স্ক্রিনশট** এবং **ইউ আইডি (UID)** একসাথে সেন্ড করুন।")

# স্ক্রিনশট রিসিভ করা এবং অ্যাডমিনকে পাঠানো
@bot.message_handler(content_types=['photo'])
def handle_deposit_photo(message):
    user_info = f"👤 **New Deposit Submission!**\n\n" \
                f"🆔 **User Name:** @{message.from_user.username}\n" \
                f"🆔 **Telegram ID:** `{message.from_user.id}`\n" \
                f"📝 **Caption/UID:** {message.caption if message.caption else 'No UID provided'}"
    
    # অ্যাডমিনকে পাঠানো
    bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=user_info, parse_mode="Markdown")
    
    # ইউজারকে কনফার্মেশন দেওয়া
    bot.send_message(message.chat.id, "✅ আপনার স্ক্রিনশটটি অ্যাডমিনের কাছে পাঠানো হয়েছে। যাচাই করার পর আপনার সিগন্যাল অ্যাক্টিভ করে দেওয়া হবে। ধন্যবাদ!")

@bot.message_handler(func=lambda message: message.text == "Get AI Signal 🚀")
def handle_signal(message):
    uid = message.chat.id
    now = datetime.datetime.now()
    
    # সেশন এবং লজিক আগের মতোই থাকবে...
    if uid in user_status and user_status[uid] == "CLOSED":
        bot.send_message(uid, "🎊 অভিনন্দন! প্রফিট হয়েছে। পরবর্তী সেশনে আবার আসুন। 🚫")
        return

    in_session = False
    current_session_end = ""
    for s_time in SIGNAL_TIMES:
        start_time = datetime.datetime.strptime(s_time, "%I:%M %p").replace(
            year=now.year, month=now.month, day=now.day
        )
        end_time = start_time + datetime.timedelta(minutes=SESSION_DURATION)
        if start_time <= now <= end_time:
            in_session = True
            current_session_end = end_time.strftime("%I:%M %p")
            break
    
    is_in_loss = uid in user_status and user_status[uid] == "RECOVERY"

    if in_session or is_in_loss:
        processing = bot.send_message(uid, "🔍 **AI মার্কেট বিশ্লেষণ করছে...** 📊")
        time.sleep(1.8)
        bot.delete_message(uid, processing.message_id)

        prediction = random.choice(["BIG 🔴", "SMALL 🟢"])
        period_id = now.strftime("%Y%m%d") + str(random.randint(100, 999))
        
        outcome = random.choice(["WIN", "LOSS"]) 

        if outcome == "LOSS":
            loss_count[uid] = loss_count.get(uid, 0) + 1
            user_status[uid] = "RECOVERY"
            status_note = f"⚠️ **STATUS: LOSS** (স্টেপ: {loss_count[uid]})"
            msg_footer = "পরবর্তী স্টেপে ডাবল ফান্ড দিন।"
        else:
            loss_count[uid] = 0
            user_status[uid] = "CLOSED"
            status_note = "✅ **STATUS: SUPER WIN!!** 🏆"
            msg_footer = "সফলভাবে প্রফিট হয়েছে!"

        signal_msg = (
            f"💥 **BDWIN24 WINGO 1 MINUTE** ✅\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔹 **PERIOD:** `{period_id}`\n"
            f"🔹 **PREDICTION:** **{prediction}**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"⏰ **সেশন ক্লোজ হবে:** {current_session_end if in_session else 'রিকভারি শেষে'}\n\n"
            f"{status_note}\n"
            f"💡 {msg_footer}"
        )
        bot.send_message(uid, signal_msg, parse_mode="Markdown")
    else:
        bot.send_message(uid, "❌ **সেশন বর্তমানে অফলাইন!**")

print("Bot is starting...")
bot.polling(none_stop=True)
    
