import os
from pyrogram import Client, filters
from pyrogram.types import Message, ForceReply

# ==============================
# CONFIG
# ==============================
API_ID = int(os.getenv("API_ID", ""))   
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# ==============================
# START BOT
# ==============================
app = Client(
    "LinkNamingBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Temporary storage for links
user_links = {}


@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    await message.reply_text(
        "👋 Hello! Send me a link and I will ask you to provide a custom name for it.\n\n"
        "Example:\n`https://example.com/video.mp4` → `Name S01E01 480p Hindi`",
        quote=True
    )


@app.on_message(filters.private & filters.text & ~filters.reply)
async def link_receiver(client: Client, message: Message):
    text = message.text.strip()

    # Very simple check if it's a link
    if text.startswith("http://") or text.startswith("https://"):
        user_links[message.from_user.id] = text
        await message.reply_text(
            "🔗 Got your link!\n\nNow please reply with the **name you want** for this link:",
            reply_markup=ForceReply(selective=True)
        )
    else:
        await message.reply_text("❌ Please send a valid link starting with http:// or https://")


@app.on_message(filters.private & filters.reply)
async def name_receiver(client: Client, message: Message):
    user_id = message.from_user.id

    if user_id not in user_links:
        await message.reply_text("⚠️ Please send me a link first.")
        return

    link = user_links.pop(user_id)
    name = message.text.strip()

    formatted = f"[{name}] {link}"
    await message.reply_text(
        f"✅ Saved:\n\n{formatted}",
        quote=True
    )


# ==============================
# RUN BOT
# ==============================
print("🤖 Bot Started...")
app.run()
