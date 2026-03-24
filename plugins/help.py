from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.private & (filters.command("cc") | filters.command("adminhelp")))
async def admin_help(client: Client, message: Message):
    if message.from_user.id not in client.admins:
        return
        
    help_text = """
🛠 **Aᴅᴍɪɴ Hᴇʟᴘ Mᴇɴᴜ 🛠**

/users - Get total users count
/settings - Open Bot Settings Panel
/stats - See bot statistics 
/broadcast - Broadcast a message to all users. (Reply this to any message/photo)
/pbroadcast - Broadcast message and pin it in users chat
/batch - Generate Batch Link (Asking First and Last Message from DB Channel)
/nbatch {count} - Generate Batch Link continuously from a start link
/genlink - Generate single file link
/bulk - Generate Links for Multiple Files with direct links along with one batch link
/movie {Name} - Start movie setup to fetch continuous files with file sizes & indexing
/series {Name} - Start series setup to fetch continuous episodes with original filename & batch link
/ban {user_id} - Ban a user
/unban {user_id} - Unban a user
/addpremium {user_id} {time} - Give Premium to User
/delpremium {user_id} - Remove Premium
/premiumusers - List of Premium Users
/db, /adddb, /removedb - Multi-Database management
"""
    await message.reply(help_text)
