import asyncio
import os
from aiohttp import web
from aiogram import Bot

# ⚠️ ВСТАВЬ НОВЫЙ ТОКЕН (после отзыва старого!)
BOT_TOKEN = "9180266879:AAFCthTTTiGUgFWqmudaSHPggTDCSFq5O2Q"

# Твой Telegram ID (получатель уведомлений)
ADMIN_ID = 6040186314

bot = Bot(token=BOT_TOKEN)

async def handle_invite(request):
    try:
        data = await request.json()
        day = data.get("day", "—")
        time = data.get("time", "—")
        place = data.get("place", "—")

        text = (
            f"💌 *Yangi taklif qabul qilindi!*\n\n"
            f"📅 Kun: *{day}*\n"
            f"⏰ Vaqt: *{time}*\n"
            f"📍 Joy: *{place}*\n\n"
            f"🐱 Mushukchalar ma'qulladi!"
        )

        await bot.send_message(ADMIN_ID, text, parse_mode="Markdown")

        return web.json_response({"ok": True}, headers={
            "Access-Control-Allow-Origin": "*"
        })
    except Exception as e:
        print(f"Ошибка: {e}")
        return web.json_response({"ok": False, "error": str(e)}, status=400, headers={
            "Access-Control-Allow-Origin": "*"
        })

async def handle_options(request):
    return web.Response(headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    })

async def main():
    app = web.Application()
    app.router.add_post("/invite", handle_invite)
    app.router.add_options("/invite", handle_options)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

    print("✅ Сервер запущен на порту 8080")
    print("📡 Ожидаю запросы от сайта на http://localhost:8080/invite")

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())