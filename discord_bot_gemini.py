import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import google.generativeai as genai
from pathlib import Path
import datetime
from openai import OpenAI

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_KEY")

# Setup Google AI
genai.configure(api_key=GOOGLE_API_KEY)
openai_client = OpenAI(api_key=OPENAI_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

# Initialize Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# Menyimpan riwayat percakapan untuk setiap pengguna
user_conversations = {}

@bot.tree.command(name="chat", description="Chat dengan Ahlinya ahli")
async def chat(interaction: discord.Interaction, prompt: str):
    user_id = str(interaction.user.id)
    
    # Inisialisasi chat jika belum ada
    if user_id not in user_conversations:
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
    
    # Kirim pesan dan dapatkan respons
    await interaction.response.defer()
    try:
        response = user_conversations[user_id].send_message(prompt)
        
        # Pecah respons panjang menjadi beberapa bagian
        full_response = response.text
        
        # Batas karakter Discord
        MAX_LENGTH = 1900  # Sedikit di bawah 2000 untuk amannya
        
        # Jika respons melebihi batas
        if len(full_response) > MAX_LENGTH:
            # Pisahkan respons menjadi beberapa bagian
            chunks = [full_response[i:i+MAX_LENGTH] for i in range(0, len(full_response), MAX_LENGTH)]
            
            # Kirim bagian pertama
            await interaction.followup.send(chunks[0])
            
            # Kirim bagian lainnya
            for chunk in chunks[1:]:
                await interaction.channel.send(chunk)
        else:
            await interaction.followup.send(full_response)
            
    except Exception as e:
        await interaction.followup.send("Maaf, ada masalah dengan permintaan.")
        print(f"Error: {str(e)}")

@bot.tree.command(name="tts", description="Ubah teks menjadi suara")
async def text_to_speech(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    try:
        # Buat folder output jika belum ada
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        # Buat nama file unik berdasarkan timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tts_{timestamp}.mp3"
        
        # Path lengkap file output
        speech_file_path = output_dir / filename
        
        with openai_client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="ash",
            input=text,
            instructions="Speak in friendly, positive, cheerful, and joking tone.",
        ) as response:
            response.stream_to_file(speech_file_path)
        
        await interaction.followup.send(file=discord.File(speech_file_path))
    except Exception as e:
        await interaction.followup.send(f"Sorry, there is a problem with the request.")
        print(f"Error: {str(e)}")

@bot.tree.command(name="reset", description="Reset riwayat percakapan")
async def reset_conversation(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    if user_id in user_conversations:
        del user_conversations[user_id]
        await interaction.response.send_message("Riwayat percakapan telah direset.")
    else:
        await interaction.response.send_message("Tidak ada riwayat percakapan untuk direset.")

# Run the bot
bot.run(DISCORD_TOKEN)