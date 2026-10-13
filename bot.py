import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id

    if url.startswith("http") and ".mp4" in url.lower():
        await context.bot.send_message(chat_id=chat_id, text="Procesando video...")
        try:
            await context.bot.send_video(chat_id=chat_id, video=url)
        except Exception as e:
            await context.bot.send_message(chat_id=chat_id, text=f"Error al enviar el video: {str(e)}")
    else:
        await context.bot.send_message(chat_id=chat_id, text="Envía un enlace directo válido que contenga .mp4")

if __name__ == '__main__':
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    
    application = ApplicationBuilder().token(TOKEN).build()
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_url)
    application.add_handler(text_handler)

    print("Bot iniciado correctamente...")
    application.run_polling()
