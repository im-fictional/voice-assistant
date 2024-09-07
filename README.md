Here’s a sample `README.md` file for your voice assistant project:

---

# Stella Voice Assistant

Stella is a voice-controlled assistant built using Python. The assistant can recognize voice commands to perform various tasks such as web searches, opening programs, adjusting system volume, creating files or folders, and controlling system functions like shutdown, restart, and sleep mode.

## Features

- **Speech Recognition**: Listens to user commands and processes them in Ukrainian.
- **Voice Responses**: Uses Google Text-to-Speech (gTTS) for voice output.
- **Web Integration**: Opens websites and performs Google searches.
- **Program Control**: Launches programs via system search.
- **File Management**: Creates text documents and folders on the desktop.
- **System Control**: Adjusts volume, shuts down, restarts, or puts the system to sleep.
  
## Requirements

Before running the project, ensure you have the following dependencies installed:

```bash
pip install eel requests beautifulsoup4 pygame gtts pyautogui pyperclip pyaudio pycaw SpeechRecognition
```

## Usage

1. Clone the repository and navigate to the project directory.
   
   ```bash
   git clone https://github.com/im-fictional/voice-assistant.git
   cd voice-assistant
   ```

2. Run the assistant:

   ```bash
   python assistant.py
   ```

3. Use voice commands like:
   
   - **"Stella, відкрий YouTube"**: Opens YouTube in the browser.
   - **"Stella, який зараз час?"**: Tells the current time.
   - **"Stella, гучність на 50%"**: Adjusts the system volume to 50%.
   - **"Stella, створити папку"**: Creates a folder on the desktop.
   - **"Stella, виключи комп'ютер"**: Shuts down the computer.

## Project Structure

- **`assistant.py`**: Main script for handling commands and controlling the assistant.
- **`commands.py`**: Contains mappings for various commands in Ukrainian.
- **`web/`**: Contains the frontend for the assistant using Eel.

## Frontend

The project uses Eel to provide a simple web-based interface.

## Future Improvements

- Add more voice commands.
- Improve the speech recognition model.
- Add support for other languages.
