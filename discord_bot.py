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

@bot.command(name='chat')
async def chat(ctx, *, prompt):
    """Generate a response using OpenAI"""
    async with ctx.typing():
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Anda adalah asisten yang membalas dengan bahasa sesuai pesan pengguna."},
                    {"role": "user", "content": prompt}
                    ]
            )
            response = completion.choices[0].message.content
            await ctx.send(response)
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

@bot.command(name='tts')
async def text_to_speech(ctx, *, text):
    """Convert text to speech using OpenAI TTS"""
    async with ctx.typing():
        try:
            # Generate speech file
            speech_file_path = Path(__file__).parent / "speech.mp3"
            
            with client.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts",
                voice="ash",
                input=text,
                instructions="Speak in a cheerful and positive tone.",
            ) as response:
                response.stream_to_file(speech_file_path)
            
            # Send audio file to Discord
            await ctx.send(file=discord.File(speech_file_path))
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

# Run the bot
bot.run(DISCORD_TOKEN)