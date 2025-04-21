import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler, ContextTypes
from telegram.helpers import escape_markdown

load_dotenv()

_l = {
    'mention': lambda u: f'[{escape_markdown(u.full_name, version=2)}](tg://user?id={u.id})'
}

cfg = { 'bot': {
    'group': os.getenv('GROUP_ID'),
    'topic': os.getenv('TOPIC_ID'),
    'token': os.getenv('BOT_TOKEN'),
}}

async def handle_join_request(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    await context.bot.send_message(
        chat_id=cfg['bot']['group'],
        message_thread_id=cfg['bot']['topic'],
        text='*New join request:*\t' + _l['mention'](user),
        parse_mode='MarkdownV2'
    )
    
app = ApplicationBuilder().token(cfg['bot']['token']).build()
app.add_handler(ChatJoinRequestHandler(handle_join_request))
app.run_polling()