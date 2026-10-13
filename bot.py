import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Servidor HTTP básico para satisfacer el requisito de puertos de Render
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

TOKEN = os.getenv("TELEGRAM_TOKEN")
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
        mensaje_en_canal = await context.bot.send_video(
            chat_id=CANAL_PUBLICO,
            video=url_video,
            caption="Video subido desde el bot."
        )
        
        message_id = mensaje_en_canal.message_id
        canal_username = CANAL_PUBLICO.replace("@", "")
        enlace_publico = f"https://t.me/{canal_username}/{message_id}"
        
        await msg.edit_text(
            f"✅ **¡Video procesado con éxito!**\n\n"
            f"🔗 **Tu enlace público es:**\n{enlace_publico}",
            parse_mode="Markdown"
        )

    except Exception as e:
        await msg.edit_text(f"Hubo un error al procesar el video: {str(e)}")

def main():
    # Iniciar el servidor web en un hilo separado para que Render detecte el puerto abierto
    t = threading.Thread(target=run_web_server, daemon=True)
    t.start()

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, procesar_video))
    
    print("Bot iniciado correctamente...")
    app.run_polling()

if __name__ == "__main__":
    main()
