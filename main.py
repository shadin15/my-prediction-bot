import telebot
import random
import time
import datetime
from telebot import types

# আপনার টোকেন এবং নতুন এডমিন আইডি
API_TOKEN = '8792313235:AAGLv8pmNBm8G2emNK4TW67am45VvFNF5nU'
ADMIN_ID = 7911996579 

bot = telebot.TeleBot(API_TOKEN)

approved_users = set()
# মেম্বারের স্টেট ট্র্যাকিং
user_data = {} 

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
            return True, end_time
    return False, None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 **Welcome to BDWIN24 Official AI Bot!** 🤖\n\n"
        f"🔗 [একাউন্ট খুলতে এখানে ক্লিক করুন]({REFERRAL_LINK})\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✅ সিগন্যাল পেতে ডিপোজিট স্ক্রিনশট এবং UID পাঠান।\n"
        "✅ অ্যাডমিন এপ্রুভ করলে সিগন্যাল বাটন কাজ করবে।"
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
    bot.send_message(user_id, "⏳ আপনার তথ্য অ্যাডমিনকে পাঠানো হয়েছে। এপ্রুভ হওয়া পর্যন্ত অপেক্ষা করুন।")

@bot.callback_query_handler(func=lambda call: call.data.startswith('approve_'))
def approve_user(call):
    target_id = int(call.data.split('_')[1])
    approved_users.add(target_id)
    bot.send_message(target_id, "🎉 অভিনন্দন! আপনি এপ্রুভ হয়েছেন। এখন সেশন টাইমে সিগন্যাল নিতে পারবেন।")
    bot.edit_message_caption("✅ Approved!", chat_id=ADMIN_ID, message_id=call.message.message_id)

@bot.message_handler(func=lambda message: message.text == "Get AI Signal 🚀")
def handle_signal_request(message):
    uid = message.chat.id
    if uid not in approved_users and uid != ADMIN_ID:
        bot.send_message(uid, "🚫 আপনি এপ্রুভড নন। আগে স্ক্রিনশট পাঠিয়ে ভেরিফাই করুন।")
        return

    # Strict Check: আগের রেজাল্ট না দিলে নতুন সিগন্যাল লক
    if uid in user_data and user_data[uid].get('waiting_result'):
        bot.send_message(uid, "⚠️ **সতর্কতা!** আগে দেওয়া সিগন্যালের রেজাল্ট জানাননি।\nদয়া করে WIN অথবা LOSS বাটনে ক্লিক করুন।")
        return

    active, end_time = is_session_active()
    # সেশন শেষ হলেও যদি লস রিকভারি বাকি থাকে (স্টেপ > ১) তবে সিগন্যাল দিবে
    if not active and user_data.get(uid, {}).get('step', 1) == 1:
        bot.send_message(uid, "❌ বর্তমানে কোনো সেশন নেই। পরবর্তী সেশনের জন্য অপেক্ষা করুন। ⏳")
        return

    msg = bot.send_message(uid, "📝 বর্তমান পিরিয়ড এবং রেজাল্ট দিন (যেমন: `425/9`)")
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

        # ৬-স্টেপ গ্যারান্টি লজিক
        if step >= 5:
            bot.send_message(uid, "🔍 AI মার্কেট এনালাইসিস করছে... (৫ সেকেন্ড)")
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

        amount = 10 * (2**(step-1)) # ১০, ২০, ৪০, ৮০...
        response = (
            f"🎯 **STEP {step} SIGNAL** ✅\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🔹 **PERIOD:** `{period}`\n"
            f"🔮 **PREDICTION:** **{prediction}**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 **ফান্ড:** {amount} টাকা\n\n"
            f"⚠️ রেজাল্ট জানানো ছাড়া পরবর্তী সিগন্যাল আসবে না।"
        )
        bot.send_message(uid, response, parse_mode="Markdown", reply_markup=markup)

    except:
        bot.send_message(uid, "❌ ভুল ফরম্যাট! পিরিয়ড এবং রেজাল্ট এভাবে দিন: `425/9`")

@bot.callback_query_handler(func=lambda call: call.data.startswith('res_'))
def handle_result(call):
    uid = call.message.chat.id
    if uid not in user_data: return
    
    if call.data == "res_win":
        user_data[uid]['step'] = 1 
        user_data[uid]['waiting_result'] = False 
        bot.edit_message_text("🎉 **SUPER WIN!!** অভিনন্দন।\nপরের সিগন্যালের জন্য আবার 'Get Signal' ক্লিক করুন।", uid, call.message.message_id)
    
    elif call.data == "res_loss":
        if user_data[uid]['step'] < 6:
            user_data[uid]['step'] += 1 
            user_data[uid]['waiting_result'] = False 
            bot.edit_message_text(f"⚠️ লস হয়েছে! ঘাবড়াবেন না।\nস্টেপ {user_data[uid]['step']} রিকভারি সিগন্যাল নিতে আবার ইনপুট দিন।", uid, call.message.message_id)
        else:
            user_data[uid]['step'] = 1
            user_data[uid]['waiting_result'] = False
            bot.edit_message_text("🚫 সেশন রিকভারি ব্যর্থ। মার্কেট অতিরিক্ত খারাপ, সেশন অফ করা হলো।", uid, call.message.message_id)

bot.polling(none_stop=True)
        
