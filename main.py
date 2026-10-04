import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "893502667:AAF08umiXUYMK4F45pU19RdYWpNcon0rhGY"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হ্যালো! আমি লিঙ্ক বাইপাস বোট। আপনার লিঙ্কটি এখানে পাঠান।")

async def auto_delete_job(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    try:
        await context.bot.delete_message(chat_id=job_data['chat_id'], message_id=job_data['message_id'])
    except Exception as e:
        logging.error(f"Error deleting message: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.effective_chat.id
    
    # লিঙ্ক পাঠানোর পর উত্তর
    sent_message = await update.message.reply_text(f"আপনার লিঙ্ক প্রসেস করা হচ্ছে: {user_text}")
    
    # ১০ সেকেন্ড পর মেসেজ মুছে ফেলার ব্যবস্থা
    if context.job_queue:
        context.job_queue.run_once(auto_delete_job, 10, data={
            'chat_id': chat_id,
            'message_id': sent_message.message_id
        })

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.run_polling()

if __name__ == '__main__':
    main()
