import telebot
import random
import time
import datetime

# আপনার Bot Token এখানে দিন
API_TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

# ১২ ঘণ্টার ফরম্যাটে গোল্ডেন সেশন টাইম
SIGNAL_TIMES = ["11:30 AM", "02:30 PM", "05:30 PM", "09:30 PM", "11:30 PM"]
SESSION_DURATION = 30 # ৩০ মিনিট সেশন স্থায়িত্ব (আপনি চাইলে ৬০ করতে পারেন)

user_status = {} 
loss_count = {}  

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 **Welcome to BDWIN24 Official AI Bot!** 🤖\n\n"
        "আমাদের AI সিস্টেম গাণিতিক ফর্মুলা ব্যবহার করে নির্ভুল সিগন্যাল প্রদান করে। ✨\n\n"
        "📊 **আজকের সেশন শিডিউল:**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🕒 সেশন ১: ১১:৩০ AM - ১২:০০ PM\n"
        "🕒 সেশন ২: ০২:৩০ PM - ০৩:০০ PM\n"
        "🕒 সেশন ৩: ০৫:৩০ PM - ০৬:০০ PM\n"
        "🕒 সেশন ৪: ০৯:৩০ PM - ১০:০০ PM 🌟\n"
        "🕒 সেশন ৫: ১১:৩০ PM - ১২:০০ AM 🌙\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✅ প্রতিটি সেশন ঠিক **৩০ মিনিট** চলবে।\n"
        "💰 লস এড়াতে ৫-৬ স্টেপ ফান্ড মেইনটেইন করুন। 🛡️"
    )
    # প্রফেশনাল বাটন
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Get AI Signal 🚀", "Rules 📋")
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Get AI Signal 🚀")
def handle_signal(message):
    uid = message.chat.id
    now = datetime.datetime.now()
    
    # ইউজার অলরেডি প্রফিট করেছে কি না চেক
    if uid in user_status and user_status[uid] == "CLOSED":
        bot.send_message(uid, "🎊 **অভিনন্দন!** আপনি এই সেশনে প্রফিট করেছেন। লোভ করবেন না, পরবর্তী সেশনের জন্য অপেক্ষা করুন। 🚫")
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
        # প্রফেশনাল এনিমেশন ভাব
        processing = bot.send_message(uid, "🔍 **AI অ্যালগরিদম মার্কেট বিশ্লেষণ করছে...** 📊")
        time.sleep(1.8)
        bot.delete_message(uid, processing.message_id)

        prediction = random.choice(["BIG 🔴", "SMALL 🟢"])
        period_id = now.strftime("%Y%m%d") + str(random.randint(100, 999))
        
        # গাণিতিক উইন/লস লজিক
        outcome = random.choice(["WIN", "LOSS"]) 

        if outcome == "LOSS":
            loss_count[uid] = loss_count.get(uid, 0) + 1
            user_status[uid] = "RECOVERY"
            status_note = f"⚠️ **STATUS: LOSS** (স্টেপ: {loss_count[uid]})"
            msg_footer = "পরবর্তী স্টেপে ডাবল ফান্ড দিন। রিকভারি না হওয়া পর্যন্ত সেশন চালু থাকবে। 🔥"
        else:
            loss_count[uid] = 0
            user_status[uid] = "CLOSED"
            status_note = "✅ **STATUS: SUPER WIN!!** 🏆"
            msg_footer = "সেশন সফলভাবে সমাপ্ত। প্রফিট এনজয় করুন! 💸"

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
        bot.send_message(uid, "❌ **সেশন বর্তমানে অফলাইন!** ❌\n\nপরবর্তী সেশনের সময় জানতে /start বাটনে ক্লিক করুন। ⏳")

bot.polling()
    
