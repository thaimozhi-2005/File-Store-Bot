import os
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message

# Telegraph/Graph.org upload endpoint
TELEGRAPH_URL = "https://graph.org/upload"

async def upload_to_telegraph(file_path):
    endpoints = [
        "https://graph.org/upload",
        "https://telegra.ph/upload"
    ]
    for url in endpoints:
        try:
            async with aiohttp.ClientSession() as session:
                with open(file_path, 'rb') as f:
                    async with session.post(url, data={'file': f}, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            if isinstance(data, list) and len(data) > 0:
                                base_url = "https://graph.org" if "graph.org" in url else "https://telegra.ph"
                                return f"{base_url}{data[0]['src']}"
        except Exception as e:
            print(f"Telegraph upload error for {url}: {e}")
            continue
    return None

@Client.on_message(filters.private & filters.command(["telegraph", "img", "tgt"]))
async def telegraph_upload(client, message: Message):
    if message.from_user.id not in client.admins:
        return
    
    replied = message.reply_to_message
    if not replied or not (replied.photo or replied.video or replied.animation or replied.document):
        return await message.reply("<blockquote>✗ ᴇʀʀᴏʀ</blockquote>\n\nʀᴇᴘʟʏ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ ᴏʀ ᴠɪᴅᴇᴏ ᴛᴏ ᴜᴘʟᴏᴀᴅ ɪᴛ ᴛᴏ ɢʀᴀᴘʜ.ᴏʀɢ")

    # Filter out large files (graph.org limit is usually 5MB)
    file_size = 0
    if replied.photo: file_size = replied.photo.file_size
    elif replied.video: file_size = replied.video.file_size
    elif replied.animation: file_size = replied.animation.file_size
    elif replied.document: file_size = replied.document.file_size
    
    if file_size > 5 * 1024 * 1024:
        return await message.reply("<blockquote>✗ ᴇʀʀᴏʀ</blockquote>\n\nꜰɪʟᴇ sɪᴢᴇ ᴛᴏᴏ ʟᴀʀɢᴇ! ᴍᴀxɪᴍᴜᴍ ʟɪᴍɪᴛ ɪs 5ᴍʙ.")

    status = await message.reply("<blockquote>🚀 ᴜᴘʟᴏᴀᴅɪɴɢ...</blockquote>", quote=True)
    
    try:
        file_path = await replied.download()
        url = await upload_to_telegraph(file_path)
        
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            
        if url:
            await status.edit(f"<blockquote>✓ ᴜᴘʟᴏᴀᴅ ᴄᴏᴍᴘʟᴇᴛᴇ!</blockquote>\n\n<code>{url}</code>")
        else:
            await status.edit("<blockquote>✗ ꜰᴀɪʟᴇᴅ ᴛᴏ ᴜᴘʟᴏᴀᴅ!</blockquote>")
            
    except Exception as e:
        if 'status' in locals():
            await status.edit(f"<blockquote>✗ ᴇʀʀᴏʀ:</blockquote> <code>{e}</code>")
