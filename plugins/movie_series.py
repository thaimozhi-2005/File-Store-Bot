import io
import re
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

def extract_episode(filename):
    """Extract episode number from filename supporting 20+ naming conventions."""
    if not filename:
        return None

    # Normalize separators
    name = filename.replace("_", " ").replace(".", " ")

    patterns = [
        # S01E07, S1E7, s01e07
        r"[Ss]\d+[Ee](\d+)",
        # Season 01 Episode 07
        r"[Ss]eason\s*\d+\s*[Ee]pisode\s*(\d+)",
        # Episode 07, Ep07, Ep 7, EP.07
        r"[Ee]pisode\s*(\d+)",
        r"\b[Ee][Pp]\.?\s*(\d+)\b",
        # - 07 - (standalone number with dashes/spaces on both sides, like "Title - 07 - Info")
        r"[-–]\s*(\d{1,3})\s*[-–]",
        # [ 07 ] or (07) standalone
        r"[\[\(]\s*(\d{1,3})\s*[\]\)]",
        # E07, e07
        r"\b[Ee](\d{2,3})\b",
        # x07 (common in some groups)
        r"\b[xX](\d{2,3})\b",
        # Trailing number before quality like "07 1080p", "07 720p", "07 480p"
        r"\b(\d{1,3})\s*(?:1080|720|480|2160)[pP]",
        # Pure number at the boundary of the title "Title 07 Info"
        r"(?:^|\s)(\d{2,3})(?:\s|$)",
    ]

    for pattern in patterns:
        match = re.search(pattern, name)
        if match:
            ep = match.group(1)
            # Sanity: episode numbers usually 1-999
            if 1 <= int(ep) <= 999:
                return ep.zfill(2)
    return None

# ─── Movie command ───────────────────────────────────────────
@Client.on_message(filters.private & filters.command("movie"))
async def start_movie(client: Client, message: Message):
    if message.from_user.id not in client.admins:
        return
    if len(message.command) < 2:
        return await message.reply(
            "<blockquote>✗ ᴇʀʀᴏʀ</blockquote>\n\nᴜsᴇ: <code>/movie {movie name}</code>", quote=True)
    title = message.text.split(" ", 1)[1]
    ACTIVE_SESSIONS[message.from_user.id] = {"type": "movie", "title": title, "files": [], "msg_ids": []}
    await message.reply(
        f"<blockquote>🍿 Mᴏᴠɪᴇ Sᴇᴛᴜᴘ Sᴛᴀʀᴛᴇᴅ!</blockquote>\n\n"
        f"<b>Title:</b> {title}\n\n"
        f"➤ Sᴇɴᴅ ᴏʀ ꜰᴏʀᴡᴀʀᴅ ᴀʟʟ ᴍᴏᴠɪᴇ ꜰɪʟᴇs ɴᴏᴡ (15+ ꜰɪʟᴇs ᴀᴛ ᴏɴᴄᴇ ᴡᴏʀᴋs ᴛᴏᴏ!)\n"
        f"➤ Wʜᴇɴ ᴅᴏɴᴇ, sᴇɴᴅ <code>/done</code>", quote=True)

# ─── Series command ──────────────────────────────────────────
@Client.on_message(filters.private & filters.command("series"))
async def start_series(client: Client, message: Message):
    if message.from_user.id not in client.admins:
        return
    if len(message.command) < 2:
        return await message.reply(
            "<blockquote>✗ ᴇʀʀᴏʀ</blockquote>\n\nᴜsᴇ: <code>/series {series name} {quality}</code>", quote=True)
    title = message.text.split(" ", 1)[1]
    ACTIVE_SESSIONS[message.from_user.id] = {"type": "series", "title": title, "files": [], "msg_ids": []}
    await message.reply(
        f"<blockquote>📺 Sᴇʀɪᴇs Sᴇᴛᴜᴘ Sᴛᴀʀᴛᴇᴅ!</blockquote>\n\n"
        f"<b>Title:</b> {title}\n\n"
        f"➤ Sᴇɴᴅ ᴏʀ ꜰᴏʀᴡᴀʀᴅ ᴀʟʟ ᴇᴘɪsᴏᴅᴇ ꜰɪʟᴇs (ʙᴜʟᴋ ꜰᴏʀᴡᴀʀᴅ ᴡᴏʀᴋs!)\n"
        f"➤ Eᴘɪsᴏᴅᴇ ɴᴜᴍʙᴇʀs ᴀʀᴇ ᴀᴜᴛᴏ-ᴅᴇᴛᴇᴄᴛᴇᴅ ꜰʀᴏᴍ ꜰɪʟᴇɴᴀᴍᴇ\n"
        f"➤ Wʜᴇɴ ᴅᴏɴᴇ, sᴇɴᴅ <code>/done</code>", quote=True)

