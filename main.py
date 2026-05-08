import telebot
from telebot import types
import random

# আপনার তথ্যগুলো এখানে সংরক্ষিত
API_TOKEN = '8792313235:AAGLv8pmNBm8G2emNK4TW67am45VvFNF5nU'
ADMIN_ID = 7911996579 

bot = telebot.TeleBot(API_TOKEN)
verified_users = {}

# রেজিস্ট্রেশন লিংক
REGISTRATION_LINK = "https://21bdwin24.com/register?inviteCode=VFNRBPN&from=web"

@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "💥 **WELCOME TO VIP WINGO PREDICTOR** ✅\n\n"
        "বটের সিগন্যাল পেতে হলে আপনাকে আমাদের রেফার লিংকে একাউন্ট খুলে ডিপোজিট করতে হবে।\n\n"
        f"🔗 [একাউন্ট খুলতে এখানে ক্লিক করুন]({REGISTRATION_LINK})\n\n"
        "✅ একাউন্ট খুলে ডিপোজিট করার পর স্ক্রিনশট এখানে পাঠান। অ্যাডমিন আপনাকে ভেরিফাই করে দেবে।"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "✅ আপনার স্ক্রিনশট জমা হয়েছে। অ্যাডমিন চেক করে আপনাকে ভেরিফাই করে দেবে।")
    bot.send_message(ADMIN_ID, f"নতুন ইউজার রিকোয়েস্ট!\nID: `{message.chat.id}`\nঅ্যাপ্রুভ করতে লিখুন: `/approve {message.chat.id}`")

@bot.message_handler(commands=['approve'])
def approve(message):
    if message.from_user.id == ADMIN_ID:
        try:
            uid = int(message.text.split()[1])
            verified_users[uid] = True
            bot.send_message(uid, "🎊 অভিনন্দন! আপনি এখন VIP ভেরিফাইড ইউজার।\n\n👉 সিগন্যাল পেতে পিরিয়ডের **শেষ ৩ ডিজিট** লিখে পাঠান।")
        except:
            bot.reply_to(message, "সঠিক ফরম্যাট: /approve ID")

@bot.message_handler(func=lambda message: True)
def give_signal(message):
    if message.chat.id in verified_users:
        period_input = message.text
        if period_input.isdigit() and len(period_input) >= 3:
            prediction = random.choice(["BIG 🔴", "SMALL 🟢"])
            
            # বাটন তৈরি
            markup = types.InlineKeyboardMarkup()
            item1 = types.InlineKeyboardButton("WIN ✅", callback_data="win")
            item2 = types.InlineKeyboardButton("LOSS ❌", callback_data="loss")
            markup.add(item1, item2)

            signal_text = (
                f"💥 **BDWIN24 WINGO 1 MIN** ✅\n\n"
                f"🔺 **FOLLOW 5-6 STAGE** 💯🔻\n\n"
                f"🔹 **PERIOD: {period_input}**\n"
                f"🔹 **RESULT: {prediction}**\n\n"
                f"⚠️ অবশ্যই ৫-৬ স্টেপ ফান্ড মেইনটেইন করবেন। রেজাল্ট কী আসলো নিচের বাটনে ক্লিক করুন 👇"
            )
            bot.send_message(message.chat.id, signal_text, parse_mode='Markdown', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "❌ সঠিক পিরিয়ড নম্বর লিখুন।")
    else:
        bot.send_message(message.chat.id, "🚫 আপনি ভেরিফাইড নন।")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "win":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                             text="🎊 **CONGRATULATIONS! WE WON!** 💰\n\nআপনার ব্যালেন্স চেক করুন। পরবর্তী সিগন্যালের জন্য নতুন পিরিয়ড নম্বর লিখুন।")
    elif call.data == "loss":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                             text="😔 **LOSS! DON'T WORRY!**\n\nপরবর্তী লেভেল (3X) ফলো করুন এবং ৫-৬ স্টেপ ফান্ড রাখুন। নতুন পিরিয়ড নম্বর লিখে পাঠান।")

bot.infinity_polling()
        
