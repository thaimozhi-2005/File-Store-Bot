import asyncio
import logging

from bot import Bot, web_app
from pyrogram import compose
from pyrogram.errors import FloodWait
from config import *

log = logging.getLogger(__name__)

async def main():
    app = []
    app.append(
        Bot(
            SESSION,
            WORKERS,
            DB_CHANNEL,
            FSUBS,
            TOKEN,
            ADMINS,
            MESSAGES,
            AUTO_DEL,
            DB_URI,
            DB_NAME,
            API_ID,
            API_HASH,
            PROTECT,
            DISABLE_BTN
        )
    )

    # Handle FloodWait on startup - wait and retry instead of crashing
    while True:
        try:
            await compose(app)
            break
        except FloodWait as e:
            wait = e.value if hasattr(e, 'value') else e.x
            log.warning(f"FloodWait on startup! Waiting {wait} seconds before retrying...")
            await asyncio.sleep(wait + 10)
        except Exception as e:
            log.error(f"Startup error: {e}")
            raise


async def runner():
    await asyncio.gather(
        main(),
        web_app()
    )

asyncio.run(runner())
