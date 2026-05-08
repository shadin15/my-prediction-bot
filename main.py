import telebot
import random

# আপনার দেওয়া তথ্যগুলো সরাসরি বসিয়ে দেওয়া হয়েছে
API_TOKEN = '8792313235:AAGLv8pmNBm8G2emNK4TW67am45VvFNF5nU'
ADMIN_ID = 7911996579 

bot = telebot.TeleBot(API_TOKEN)
verified_users = {}

# আপনার নতুন সাইটের রেফার লিংক
REGISTRATION_LINK = "https://21bdwin24.com/register?inviteCode=VFNRBPN&from=web"

@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "💥 **WELCOME TO VIP WINGO PREDICTOR** ✅\n\n"
        "বটের সিগন্যাল পেতে হলে আপনাকে আমাদের রেফার লিংকে একাউন্ট খুলে ডিপোজিট করতে হবে।\n\n"
        f"🔗 [একাউন্ট খুলতে এখানে ক্লিক করুন]({REGISTRATION_LINK})\n\n"
        "✅ একাউন্ট খুলে ডিপোজিট করার পর স্ক্রিনশট এখানে পাঠান। অ্যাডমিন আপনাকে চেক করে VIP এক্সেস দিয়ে দেবে।"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "✅ আপনার স্ক্রিনশট জমা হয়েছে। অ্যাডমিন চেক করে আপনাকে ভেরিফাই করে দেবে।")
    bot.send_message(ADMIN_ID, f"নতুন ইউজার রিকোয়েস্ট!\nID: `{message.chat.id}`\nঅ্যাপ্রুভ করতে নিচের লেখাটি কপি করে পাঠান:\n\n`/approve {message.chat.id}`", parse_mode='Markdown')

@bot.message_handler(commands=['approve'])
def approve(message):
    if message.from_user.id == ADMIN_ID:
        try:
            uid = int(message.text.split()[1])
            verified_users[uid] = True
            bot.send_message(uid, "🎊 অভিনন্দন! আপনি এখন VIP ভেরিফাইড ইউজার।\n\n"
                                 "👉 সিগন্যাল পেতে এখন যে পিরিয়ডে খেলছেন তার **শেষ ৩ বা ৪ ডিজিট** এখানে লিখে পাঠান।")
        except:
            bot.reply_to(message, "ভুল ফরম্যাট! লিখুন: /approve 12345678")

@bot.message_handler(func=lambda message: True)
def give_signal(message):
    if message.chat.id in verified_users:
        period_input = message.text
        if period_input.isdigit() and len(period_input) >= 3:
            prediction = random.choice(["BIG 🔴", "SMALL 🟢"])
            
            signal_text = (
                f"💥 **BDWIN24 WINGO 1 MINUTE** ✅\n\n"
                f"🔺 **FOLLOW 5 STAGE** 💯🔻\n\n"
                f"🔹 **PD-{period_input}-{prediction}**\n\n"
                f"⚠️ অবশ্যই ৫ স্টেপ ফান্ড মেইনটেইন করবেন।"
            )
            bot.send_message(message.chat.id, signal_text, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "❌ দয়া করে সঠিক পিরিয়ড নম্বর (শেষ ৩ বা ৪ ডিজিট) লিখুন।")
    else:
        bot.send_message(message.chat.id, "🚫 আপনি এখনো ভেরিফাইড নন। সিগন্যাল পেতে অ্যাডমিনকে স্ক্রিনশট পাঠান।")

bot.infinity_polling()
