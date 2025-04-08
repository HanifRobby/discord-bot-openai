import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

# Setup OpenAI client
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

@bot.tree.command(name="chat", description="Chat dengan AI assistant")
async def chat(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Anda adalah asisten yang membalas dalam bahasa Indonesia yang formal dan sopan."},
                {"role": "user", "content": prompt}
            ]
        )
        response = completion.choices[0].message.content
        await interaction.followup.send(response)
    except Exception as e:
        await interaction.followup.send(f"Error: {str(e)}")

@bot.tree.command(name="tts", description="Ubah teks menjadi suara")
async def text_to_speech(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    try:
        speech_file_path = Path(__file__).parent / "speech.mp3"
        
        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="ash",
            input=text,
            instructions="Speak in a cheerful and positive tone.",
        ) as response:
            response.stream_to_file(speech_file_path)
        
        await interaction.followup.send(file=discord.File(speech_file_path))
    except Exception as e:
        await interaction.followup.send(f"Error: {str(e)}")

# Run the bot
bot.run(DISCORD_TOKEN)