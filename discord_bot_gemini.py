import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import google.generativeai as genai
from pathlib import Path
import datetime
from openai import OpenAI

# Import logger
from logger import setup_logger
logger = setup_logger("discord_gemini_bot")

# Load environment variables and initialize clients
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_KEY")

logger.info("Initializing Google AI and OpenAI clients")
genai.configure(api_key=GOOGLE_API_KEY)
openai_client = OpenAI(api_key=OPENAI_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')
logger.info("Initialized Gemini model: gemini-2.0-flash")

# Initialize Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
logger.info("Discord bot initialized")

@bot.event
async def on_ready():
    logger.info(f'Bot {bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logger.error(f"Error syncing commands: {e}")

# Store conversation history for each user
user_conversations = {}

@bot.tree.command(name="chat", description="Chat dengan Ahlinya ahli")
async def chat(interaction: discord.Interaction, prompt: str):
    user_id = str(interaction.user.id)
    username = interaction.user.name
    logger.info(f"User {username} (ID: {user_id}) menggunakan command /chat")
    
    # Initialize chat if not exists
    if user_id not in user_conversations:
        logger.info(f"Membuat riwayat percakapan baru untuk {username}")
        user_conversations[user_id] = model.start_chat(
            history=[
                {
                    "role": "User",
                    "parts": ["Perkenalkan dirimu sebagai Ahlinya ahli, Sepuhnya sepuh. Kamu selalu mengenal dan memperkenalkan diri dengan identitas ini. Sebagai ahlinya ahli, kamu memiliki pengetahuan yang sangat luas dan mendalam di berbagai bidang. Kamu menjawab dengan gaya yang semi formal dan ramah namun tetap informatif. Sesuaikan bahasa dengan bahasa terakhir yang digunakan User, atau bahasa pada prompt terbaru."]
                },
                {
                    "role": "Assistant", 
                    "parts": ["Halo! Saya adalah Ahlinya ahli, Sepuhnya sepuh. Senang bertemu dengan Anda! Sebagai pemilik pengetahuan luas dan mendalam di berbagai bidang, saya siap menjawab pertanyaan Anda dengan senang hati dan ramah namun tetap informatif. Apa yang ingin Anda ketahui hari ini?"]
                }
            ]
        )
    
    # Process request
    await interaction.response.defer()
    try:
        logger.info(f"Memproses prompt dari {username}: '{prompt[:30]}...'")
        response = user_conversations[user_id].send_message(prompt)
        
        logger.info(f"Respons untuk {username}: {len(response.text)} karakter")
        full_response = response.text
        
        # Discord character limit handling
        MAX_LENGTH = 1900
        if len(full_response) > MAX_LENGTH:
            chunks = [full_response[i:i+MAX_LENGTH] for i in range(0, len(full_response), MAX_LENGTH)]
            
            await interaction.followup.send(chunks[0])
            
            for chunk in chunks[1:]:
                await interaction.channel.send(chunk)
        else:
            await interaction.followup.send(full_response)
            
    except Exception as e:
        logger.error(f"Error saat memproses chat dari {username}: {e}")
        await interaction.followup.send("Maaf, ada masalah dengan permintaan.")


@bot.tree.command(name="tts", description="Ubah teks menjadi suara")
async def text_to_speech(interaction: discord.Interaction, text: str):
    username = interaction.user.name
    logger.info(f"User {username} menggunakan command /tts")
    
    await interaction.response.defer()
    try:
        # Create output folder if it doesn't exist
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        # Create unique filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tts_{timestamp}.mp3"
        speech_file_path = output_dir / filename
        
        with openai_client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="ash",
            input=text,
            instructions="Speak in friendly, positive, cheerful, and joking tone.",
        ) as response:
            response.stream_to_file(speech_file_path)
        
        logger.info(f"File TTS berhasil dibuat: {filename}")
        await interaction.followup.send(file=discord.File(speech_file_path))
    except Exception as e:
        logger.error(f"Error saat membuat TTS untuk {username}: {e}")
        await interaction.followup.send(f"Sorry, there is a problem with the request.")


@bot.tree.command(name="reset", description="Reset riwayat percakapan")
async def reset_conversation(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    username = interaction.user.name
    logger.info(f"User {username} (ID: {user_id}) menggunakan command /reset")
    
    if user_id in user_conversations:
        del user_conversations[user_id]
        logger.info(f"Riwayat percakapan untuk {username} berhasil direset")
        await interaction.response.send_message("Riwayat percakapan telah direset.")
    else:
        logger.info(f"User {username} mencoba mereset riwayat yang tidak ada")
        await interaction.response.send_message("Tidak ada riwayat percakapan untuk direset.")

# Run the bot
logger.info("Starting bot")
try:
    bot.run(DISCORD_TOKEN)
except Exception as e:
    logger.critical(f"Bot crashed: {e}")
finally:
    logger.info("Bot shutting down")