from pyrogram import StopPropagation

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio), group=-1)
async def file_receiver(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in ACTIVE_SESSIONS:
        return
        
    raise StopPropagation
    
    file_size = 0
    file_name = "Unknown_File"
    if getattr(message, "document", None):
        file_size = message.document.file_size
        file_name = message.document.file_name or "Unknown_File"
    elif getattr(message, "video", None):
        file_size = message.video.file_size
        file_name = message.video.file_name or "Unknown_File"
    elif getattr(message, "audio", None):
        file_size = message.audio.file_size
        file_name = message.audio.file_name or "Unknown_File"

    try:
        post_message = await message.copy(chat_id=client.db, disable_notification=True)
    except Exception as e:
        await message.reply(f"❌ DB Error: {e}")
        return

    ACTIVE_SESSIONS[user_id]["msg_ids"].append(post_message.id)
    converted_id = post_message.id * abs(client.db)
    base64_string = await encode(f"get-{converted_id}")
    link = f"https://t.me/{client.username}?start={base64_string}"

    if ACTIVE_SESSIONS[user_id]["type"] == "movie":
        size_str = get_human_size(file_size)
        ACTIVE_SESSIONS[user_id]["files"].append({"size": size_str, "link": link})
        count = len(ACTIVE_SESSIONS[user_id]["files"])
        await message.reply(f"✅ Added file {count} ({size_str})", quote=True, disable_notification=True)
    else:
        ep_num = extract_episode(file_name)
        ACTIVE_SESSIONS[user_id]["files"].append({"name": file_name, "link": link, "ep": ep_num})
        count = len(ACTIVE_SESSIONS[user_id]["files"])
        ep_label = f"Ep {ep_num}" if ep_num else "Unknown"
        await message.reply(f"✅ Added {ep_label} (Total: {count})", quote=True, disable_notification=True)

# ─── Done command ─────────────────────────────────────────────
@Client.on_message(filters.private & filters.command("done"), group=-1)
async def done_command(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in ACTIVE_SESSIONS:
        return
        
    session = ACTIVE_SESSIONS.pop(user_id)
    raise StopPropagation
    files = session["files"]
    title = session["title"]

    if not files:
        return await message.reply("❌ No files received. Cancelled.")

    if session["type"] == "movie":
        lines = []
        for i, f in enumerate(files, 1):
            lines.append(f"  <code>{i}.</code> <b>{f['size']}</b> — <a href=\"{f['link']}\">Download</a>")
        final_text = (
            f"🎬 <b>{title}</b>\n"
            f"{'━' * 30}\n\n"
            + "\n".join(lines) +
            f"\n\n{'━' * 30}\n"
            f"📦 <b>Total Files:</b> {len(files)}"
        )
    else:
        # Sort by episode
        try:
            files.sort(key=lambda x: int(x["ep"]) if x.get("ep") and x["ep"].isdigit() else 9999)
        except Exception:
            pass

        lines = []
        for i, f in enumerate(files, 1):
            ep_label = f"Episode {f['ep']}" if f.get("ep") else f"File {i:02d}"
            lines.append(f"  <code>{ep_label}</code> — <a href=\"{f['link']}\">Watch</a>")

        batch_link = ""
        msg_ids = session["msg_ids"]
        if msg_ids:
            first_msg = min(msg_ids)
            last_msg = max(msg_ids)
            batch_string = f"get-{first_msg * abs(client.db)}-{last_msg * abs(client.db)}"
            base64_batch = await encode(batch_string)
            batch_link = f"https://t.me/{client.username}?start={base64_batch}"

        final_text = (
            f"📺 <b>{title}</b>\n"
            f"{'━' * 30}\n\n"
            + "\n".join(lines) +
            f"\n\n{'━' * 30}\n"
            f"📦 <b>Total Episodes:</b> {len(files)}\n"
            f"🔗 <b>Batch Link (All Episodes):</b> <a href=\"{batch_link}\">Click Here</a>"
        )

    if len(final_text) > 4000:
        plain = re.sub(r"<[^>]+>", "", final_text)
        file_bytes = io.BytesIO(plain.encode("utf-8"))
        file_bytes.name = f"{title}_links.txt"
        await message.reply_document(
            document=file_bytes,
            caption=f"<b>{title}</b> — {len(files)} files generated.",
            quote=True
        )
    else:
        await message.reply(final_text, disable_web_page_preview=True)
