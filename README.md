# Real-Time Scam Monitoring and Prevention System

This project monitors and analyzes phone conversations for signs of suspicious or scam activity using OpenAI GPT-4 and speech recognition. The system captures conversations via a microphone, transcribes the audio, and uses AI to determine if the conversation contains any scam indicators. It provides insights such as the names of individuals, companies mentioned, and suggests next steps for the user if the conversation is deemed suspicious.

## Table of Contents
1. [Features](#features)
2. [Setup Instructions](#setup-instructions)
3. [How It Works](#how-it-works)
4. [Project Structure](#project-structure)
5. [Usage](#usage)
6. [Contributing](#contributing)

## Features
- **Real-time Monitoring**: The system listens for conversations and performs analysis in real-time.
- **GPT-4 Analysis**: Conversations are analyzed to detect suspicious patterns, extract names, and identify companies.
- **Multi-threading**: Tasks like analyzing conversations, detecting suspicious activity, and suggesting next steps are processed in parallel.
- **Speech Recognition**: Uses Google Speech Recognition to transcribe audio.
- **Safety Suggestions**: Offers advice on how to handle potentially scam conversations.

## Setup Instructions
### Prerequisites
1. **Python 3.x**: Ensure that you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).I used Python 3.12.
2. **OpenAI API Key**: Obtain an OpenAI API key from [OpenAI's website](https://beta.openai.com/signup/).
3. **Python Libraries**: The following Python libraries are required:
   - `openai`
   - `speech_recognition`
   - `concurrent.futures`
   - `warnings`
   
   You can install the dependencies using the following command:
   ```bash
   pip install openai SpeechRecognition
   ```

## How It Works
1. Listening: The system uses a microphone to listen to real-time audio input.
2. Transcription: Audio is converted into text using Google's Speech Recognition.
3. Analysis: The transcribed text is processed by OpenAI's GPT-4 to:
4. Analyze Conversation: Provides a general analysis of the conversation.
   Detect Suspicion: Flags the conversation if it seems suspicious.
   Extract Names and Companies: Extract the names of individuals and companies mentioned in the conversation.
   Suggest Next Steps: Offers advice on how to handle potential scam situations.

## Project Structure
```bash
├── Scam_patterns.py     # Main script that performs real-time monitoring and analysis
├── README.md            # Documentation file
```

## Reference 
Use ``` scam_project_doc.odt ``` file to understand some other things like virtual environment creation etc which I used while building.
