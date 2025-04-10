# AI-Powered Discord Bot

A versatile Discord bot that leverages both OpenAI's GPT and Google's Gemini models to provide intelligent chat capabilities and text-to-speech functionality.

## 📋 Features

* **Intelligent AI Chat** - Talk with an AI assistant powered by either:
  * OpenAI GPT-4o-mini
  * Google Gemini 2.0 Flash
* **Text-to-Speech** - Convert text to natural-sounding speech
* **Conversation Memory** - Bot remembers previous interactions in a conversation
* **Multi-user Support** - Each user has their own conversation history
* **Comprehensive Logging** - Detailed logs for monitoring and debugging

## 🛠️ Setup and Installation

### Prerequisites
* Python 3.8+
* Discord Bot Token
* OpenAI API Key
* Google AI API Key (for Gemini version)

### Installation
1. Clone the repository
```
git clone https://github.com/yourusername/openai-discord-bot.git
cd openai-discord-bot
```

2. Install required dependencies
```
pip install discord.py python-dotenv openai google-generativeai
```

3. Create a .env file in the project root with your API keys
```
DISCORD_TOKEN=your_discord_bot_token
OPENAI_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_ai_api_key
```

4. Run one of the bot versions
```
# For OpenAI version
python discord_bot.py

# For Gemini version
python discord_bot_gemini.py
```

## 🤖 Usage

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/chat` | Chat with the AI assistant | `/chat Tell me about machine learning` |
| `/tts` | Convert text to speech | `/tts Hello, how are you today?` |
| `/reset` | Reset your conversation history (Gemini version only) | `/reset` |

## 🗂️ Project Structure

* `discord_bot.py` - Main bot implementation using OpenAI API
* `discord_bot_gemini.py` - Alternative implementation using Google Gemini API
* `logger.py` - Logging configuration
* `logs` - Directory containing log files
* `output` - Directory for TTS audio output files

## ⚙️ Configuration

### Bot Persona
The bot is configured to respond as "Ahlinya ahli, Sepuhnya sepuh" - an expert with extensive knowledge across various fields. This persona can be customized by modifying the system prompt in the respective bot files.

### Logging
The project uses a custom logger with:
* Console output for real-time monitoring
* Daily rotating log files
* Detailed information including user interactions and response metrics

## 🧰 Technologies Used

* Discord.py - Discord API wrapper
* OpenAI API - For GPT models and TTS
* Google Generative AI - For Gemini model
* Python-dotenv - Environment variable management

## 🔒 Privacy & Security

* User conversation data is stored in memory and not persisted between bot restarts
* API keys are stored in a local .env file that is excluded from version control

## 📜 License

[Specify your license here]

## 👥 Contributors

[Your name/organization]

For questions or support, please open an issue.