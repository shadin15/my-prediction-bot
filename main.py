import telebot
import random
import time
import datetime
from telebot import types

# আপনার টোকেন এবং অ্যাডমিন আইডি
API_TOKEN = '8792313235:AAGLv8pmNBm8G2emNK4TW67am45VvFNF5nU'
ADMIN_ID = 7911996579 

bot = telebot.TeleBot(API_TOKEN)

approved_users = set()
user_data = {} 
# সেশন ভিত্তিক উইন ট্র্যাকিং (১০টি উইন টার্গেট)
session_stats = {"wins": 0, "last_session_time": ""}

REFERRAL_LINK = "https://18bdwin24.com/register?inviteCode=VFNRBPN&from=web"
SIGNAL_TIMES = ["11:30 AM", "03:30 PM", "07:30 PM", "10:30 PM"]

def get_next_session_info():
    now = datetime.datetime.now()
    for s_time in SIGNAL_TIMES:
        start_time = datetime.datetime.strptime(s_time, "%I:%M %p").replace(
            year=now.year, month=now.month, day=now.day
        )
        if now < start_time:
            return s_time
    return SIGNAL_TIMES[0]

def check_session_status():
    now = datetime.datetime.now()
    current_s_time = ""
    
    # বর্তমান কোন সেশনের সময় চলছে তা বের করা
    for s_time in SIGNAL_TIMES:
        start_time = datetime.datetime.strptime(s_time, "%I:%M %p").replace(
            year=now.year, month=now.month, day=now.day
        )
        # সেশন শুরুর সময় থেকে পরবর্তী সেশন পর্যন্ত উইন্ডো খোলা থাকে কিন্তু উইন লিমিট থাকলে বন্ধ হবে
        if now >= start_time:
            current_s_time = s_time

    # নতুন সেশন শুরু হলে উইন কাউন্ট রিসেট করার লজিক
    if session_stats["last_session_time"] != current_s_time:
        session_stats["wins"] = 0
        session_stats["last_session_time"] = current_s_time

    # যদি ১০টি উইন হয়ে যায়
    if session_stats["wins"] >= 10:
        return False, "LIMIT_REACHED"
    
    if current_s_time == "":
        return False, "NO_SESSION"
    
    return True, "ACTIVE"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 **Welcome to BDWIN24 Official AI Bot!** 🤖\n\n"
        f"🔗 [একাউন্ট খুলতে এখানে ক্লিক করুন]({REFERRAL_LINK})\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✅ সিগন্যাল পেতে আপনার ডিপোজিট স্ক্রিনশট এবং UID পাঠান।\n"
        "✅ অ্যাডমিন এপ্রুভ করলে আপনি সিগন্যাল নিতে পারবেন।"
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Get AI Signal 🚀", "My Status 👤")
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup, disable_web_page_preview=True)

@bot.message_handler(content_types=['photo'])
def handle_verification(message):
    user_id = message.from_user.id
    user_name = f"@{message.from_user.username}" if message.from_user.username else "No Username"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Approve Member", callback_data=f"approve_{user_id}"))
    bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f"📩 Request from {user_name}\nID: `{user_id}`\nUID: {message.caption}", reply_markup=markup)
    bot.send_message(user_id, "⏳ আপনার তথ্য পাঠানো হয়েছে। এপ্রুভ হওয়া পর্যন্ত অপেক্ষা করুন।")

@bot.callback_query_handler(func=lambda call: call.data.startswith('approve_'))
def approve_user(call):
    target_id = int(call.data.split('_')[1])
    approved_users.add(target_id)
    bot.send_message(target_id, "🎉 অভিনন্দন! আপনি এপ্রুভ হয়েছেন। এখন সেশন অনুযায়ী সিগন্যাল নিতে পারবেন।")
    bot.edit_message_caption("✅ Approved!", chat_id=ADMIN_ID, message_id=call.message.message_id)

