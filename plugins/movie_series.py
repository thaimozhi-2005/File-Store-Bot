import io
from pyrogram import Client, filters
from pyrogram.types import Message
from helper.helper_func import encode

ACTIVE_SESSIONS = {}

def get_human_size(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"

# Command to start movie collection
@Client.on_message(filters.private & filters.command("movie"))
async def start_movie(client: Client, message: Message):
    if message.from_user.id not in client.admins:
        return
    if len(message.command) < 2:
        return await message.reply("<blockquote>✗ ᴇʀʀᴏʀ</blockquote>\n\nᴜsᴇ: `/movie {movie name}`", quote=True)
    title = message.text.split(" ", 1)[1]
    ACTIVE_SESSIONS[message.from_user.id] = {"type": "movie", "title": title, "files": [], "msg_ids": []}
    
    await message.reply(f"<blockquote>🍿 Mᴏᴠɪᴇ Sᴇᴛᴜᴘ: {title}</blockquote>\n\nSᴇɴᴅ ᴏʀ ꜰᴏʀᴡᴀʀᴅ ᴀʟʟ ᴛʜᴇ ᴍᴏᴠɪᴇ ꜰɪʟᴇs ɴᴏᴡ.\nEᴠᴇɴ ɪꜰ ʏᴏᴜ sᴇɴᴅ/ꜰᴏʀᴡᴀʀᴅ 15+ ꜰɪʟᴇs ᴀᴛ ᴏɴᴄᴇ, ɪᴛ ᴡɪʟʟ ᴘʀᴏᴄᴇss! Wʜᴇɴ ʏᴏᴜ ᴀʀᴇ ᴅᴏɴᴇ, sᴇɴᴅ `/done` ᴛᴏ ɢᴇᴛ ᴛʜᴇ ꜰɪɴᴀʟ ʟɪsᴛ.", quote=True)

# Command to start series collection
@Client.on_message(filters.private & filters.command("series"))
async def start_series(client: Client, message: Message):
    if message.from_user.id not in client.admins:
        return
    if len(message.command) < 2:
        return await message.reply("<blockquote>✗ ᴇʀʀᴏʀ</blockquote>\n\nᴜsᴇ: `/series {series name and quality}`", quote=True)
    title = message.text.split(" ", 1)[1]
    ACTIVE_SESSIONS[message.from_user.id] = {"type": "series", "title": title, "files": [], "msg_ids": []}
    
    await message.reply(f"<blockquote>📺 Sᴇʀɪᴇs Sᴇᴛᴜᴘ: {title}</blockquote>\n\nSᴇɴᴅ ᴏʀ ꜰᴏʀᴡᴀʀᴅ ᴀʟʟ ᴛʜᴇ ᴇᴘɪsᴏᴅᴇ ꜰɪʟᴇs ɴᴏᴡ.\nYᴏᴜ ᴄᴀɴ sᴇɴᴅ/ꜰᴏʀᴡᴀʀᴅ 15+ ꜰɪʟᴇs ᴀᴛ ᴏɴᴄᴇ! Wʜᴇɴ ʏᴏᴜ ᴀʀᴇ ᴅᴏɴᴇ, sᴇɴᴅ `/done` ᴛᴏ ɢᴇᴛ ᴛʜᴇ ꜰɪɴᴀʟ ʟɪsᴛ ᴡɪᴛʜ Bᴀᴛᴄʜ Lɪɴᴋ.", quote=True)

import re

def extract_episode(filename):
    # Try to find episode number (e.g. E01, Ep 1, Episode 01, S01E01)
    patterns = [
        r".*[sS]\d+[eE](\d+).*",
        r".*[eE]pisode\s*(\d+).*",
        r".*[eE]p\s*(\d+).*",
        r".*[eE](\d+).*",
        r".*?\s+(\d+)\s+.*", # 01 in the middle
    ]
    for p in patterns:
        match = re.match(p, filename)
        if match:
            return match.group(1).zfill(2)
    return None

# Main file listener
@Client.on_message(filters.private & (filters.document | filters.video | filters.audio), group=-1)
async def file_receiver(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id in ACTIVE_SESSIONS:
        # Process the file, stop propagate meaning channel_post.py ignores it!
        message.stop_propagation()
        
        file_size = 0
        file_name = "Unknown_File"
        if getattr(message, "document", None): 
            file_size = message.document.file_size
            file_name = message.document.file_name
        elif getattr(message, "video", None): 
            file_size = message.video.file_size
            file_name = message.video.file_name
        elif getattr(message, "audio", None): 
            file_size = message.audio.file_size
            file_name = message.audio.file_name
        
        # Forward to DB
        try:
            post_message = await message.copy(chat_id=client.db, disable_notification=True)
        except Exception as e:
            await message.reply(f"❌ Error forwarding to DB: {e}")
            return

        ACTIVE_SESSIONS[user_id]["msg_ids"].append(post_message.id)
        
        converted_id = post_message.id * abs(client.db)
        base64_string = await encode(f"get-{converted_id}")
        link = f"https://t.me/{client.username}?start={base64_string}"
        
        sess_type = ACTIVE_SESSIONS[user_id]["type"]
        
        if sess_type == "movie":
            size_str = get_human_size(file_size)
            ACTIVE_SESSIONS[user_id]["files"].append(f"{size_str} : {link}")
        else:
            ep_num = extract_episode(file_name)
            ACTIVE_SESSIONS[user_id]["files"].append({"name": file_name, "link": link, "ep": ep_num})
        
        
@Client.on_message(filters.private & filters.command("done"), group=-1)
async def done_command(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in ACTIVE_SESSIONS:
        return
        
    message.stop_propagation()
    
    session = ACTIVE_SESSIONS.pop(user_id)
    files = session["files"]
    title = session["title"]
    
    if not files:
        return await message.reply("❌ Nᴏ ꜰɪʟᴇs ʀᴇᴄᴇɪᴠᴇᴅ. Cᴀɴᴄᴇʟʟᴇᴅ.")
        
    final_text = f"<b>{title}</b>\n\n"
    
    if session["type"] == "movie":
        for i, item in enumerate(files, 1):
            final_text += f"{i}. {item}\n"
    else:
        # Sort files by episode number if available
        try:
            files.sort(key=lambda x: int(x["ep"]) if x["ep"] and x["ep"].isdigit() else 999)
        except:
            pass
            
        for i, item in enumerate(files, 1):
            ep_label = f"Episode {item['ep']}" if item['ep'] else f"File {i:02d}"
            final_text += f"{ep_label} : {item['link']}\n"
            
        msg_ids = session["msg_ids"]
        if msg_ids:
            first_msg = min(msg_ids)
            last_msg = max(msg_ids)
            batch_string = f"get-{first_msg * abs(client.db)}-{last_msg * abs(client.db)}"
            base64_batch = await encode(batch_string)
            batch_link = f"https://t.me/{client.username}?start={base64_batch}"
            final_text += f"\n🔗 <b>Batch Link:</b> {batch_link}"
            
    if len(final_text) > 4000:
        file_bytes = io.BytesIO(final_text.encode('utf-8'))
        file_bytes.name = f"{title}_links.txt"
        await message.reply_document(document=file_bytes, caption=f"**{title}** - Links generated.", quote=True)
    else:
        await message.reply(final_text, disable_web_page_preview=True)
