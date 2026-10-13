import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")
# Canal público configurado como servidor
CANAL_PUBLICO = "@fullpelis_storage"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Envíame un enlace de video .mp4. "
        "Lo guardaré en el canal de respaldo y te generaré un enlace público."
    )

async def procesar_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url_video = update.message.text
    
    if not url_video.startswith("http"):
        await update.message.reply_text("Por favor, envía un enlace válido que comience con http o https.")
        return

    msg = await update.message.reply_text("⏳ Subiendo el video al canal servidor...")

    try:
        # 1. Envía el video directamente al canal público configurado
        mensaje_en_canal = await context.bot.send_video(
            chat_id=CANAL_PUBLICO,
            video=url_video,
            caption="Video subido desde el bot."
        )
        
        # 2. Obtiene el enlace público único del mensaje en el canal (t.me/canal/id)
        message_id = mensaje_en_canal.message_id
        canal_username = CANAL_PUBLICO.replace("@", "")
        enlace_publico = f"https://t.me/{canal_username}/{message_id}"
        
        # 3. Le responde al usuario con el enlace generado
        await msg.edit_text(
            f"✅ **¡Video procesado con éxito!**\n\n"
            f"🔗 **Tu enlace público es:**\n{enlace_publico}",
            parse_mode="Markdown"
        )

    except Exception as e:
        await msg.edit_text(f"Hubo un error al procesar el video: {str(e)}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, procesar_video))
    
    print("Bot iniciado correctamente...")
    app.run_polling()

if __name__ == "__main__":
    main()
