# Gemini AI Setup Guide

## Quick Setup

1. **Get Your Gemini API Key**
   - Visit: https://makersuite.google.com/app/apikey
   - Click "Create API Key"
   - Copy your API key

2. **Set the Environment Variable**

   **Option A: Temporary (for testing)**
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   cd /home/pi/Documents/Embedded/act7
   ./run.sh
   ```

   **Option B: Permanent**
   ```bash
   # Add to your ~/.bashrc file
   echo 'export GEMINI_API_KEY="your_api_key_here"' >> ~/.bashrc
   source ~/.bashrc
   ```

   **Option C: Create .env file** (Recommended)
   ```bash
   cd /home/pi/Documents/Embedded/act7
   cp .env.example .env
   nano .env
   # Add your key: GEMINI_API_KEY=your_actual_key_here
   ```

3. **Install Required Package**
   ```bash
   cd /home/pi/Documents/Embedded/act7
   source .venv/bin/activate
   pip install google-generativeai
   ```

4. **Run the Application**
   ```bash
   cd /home/pi/Documents/Embedded/act7
   GEMINI_API_KEY="your_key" ./run.sh
   ```

## Features

### AI-Powered Voice Commands
- **Natural Language**: Speak naturally, no need to memorize exact phrases
- **Bilingual Support**: Works in English and Filipino/Tagalog
- **Smart Understanding**: AI interprets your intent even with variations

### Example Commands

**English:**
- "Turn on the white light"
- "Can you blink the blue LED?"
- "Switch off all the lights"
- "Make the red one flash"
- "Activate the buzzer"

**Filipino:**
- "Buksan ang puting ilaw"
- "Paki-blink yung asul"
- "Patayin lahat"
- "I-on mo yung pula"

### Fallback Mode
If no API key is set, the system automatically falls back to the original hardcoded command patterns.

## Troubleshooting

**Error: "WARNING: GEMINI_API_KEY not set"**
- Solution: Set the environment variable as shown above

**Commands not working:**
- Check if API key is valid
- Verify internet connection
- Check console for error messages

**Slow response:**
- Normal for first request (API initialization)
- Subsequent requests are faster

## Cost & Limits

- Gemini API has a free tier with generous limits
- Check current pricing: https://ai.google.dev/pricing
- Free tier typically includes 60 requests per minute

## Security Note

⚠️ **Never commit your API key to git!**
- Keep `.env` file in `.gitignore`
- Use environment variables for production
