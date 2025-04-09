import os
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Client(
    "RiseMusicBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# Start Command with Stylish Animation
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    welcome_text = """
✨ *Welcome to RiseTunez Music Bot!* ✨

🎵 Play high-quality music in your groups
🎮 Enjoy multiplayer games with friends
🛡️ Advanced group protection features
🔞 Private adult chat (in private only)

Use buttons below to explore features!
"""
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎵 Music Commands", callback_data="music_help")],
        [InlineKeyboardButton("🎮 Games", callback_data="games")],
        [InlineKeyboardButton("🛡️ Admin Tools", callback_data="admin_tools")],
        [InlineKeyboardButton("🔞 Adult Chat", callback_data="adult_chat")],
        [InlineKeyboardButton("📢 Join Channel", url=Config.MUST_JOIN_GROUP)],
        [InlineKeyboardButton("💬 Support", url=Config.SUPPORT_GROUP)]
    ])
    
    # Send with animation
    await message.reply_animation(
        animation="https://telegra.ph/file/5e6c160a40a6c8a0d1a2a.mp4",
        caption=welcome_text,
        reply_markup=buttons
    )

# Music Player Commands
@app.on_message(filters.command("play") & filters.group)
async def play_music(client, message):
    # Music playback logic here
    await message.reply("🎵 Playing your requested song!")

# Link Protection
@app.on_message(filters.group & filters.text & filters.regex(r'https?://[^\s]+'))
async def link_protection(client, message):
    if message.from_user.id in Config.SUDO_USERS:
        return
    
    await client.restrict_chat_member(
        message.chat.id,
        message.from_user.id,
        ChatPermissions(),
        int(time.time() + 3600)  # Mute for 1 hour
    await message.reply(f"⚠️ {message.from_user.mention} was muted for sending links!")

# Random Member Tagging
@app.on_message(filters.command("tagall") & filters.group)
async def tag_all(client, message):
    members = []
    async for member in client.get_chat_members(message.chat.id):
        members.append(member.user.mention)
    
    random.shuffle(members)
    tagged = " ".join(members[:10])  # Tag 10 random members
    await message.reply(f"👥 Random members: {tagged}")

# Games Section
@app.on_message(filters.command("game") & filters.group)
async def games_menu(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎯 Sticker Duel", callback_data="sticker_duel")],
        [InlineKeyboardButton("🎲 Dice Game", callback_data="dice_game")],
        [InlineKeyboardButton("🧩 Trivia Quiz", callback_data="trivia_quiz")]
    ])
    await message.reply("🎮 Choose a game to play:", reply_markup=buttons)

# Content Downloader
@app.on_message(filters.command("download"))
async def download_content(client, message):
    # Implement download logic for YouTube, Pinterest, etc.
    await message.reply("⬇️ Downloading your content...")

# Adult Chat (Private Only)
@app.on_message(filters.private & filters.command("sexting"))
async def adult_chat(client, message):
    await message.reply("🔞 This feature is only available in private chat.")

# Help Command
@app.on_message(filters.command("help"))
async def help_command(client, message):
    help_text = """
🛠 *RiseTunez Bot Help* 🛠

*Music Commands:*
/play [song] - Play a song
/queue - Show current queue
/skip - Skip current song

*Group Tools:*
/tagall - Tag random members
/game - Play games
/rules - Show group rules

*Admin Commands:*
/mute [user] - Mute a user
/ban [user] - Ban a user
/warn [user] - Warn a user

Use buttons for more options!
"""
    await message.reply(help_text)

# Callback Query Handler
@app.on_callback_query()
async def callback_handler(client, query):
    if query.data == "music_help":
        await query.message.edit_text("🎵 *Music Help*\n\nUse /play to play music\n/queue to see queue\n/skip to skip song")
    elif query.data == "games":
        await query.message.edit_text("🎮 *Games Menu*\n\nAvailable games:\n- Sticker Duel\n- Dice Game\n- Trivia Quiz")
    elif query.data == "admin_tools":
        await query.message.edit_text("🛡️ *Admin Tools*\n\nAvailable tools:\n- Link protection\n- Auto-mute\n- Warning system")

if __name__ == "__main__":
    logger.info("Starting RiseTunez Music Bot...")
    app.run()
