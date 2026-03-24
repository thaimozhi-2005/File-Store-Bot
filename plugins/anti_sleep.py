"""
Anti-sleep plugin for Render.
Pings the bot's own web URL every 5 minutes to prevent Render free tier from sleeping.
Set RENDER_URL environment variable to your Render URL (e.g. https://my-bot.onrender.com)
"""
import asyncio
import os
import aiohttp
from pyrogram import Client

RENDER_URL = os.environ.get("RENDER_URL", "")
PING_INTERVAL = 4 * 60  # 4 minutes


async def keep_alive_loop():
    if not RENDER_URL:
        return
    await asyncio.sleep(30)  # wait for bot to fully start
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(RENDER_URL, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    print(f"[Anti-Sleep] Pinged {RENDER_URL} → {resp.status}")
            except Exception as e:
                print(f"[Anti-Sleep] Ping failed: {e}")
            await asyncio.sleep(PING_INTERVAL)


# Hook into bot startup
original_start = Client.start.__wrapped__ if hasattr(Client.start, "__wrapped__") else None

async def _patched_start(self):
    await Client.start(self)
    asyncio.create_task(keep_alive_loop())
