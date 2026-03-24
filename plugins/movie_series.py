import io
from pyrogram import Client, filters
from pyrogram.types import Message
from helper.helper_func import encode

def add_asker(client, user_id):
    if not hasattr(client, "active_askers"):
        client.active_askers = set()
    client.active_askers.add(user_id)

def remove_asker(client, user_id):
    if hasattr(client, "active_askers") and user_id in client.active_askers:
        client.active_askers.remove(user_id)

def get_human_size(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"

@Client.on_message(filters.private & filters.command("movie"))
async def movie_maker(client: Client, message: Message):
    if message.from_user.id not in client.admins:
        return await message.reply(client.reply_text)
    
    if len(message.command) < 2:
        return await message.reply("<blockquote>✗ ᴇʀʀᴏʀ</blockquote>\n\nᴜsᴇ: `/movie {movie name}`", quote=True)
    
    title = message.text.split(" ", 1)[1]
    
    await message.reply(f"<blockquote>🍿 Mᴏᴠɪᴇ Sᴇᴛᴜᴘ: {title}</blockquote>\n\nSᴇɴᴅ ᴛʜᴇ ᴍᴏᴠɪᴇ ꜰɪʟᴇs ᴏɴᴇ ʙʏ ᴏɴᴇ (480ᴘ, 720ᴘ, 1080ᴘ).\nWʜᴇɴ ʏᴏᴜ ᴀʀᴇ ᴅᴏɴᴇ, sᴇɴᴅ `/done` ᴛᴏ ɢᴇᴛ ᴛʜᴇ ꜰɪɴᴀʟ ʟɪsᴛ.", quote=True)
    
    links = []
    
    add_asker(client, message.from_user.id)
    try:
        while True:
            try:
                msg = await client.ask(
                    text="⏳ Wᴀɪᴛɪɴɢ ꜰᴏʀ ᴍᴏᴠɪᴇ ꜰɪʟᴇs ᴏʀ `/done`...",
                    chat_id=message.from_user.id,
                    filters=(filters.incoming & ~filters.edited),
                    timeout=300
                )
            except Exception as e:
                await message.reply("⏳ Tɪᴍᴇᴏᴜᴛ ʀᴇᴀᴄʜᴇᴅ. Pʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ.")
                return
                
            if msg.text and msg.text.startswith("/done"):
                break
                
            if not msg.media:
                await msg.reply("❌ Pʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ꜰɪʟᴇ (Dᴏᴄᴜᴍᴇɴᴛ/Vɪᴅᴇᴏ) ᴏʀ sᴇɴᴅ `/done`")
                continue
                
            file_size = 0
            if getattr(msg, "document", None): file_size = msg.document.file_size
            elif getattr(msg, "video", None): file_size = msg.video.file_size
            elif getattr(msg, "audio", None): file_size = msg.audio.file_size
            
            size_str = get_human_size(file_size) if file_size else "Uɴᴋɴᴏᴡɴ Sɪᴢᴇ"
            
            # Forward to DB channel
            post_message = await msg.copy(chat_id=client.db, disable_notification=True)
            converted_id = post_message.id * abs(client.db)
            base64_string = await encode(f"get-{converted_id}")
            link = f"https://t.me/{client.username}?start={base64_string}"
            
            links.append(f"{size_str} : {link}")
            await msg.reply(f"✅ Fɪʟᴇ Rᴇᴄᴇɪᴠᴇᴅ! Tᴏᴛᴀʟ ꜰɪʟᴇs: {len(links)}")
    finally:
        remove_asker(client, message.from_user.id)
        
    if not links:
        return await message.reply("❌ Nᴏ ꜰɪʟᴇs ʀᴇᴄᴇɪᴠᴇᴅ. Cᴀɴᴄᴇʟʟᴇᴅ.", quote=True)
        
    final_text = f"<b>{title}</b>\n\n"
    final_text += "\n".join(links)
    
    await message.reply(final_text, disable_web_page_preview=True)

@Client.on_message(filters.private & filters.command("series"))
async def series_maker(client: Client, message: Message):
    if message.from_user.id not in client.admins:
        return await message.reply(client.reply_text)
    
    if len(message.command) < 2:
        return await message.reply("<blockquote>✗ ᴇʀʀᴏʀ</blockquote>\n\nᴜsᴇ: `/series {series name and quality}`\nE.g.: `/series Attack on Titan 1080p`", quote=True)
    
    title = message.text.split(" ", 1)[1]
    
    await message.reply(f"<blockquote>📺 Sᴇʀɪᴇs Sᴇᴛᴜᴘ: {title}</blockquote>\n\nSᴇɴᴅ ᴇᴘɪsᴏᴅᴇs ᴏɴᴇ ʙʏ ᴏɴᴇ ɪɴ ᴄᴏʀʀᴇᴄᴛ ᴏʀᴅᴇʀ (Eᴘ 1, Eᴘ 2...).\nWʜᴇɴ ʏᴏᴜ ᴀʀᴇ ᴅᴏɴᴇ, sᴇɴᴅ `/done` ᴛᴏ ɢᴇᴛ ᴛʜᴇ ꜰɪɴᴀʟ ʟɪsᴛ ᴡɪᴛʜ Bᴀᴛᴄʜ Lɪɴᴋ.", quote=True)
    
    links = []
    first_msg_id = None
    last_msg_id = None
    
    add_asker(client, message.from_user.id)
    try:
        while True:
            try:
                msg = await client.ask(
                    text="⏳ Wᴀɪᴛɪɴɢ ꜰᴏʀ ᴇᴘɪsᴏᴅᴇs ᴏʀ `/done`...",
                    chat_id=message.from_user.id,
                    filters=(filters.incoming & ~filters.edited),
                    timeout=300
                )
            except Exception as e:
                await message.reply("⏳ Tɪᴍᴇᴏᴜᴛ ʀᴇᴀᴄʜᴇᴅ. Pʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ.")
                return
                
            if msg.text and msg.text.startswith("/done"):
                break
                
            if not msg.media:
                await msg.reply("❌ Pʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ꜰɪʟᴇ (Dᴏᴄᴜᴍᴇɴᴛ/Vɪᴅᴇᴏ) ᴏʀ sᴇɴᴅ `/done`")
                continue
                
            # Forward to DB channel
            post_message = await msg.copy(chat_id=client.db, disable_notification=True)
            
            if first_msg_id is None:
                first_msg_id = post_message.id
            last_msg_id = post_message.id
            
            converted_id = post_message.id * abs(client.db)
            base64_string = await encode(f"get-{converted_id}")
            link = f"https://t.me/{client.username}?start={base64_string}"
            
            ep_num = len(links) + 1
            links.append(f"Episode {ep_num:02d} : {link}")
            await msg.reply(f"✅ Aᴅᴅᴇᴅ Eᴘɪsᴏᴅᴇ {ep_num}!")
    finally:
        remove_asker(client, message.from_user.id)
        
    if not links:
        return await message.reply("❌ Nᴏ ᴇᴘɪsᴏᴅᴇs ʀᴇᴄᴇɪᴠᴇᴅ. Cᴀɴᴄᴇʟʟᴇᴅ.", quote=True)
        
    batch_link = ""
    if first_msg_id and last_msg_id:
        batch_string = f"get-{first_msg_id * abs(client.db)}-{last_msg_id * abs(client.db)}"
        base64_batch = await encode(batch_string)
        batch_link = f"https://t.me/{client.username}?start={base64_batch}"
        
    final_text = f"<b>{title}</b>\n\n"
    final_text += "\n".join(links)
    final_text += f"\n\n<b>Batch Link:</b> {batch_link}"
    
    await message.reply(final_text, disable_web_page_preview=True)
