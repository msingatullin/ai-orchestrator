from __future__ import annotations
import logging, os
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, Defaults, CallbackContext

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
log = logging.getLogger("bot")

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN or TOKEN.startswith("YOUR_"):
    raise RuntimeError("TELEGRAM_BOT_TOKEN не задан — впишите его в .env")

HELP = "🛠 *AI-Оркестратор*\\n\\n/start — приветствие\\n/help — справка"

async def start(update: Update, ctx: CallbackContext.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Напишите /help для помощи.")

async def help_(update: Update, ctx: CallbackContext.DEFAULT_TYPE):
    await update.message.reply_text(HELP)

def main() -> None:
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_))
    log.info("🚀 Bot starting …")
    app.run_polling(drop_pending_updates=True, stop_signals=None)

if __name__ == "__main__":
    main()
