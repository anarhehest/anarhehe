import json
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ChatJoinRequestHandler, ContextTypes
from telegram.helpers import escape_markdown

load_dotenv()

_l = {
    'mention': lambda t,u: f'{t}\t[{escape_markdown(u.full_name, version=2)}](tg://user?id={u.id})',
    'new_request': {
        'poll': {
            'text': lambda t,u: f'{t[0]} {u.full_name} {t[1]}',
        }
    }
}

cfg = { 'bot': {
    'group': os.getenv('GROUP_ID'),
    'topic': os.getenv('TOPIC_ID'),
    'token': os.getenv('BOT_TOKEN'),
}}
assert all(cfg['bot'].values())

with open('messages.json', 'r') as f:
    txt = json.load(f)


async def handle_join_request(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    await context.bot.send_message(
        chat_id=cfg['bot']['group'],
        message_thread_id=cfg['bot']['topic'],
        text=_l['mention'](txt['new_request']['text'], user),
        parse_mode='MarkdownV2'
    )
    await context.bot.send_poll(
        chat_id=cfg['bot']['group'],
        message_thread_id=cfg['bot']['topic'],
        question=_l['new_request']['poll']['text'](txt['new_request']['poll']['text'], user),
        options=txt['new_request']['poll']['options'],
        is_anonymous=False,
        allows_multiple_answers=False
    )


app = ApplicationBuilder().token(cfg['bot']['token']).build()
app.add_handler(ChatJoinRequestHandler(handle_join_request))
app.run_polling()