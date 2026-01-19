from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import os

BOT_TOKEN = "8286971022:AAHkgKK29gM2J4lMIDW6hvma334Gjce6PXQ"
OWNER_ID = 8002803133
SERVER_UPLOAD_URL = 'http://localhost:5000/upload'

def start(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        update.message.reply_text("❌ Unauthorized")
        return
    update.message.reply_text("Send me a video to upload to the streaming site.")

def receive_video(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        update.message.reply_text("❌ Unauthorized")
        return

    video = update.message.video or update.message.document
    if not video:
        update.message.reply_text("Send a valid video")
        return

    file = video.get_file()
    filename = video.file_name or "video.mp4"
    file.download(filename)

    # Upload to server
    with open(filename, 'rb') as f:
        r = requests.post(SERVER_UPLOAD_URL, files={'video': f})

    update.message.reply_text(r.text)
    os.remove(filename)

updater = Updater(BOT_TOKEN)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.video | Filters.document, receive_video))
updater.start_polling()
updater.idle()
