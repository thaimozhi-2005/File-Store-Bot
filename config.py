
import logging
from logging.handlers import RotatingFileHandler

# Configuration cleanup
import os

MSG_EFFECT = int(os.environ.get("MSG_EFFECT", "5046509860389126442"))
# Bot Configuration
SESSION = os.environ.get("SESSION", "FileStoreBot")
TOKEN = os.environ.get("TOKEN", "")
API_ID = int(os.environ.get("API_ID", 0)) if os.environ.get("API_ID") else 0
API_HASH = os.environ.get("API_HASH", "")
WORKERS = int(os.environ.get("WORKERS", 5))

# MongoDB
DB_URI = os.environ.get("DB_URI", "")
DB_NAME = os.environ.get("DB_NAME", "FileStoreBot")

# Channel config
# Force Sub Channels String format: "-100xxxx,True,10 -100yyyy,False,0"
FSUBS = [] # Hardcoding Force Subscription here or modifying if needed
# Better to pass list as env
DB_CHANNEL = int(os.environ.get("DB_CHANNEL", 0)) if os.environ.get("DB_CHANNEL") else 0
# Auto Delete Timer (seconds)
AUTO_DEL = int(os.environ.get("AUTO_DEL", 300))
# Admin IDs
OWNER_ID = int(os.environ.get("OWNER_ID", 0)) if os.environ.get("OWNER_ID") else 0
ADMINS = [int(admin) for admin in os.environ.get("ADMINS", str(OWNER_ID)).split(" ")] if os.environ.get("ADMINS", str(OWNER_ID)) else []

# Bot Settings
DISABLE_BTN = os.environ.get("DISABLE_BTN", "True").lower() == "true"
PROTECT = os.environ.get("PROTECT", "True").lower() == "true"

# Shortner config
SHORT_URL = os.environ.get("SHORT_URL", "linkshortify.com") 
SHORT_API = os.environ.get("SHORT_API", "") 
SHORT_TUT = os.environ.get("SHORT_TUT", "https://t.me/How_to_Download_7x/26")

PORT = int(os.environ.get("PORT", "5010"))
LOG_FILE_NAME = "bot.log"

# Messages Configuration
MESSAGES = {
    "START": "<b>›› ʜᴇʏ {first}! 👋\n<blockquote>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ @AnimePiratesTamil ꜰɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ!\nɪ'ᴍ ʜᴇʀᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ɢᴇᴛ ʏᴏᴜʀ ꜰɪʟᴇs ꜰᴀsᴛ & ᴇᴀsʏ 🚀</blockquote></b>",
    "FSUB": "<b><blockquote>›› ʜᴇʏ! ʏᴏᴜʀ ꜰɪʟᴇ ɪs ʀᴇᴀᴅʏ ✅</blockquote>\n\nʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ʏᴇᴛ.\nᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ ᴀɴᴅ ɢᴇᴛ ʏᴏᴜʀ ꜰɪʟᴇs! 🎬</b>",
    "ABOUT": "<b>›› ᴀʙᴏᴜᴛ ᴛʜɪs ʙᴏᴛ\n<blockquote expandable>›› ᴄʜᴀɴɴᴇʟ: <a href='https://t.me/AnimePiratesTamil'>@AnimePiratesTamil</a>\n›› ʟᴀɴɢᴜᴀɢᴇ: <a href='https://docs.python.org/3/'>Pʏᴛʜᴏɴ 3</a>\n›› ʟɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ ᴠ2</a>\n›› ᴅᴀᴛᴀʙᴀsᴇ: <a href='https://www.mongodb.com/docs/'>Mᴏɴɢᴏ ᴅʙ</a></blockquote></b>",
    "REPLY": "<b>›› ꜰᴏʀ ᴍᴏʀᴇ ᴄᴏɴᴛᴇɴᴛ ᴊᴏɪɴ - @AnimePiratesTamil</b>",
    "SHORT_MSG": "<b>📊 ʜᴇʏ {first},\n\n‼️ ɢᴇᴛ ᴀʟʟ ꜰɪʟᴇs ɪɴ ᴀ sɪɴɢʟᴇ ʟɪɴᴋ ‼️\n\n⌯ ʏᴏᴜʀ ʟɪɴᴋ ɪs ʀᴇᴀᴅʏ, ᴋɪɴᴅʟʏ ᴄʟɪᴄᴋ ᴏɴ ᴏᴘᴇɴ ʟɪɴᴋ ʙᴜᴛᴛᴏɴ..</b>",
    "START_PHOTO": "https://graph.org/file/510affa3d4b6c911c12e3.jpg",
    "FSUB_PHOTO": "https://telegra.ph/file/7a16ef7abae23bd238c82-b8fbdcb05422d71974.jpg",
    "SHORT_PIC": "https://telegra.ph/file/7a16ef7abae23bd238c82-b8fbdcb05422d71974.jpg",
    "SHORT": "https://telegra.ph/file/8aaf4df8c138c6685dcee-05d3b183d4978ec347.jpg"
}

def LOGGER(name: str, client_name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    formatter = logging.Formatter(
        f"[%(asctime)s - %(levelname)s] - {client_name} - %(name)s - %(message)s",
        datefmt='%d-%b-%y %H:%M:%S'
    )
    file_handler = RotatingFileHandler(LOG_FILE_NAME, maxBytes=50_000_000, backupCount=10)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
