import os
import telebot
import yt_dlp

TOKEN = "8607204890:AAE7yC6H97jydF1hpU0HFvg5sd_2t-7UOSE"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "⚡ Welcome to Link4kMediaBot!\n\nYouTube ya Instagram ka link bhejein. Main video download kar raha hoon!")

@bot.message_handler(func=lambda message: True)
def handle_download(message):
    url = message.text.strip()
    
    if not url.startswith("http"):
        bot.reply_to(message, "❌ Kripya ek valid URL (link) bhejein.")
        return

    msg = bot.reply_to(message, "⏳ Link process ho raha hai, please wait...")
    
    output_template = 'downloaded_video.%(ext)s'
    ydl_opts = {
        'outtmpl': output_template,
        'format': 'best[filesize<50M]/best[height<=720]/best',
    }

    try:
        bot.edit_message_text("📥 Video download ho raha hai...", chat_id=message.chat.id, message_id=msg.message_id)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)

        file_size = os.path.getsize(filename) / (1024 * 1024)
        
        if file_size > 50:
            bot.edit_message_text(f"❌ Video ka size ({file_size:.1f}MB) 50MB se bada hai.", chat_id=message.chat.id, message_id=msg.message_id)
            os.remove(filename)
            return

        bot.edit_message_text("📤 Telegram par bhej raha hoon...", chat_id=message.chat.id, message_id=msg.message_id)
        
        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video, timeout=120)
        
        os.remove(filename)
        bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ Error aa gaya: {str(e)}", chat_id=message.chat.id, message_id=msg.message_id)

bot.infinity_polling()
