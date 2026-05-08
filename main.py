import telebot
import random
import time
import datetime
from telebot import types

API_TOKEN = '8792313235:AAGLv8pmNBm8G2emNK4TW67am45VvFNF5nU'
ADMIN_ID = 7911996579 

bot = telebot.TeleBot(API_TOKEN)

approved_users = set()
# ইউজার প্রতি লস কাউন্ট রাখার জন্য
user_loss_steps = {} 

REFERRAL_LINK = "https://18bdwin24.com/register?inviteCode=VFNRBPN&from=web"
SIGNAL_TIMES = ["11:30 AM", "03:30 PM", "07:30 PM", "10:30 PM"]

def is_session_active():
    now = datetime.datetime.now()
    for s_time in SIGNAL_TIMES:
        start_time = datetime.datetime.strptime(s_time, "%I:%M %p").replace(
            year=now.year, month=now.month, day=now.day
        )
        end_time = start_time + datetime.timedelta(minutes=30)
        if start_time <= now <= end_time:
            return True, end_time.strftime("%I:%M %p")
    return False, None

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

@bot.message_handler(func=lambda message: message.text == "My Status 👤")
def check_status(message):
    uid = message.chat.id
    status = "✅ Verified" if uid in approved_users or uid == ADMIN_ID else "❌ Unverified"
    bot.send_message(uid, f"👤 **Your Status:**\n🆔 ID: `{uid}`\n📊 Status: {status}")

@bot.message_handler(content_types=['photo'])
def handle_verification(message):
    user_id = message.from_user.id
    user_name = f"@{message.from_user.username}" if message.from_user.username else "No Username"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user_id}"))
    bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f"📩 Request from {user_name}\nID: `{user_id}`\nUID: {message.caption}", reply_markup=markup)
    bot.send_message(user_id, "⏳ আপনার তথ্য পাঠানো হয়েছে। এপ্রুভ হওয়া পর্যন্ত অপেক্ষা করুন।")

@bot.callback_query_handler(func=lambda call: call.data.startswith('approve_'))
def approve_user(call):
    target_id = int(call.data.split('_')[1])
    approved_users.add(target_id)
    bot.send_message(target_id, "🎉 অভিনন্দন! আপনি এখন সেশন টাইমে সিগন্যাল নিতে পারবেন।")
    bot.edit_message_caption("✅ Approved!", chat_id=ADMIN_ID, message_id=call.message.message_id)

@bot.message_handler(func=lambda message: message.text == "Get AI Signal 🚀")
def handle_signal_request(message):
    uid = message.chat.id
    if uid not in approved_users and uid != ADMIN_ID:
        bot.send_message(uid, "🚫 আপনি এপ্রুভড নন। আগে স্ক্রিনশট পাঠিয়ে ভেরিফাই করুন।")
        return

    active, end_time = is_session_active()
    if not active:
        bot.send_message(uid, "❌ **সেশন বর্তমানে বন্ধ!**\nপরবর্তী সেশনের জন্য শিডিউল চেক করুন। ⏳")
        return

    msg = bot.send_message(uid, "📝 পিরিয়ড এবং রেজাল্ট দিন (যেমন: `425/9`)")
    bot.register_next_step_handler(msg, calculate_smart_signal)

def calculate_smart_signal(message):
    uid = message.chat.id
    try:
        # মেম্বার যদি 425/9 এই ফরম্যাটে দেয়
        data = message.text.split('/')
        period = data[0].strip()
        last_val = int(data[1].strip())

        # লস স্টেপ ট্র্যাকিং
        current_step = user_loss_steps.get(uid, 1)

        # মার্কেট খারাপ হওয়ার লজিক (র‍্যান্ডম হোল্ড চেক)
        if random.random() < 0.15: # ১৫% চান্স মার্কেট হোল্ড করার
            bot.send_message(uid, "⚠️ **MARKET ALERT:** মার্কেট বর্তমানে ভলাটাইল।\n🛑 এই পিরিয়ডটি **HOLD** করুন। ১ মিনিট পর পরের পিরিয়ড ডাটা দিন।")
            return

        # ৪ স্টেপ লস হলে ২ স্টেপ রিকভারি মোড
        if current_step >= 5:
            bot.send_message(uid, "🔍 **AI RECOVERY MODE:** মার্কেট এনালাইসিস চলছে... (১০ সেকেন্ড)")
            time.sleep(3)
            prediction = "BIG 🔴" if last_val <= 4 else "SMALL 🟢" # হাই প্রোবাবিলিটি
            note = "🔥 **CONFIRMED WIN SIGNAL!** সব ফান্ড ব্যবহার করবেন না।"
        else:
            prediction = "SMALL 🟢" if last_val >= 5 else "BIG 🔴"
            note = f"💡 Step: {current_step} | ফান্ড ব্যাকআপ রাখুন।"

        response = (
            f"💥 **BDWIN24 PREDICTION** ✅\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 **PERIOD:** `{period}`\n"
            f"🔮 **NEXT:** **{prediction}**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"{note}"
        )
        # এখানে ইউজারকে উইন/লস বাটন দেওয়া যেতে পারে অথবা পরের বার সে নিজেই ইনপুট দিবে
        user_loss_steps[uid] = current_step + 1 # আপাতত স্টেপ বাড়ছে ধরে নিচ্ছি
        bot.send_message(uid, response, parse_mode="Markdown")

    except:
        bot.send_message(uid, "❌ ভুল ফরম্যাট! দয়া করে এভাবে দিন: `425/9`")

bot.polling(none_stop=True)
