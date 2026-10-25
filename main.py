import asyncio

from admin.admins import router as admins_router
from admin.create_notification import router as notification_router
from admin.panel import router as admin_panel_router
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from config import BOT_TOKEN
from database import init_admins, init_db, is_admin
from handlers.monitor import router as monitor_router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):

    if not is_admin(message.from_user.id):
        await message.answer(
            '<tg-emoji emoji-id="5445092669522996408">❌</tg-emoji> ACCESS DENIED!!' \
            ' You are not authorized. Please contact the admin. ',
            parse_mode="HTML"
        )
        return

    user_name = message.from_user.first_name

    text = f"""<tg-emoji emoji-id="5247133031235329609">👋</tg-emoji> <b>Hello, {user_name}</b>
<tg-emoji emoji-id="5316742794562254812">⚡</tg-emoji> <b>Welcome to the VOLT Instagram Monitor Bot</b>
A powerful and simple monitoring system designed to track Instagram account availability and automatically notify you when the monitored status changes.
   
<tg-emoji emoji-id="5940433880585605708">🛠</tg-emoji> <b>HOW IT WORKS</b>
━━━━━━━━━━━━━━━━━━━━━━

Add an Instagram username to monitoring and VOLT will continuously check its status.
<tg-emoji emoji-id="5447463040498804016">🚨</tg-emoji> <b>Active Monitor</b> Monitors an active account until it becomes unavailable.
<tg-emoji emoji-id="5447463040498804016">🏆</tg-emoji> <b>Unactive Monitor</b> Monitors an unavailable account until it becomes available again.
<tg-emoji emoji-id="5447463040498804016">📸</tg-emoji> When the target status is detected, VOLT automatically stops the monitor and sends a detailed notification with the profile card and detected information.

<tg-emoji emoji-id="5960714428394507968">📌</tg-emoji> <b>MONITORING COMMANDS</b>
━━━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="5960714428394507968">👁</tg-emoji> <code>/monitor_active username</code> Start monitoring an active account until it becomes unavailable.
<tg-emoji emoji-id="5960714428394507968">🏆</tg-emoji> <code>/monitor_unactive username</code> Start monitoring an unavailable account until it becomes available again.
<tg-emoji emoji-id="6037243349675544634">🛑</tg-emoji> <code>/cancel username</code> Stop monitoring a specific username.
<tg-emoji emoji-id="6037243349675544634">🛑</tg-emoji> <code>/cancel_all</code> Stop all currently running monitors.
<tg-emoji emoji-id="5904219717073114606">📋</tg-emoji> <code>/monitors</code> View all currently active monitors.

<tg-emoji emoji-id="5960714428394507968">🔎</tg-emoji> <code>/monitor_info username</code> View detailed information about a specific monitor.

<tg-emoji emoji-id="5891207662678317861">📊</tg-emoji> <b>ADMIN & CONTROL</b>
━━━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="5891207662678317861">⚙️</tg-emoji> <code>/admin</code> Open the VOLT admin dashboard.
<tg-emoji emoji-id="5870921681735781843">📈</tg-emoji> <code>/stats</code> View monitoring statistics and completed monitors.

<tg-emoji emoji-id="5870527021485919704">🧪</tg-emoji> <b>NOTIFICATION TOOLS</b>
━━━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="5316554554735607106">🚨</tg-emoji> <code>/create_ban</code> Create a custom/test banned-account notification with a profile card.
<tg-emoji emoji-id="5348129380474306311">🏆</tg-emoji> <code>/create_unban</code> Create a custom/test recovered-account notification with a profile card.

<tg-emoji emoji-id="5316992572680320646">👑</tg-emoji> <b>ADMIN MANAGEMENT</b>
━━━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="5258362837411045098">🚨</tg-emoji> <code>/add userid</code> Add a Telegram user as an administrator.
<tg-emoji emoji-id="5408946499637752036">🚨</tg-emoji> <code>/remove userid</code> Remove an administrator from the bot.
<tg-emoji emoji-id="5258362837411045098">🚨</tg-emoji> <code>/admins</code> View the current administrator list.
━━━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="5920515922505765329">⚡</tg-emoji> <b>Fast • Automated • Reliable</b>
<tg-emoji emoji-id="5474348994605891991">🟢</tg-emoji> <b>VOLT Instagram Monitor</b>"""

    await message.answer(
        text,
        parse_mode="HTML",
    )


dp.include_router(monitor_router)
dp.include_router(admin_panel_router)
dp.include_router(notification_router)
dp.include_router(admins_router)

async def main():
    print("Bot is starting...")

    init_db()
    init_admins()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())