@bot.message_handler(func=lambda message: message.text == "Get AI Signal 🚀")
def handle_signal_request(message):
    uid = message.chat.id
    if uid not in approved_users and uid != ADMIN_ID:
        bot.send_message(uid, "🚫 আপনি এপ্রুভড নন। আগে ভেরিফাই করুন।")
        return

    # আগের রেজাল্ট না দিলে লক
    if uid in user_data and user_data[uid].get('waiting_result'):
        bot.send_message(uid, "⚠️ **সতর্কতা!** আগের সিগন্যালের রেজাল্ট জানাননি।\nদয়া করে WIN অথবা LOSS বাটনে ক্লিক করুন।")
        return

    is_active, status = check_session_status()
    
    if status == "LIMIT_REACHED":
        next_s = get_next_session_info()
        bot.send_message(uid, f"✅ **সেশন ক্লোজ!**\nএই সেশনের জন্য ১০টি উইন টার্গেট পূর্ণ হয়েছে।\n\n🔔 পরবর্তী সেশন শুরু হবে: **{next_s}**")
        return

    if status == "NO_SESSION" and user_data.get(uid, {}).get('step', 1) == 1:
        next_s = get_next_session_info()
        bot.send_message(uid, f"❌ বর্তমানে সেশন বন্ধ।\n🔔 পরবর্তী সেশন শুরু হবে: **{next_s}**")
        return

    msg = bot.send_message(uid, "📝 পিরিয়ড এবং রেজাল্ট দিন (যেমন: `425/9`)")
    bot.register_next_step_handler(msg, calculate_recovery_signal)

def calculate_recovery_signal(message):
    uid = message.chat.id
    try:
        data = message.text.split('/')
        period = data[0].strip()
        last_val = int(data[1].strip())

        if uid not in user_data:
            user_data[uid] = {'step': 1, 'waiting_result': False}
        
        step = user_data[uid]['step']

        # ৬-স্টেপ গ্যারান্টি লজিক (৫ ও ৬ নম্বর স্টেপে হাই একুরেসি)
        if step >= 5:
            bot.send_message(uid, "🔍 AI মার্কেট এনালাইসিস করছে...")
            time.sleep(2)
            prediction = "BIG 🔴" if last_val <= 3 else "SMALL 🟢"
        else:
            prediction = "SMALL 🟢" if last_val >= 5 else "BIG 🔴"

        user_data[uid]['waiting_result'] = True

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ WIN", callback_data="res_win"),
            types.InlineKeyboardButton("❌ LOSS", callback_data="res_loss")
        )

        amount = 10 * (2**(step-1))
        response = (
            f"🎯 **STEP {step} SIGNAL** ✅\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔹 **PERIOD:** `{period}`\n"
            f"🔮 **PREDICTION:** **{prediction}**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 **ফান্ড:** {amount} টাকা\n"
            f"📈 **উইন টার্গেট:** {session_stats['wins']}/10\n\n"
            f"⚠️ রেজাল্ট না দিলে পরের সিগন্যাল আসবে না।"
        )
        bot.send_message(uid, response, parse_mode="Markdown", reply_markup=markup)
    except:
        bot.send_message(uid, "❌ ভুল ফরম্যাট! পিরিয়ড এবং রেজাল্ট দিন: `425/9`")

@bot.callback_query_handler(func=lambda call: call.data.startswith('res_'))
def handle_result(call):
    uid = call.message.chat.id
    if uid not in user_data: return
    
    if call.data == "res_win":
        user_data[uid]['step'] = 1 
        user_data[uid]['waiting_result'] = False 
        session_stats["wins"] += 1 # উইন কাউন্ট হচ্ছে
        bot.edit_message_text(f"🎉 **WIN!!** (টার্গেট: {session_stats['wins']}/10)\nপরের সিগন্যালের জন্য আবার ক্লিক করুন।", uid, call.message.message_id)
    
    elif call.data == "res_loss":
        if user_data[uid]['step'] < 6:
            user_data[uid]['step'] += 1 
            user_data[uid]['waiting_result'] = False 
            bot.edit_message_text(f"⚠️ লস হয়েছে! স্টেপ {user_data[uid]['step']} রিকভারি সিগন্যাল নিতে আবার ইনপুট দিন।", uid, call.message.message_id)
        else:
            user_data[uid]['step'] = 1
            user_data[uid]['waiting_result'] = False
            bot.edit_message_text("🚫 সেশন রিকভারি ব্যর্থ। মার্কেট অতিরিক্ত খারাপ।", uid, call.message.message_id)

bot.polling(none_stop=True)
        
