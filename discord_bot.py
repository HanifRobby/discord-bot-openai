import os
import discord
import datetime
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

# Load environment variables and initialize clients
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")
client = OpenAI(api_key=OPENAI_KEY)

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

# Store conversation history for each user
user_conversations = {}

@bot.tree.command(name="chat", description="Chat dengan Ahlinya ahli")
async def chat(interaction: discord.Interaction, prompt: str):
    user_id = str(interaction.user.id)
    
    # Initialize history if not exists
    if user_id not in user_conversations:
        user_conversations[user_id] = [
            {"role": "system", "content": "Anda adalah Ahlinya ahli, Sepuhnya sepuh. Anda selalu mengenal dan memperkenalkan diri dengan identitas ini. Sebagai ahlinya ahli, Anda memiliki pengetahuan yang sangat luas dan mendalam di berbagai bidang. Anda menjawab dengan gaya yang santai dan ramah namun tetap informatif. Balas dalam bahasa yang digunakan pengguna."}
        ]
    
    # Add user message to history
    user_conversations[user_id].append({"role": "user", "content": prompt})
    
    # Limit history (to avoid excessive token usage)
    if len(user_conversations[user_id]) > 10:
        user_conversations[user_id] = [user_conversations[user_id][0]] + user_conversations[user_id][-9:]
    
    # Process with complete conversation context
    await interaction.response.defer()
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=user_conversations[user_id]
        )
        response = completion.choices[0].message.content
        
        # Add assistant response to history
        user_conversations[user_id].append({"role": "assistant", "content": response})
        
        await interaction.followup.send(response)
    except Exception as e:
        await interaction.followup.send(f"Sorry, there is a problem with the request.")
        print(f"Error: {str(e)}")

@bot.tree.command(name="tts", description="Ubah teks menjadi suara")
async def text_to_speech(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    try:
        # Create output folder if it doesn't exist
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        # Create unique filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tts_{timestamp}.mp3"
        speech_file_path = output_dir / filename
        
        with client.audio.speech.with_streaming_response.create(
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

# Run the bot
bot.run(DISCORD_TOKEN)