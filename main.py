import os
import asyncio
import subprocess
from pyrogram import Client, filters

# ================== CONFIG ==================
API_ID =   
API_HASH = ""
BOT_TOKEN = ""

# Unique safe folder
DOWNLOADS = "/root/leechbot_files"
# ============================================

os.makedirs(DOWNLOADS, exist_ok=True)

app = Client("leechbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# Run command and capture output
async def run_command(cmd):
    process = await asyncio.create_subprocess_exec(
        *cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return stdout.decode().strip(), stderr.decode().strip()


@app.on_message(filters.private & filters.text)
async def leech_file(client, message):
    url = message.text.strip()
    status = await message.reply("🔎 Extracting link...")

    # Get title for filename
    title_out, _ = await run_command(["yt-dlp", "--get-title", url])
    if not title_out:
        return await status.edit("❌ Could not extract title")

    title = "".join(c if c.isalnum() or c in "._-" else "_" for c in title_out)[:60]
    filepath = os.path.join(DOWNLOADS, f"{title}.mp4")

    await status.edit("⬇️ Downloading file...")

    # Download file with yt-dlp
    _, err = await run_command(["yt-dlp", "-o", filepath, url])
    if not os.path.exists(filepath):
        return await status.edit(f"❌ Download failed\n{err}")

    await status.edit("📤 Uploading to Telegram...")

    try:
        await client.send_video(
            chat_id=message.chat.id,
            video=filepath,
            caption=f"✅ Here is your file:\n`{title}`",
            supports_streaming=True
        )
    except Exception as e:
        await message.reply(f"❌ Upload failed: {e}")

    # Clean up file
    if os.path.exists(filepath):
        os.remove(filepath)
    await status.delete()


print("✅ Bot is running...")
app.run()
