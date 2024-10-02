import cohere
import speech_recognition as sr
import threading
import time
import os
import sys
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed

# Suppress warnings
warnings.filterwarnings("ignore")

# Redirect stderr to devnull to suppress ALSA errors .The system where it was first written is linux so used this command to supress ALSA errors. 
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')

# Function to initialize Cohere client
def init_cohere(api_key):
    return cohere.Client(api_key)

# Function to analyze the conversation
def analyze_conversation(client, conversation_text):
    try:
        response = client.generate(
            model="command-xlarge-nightly",
            prompt=f"You are an FBI agent who can understand the most likely patterns in financial scam calls. Sort out important data like the name of the person, the company they are associated with, and all other information that could help track or identify if the person is legit by running a background check.\n\nConversation:\n{conversation_text}",
            max_tokens=100
        )
        return response.generations[0].text
    except Exception as e:
        return f"Error analyzing conversation: {e}"

# Function to predict if the conversation is suspicious
def is_suspicious(client, conversation_text):
    try:
        response = client.generate(
            model="command-xlarge-nightly",
            prompt=f"You are an expert in identifying suspicious patterns in phone calls. Analyze the following conversation and determine if it seems suspicious. If suspicious, just give the single word 'suspicious'.\n\nConversation:\n{conversation_text}",
            max_tokens=20
        )
        return "suspicious" in response.generations[0].text.lower()
    except Exception as e:
        print(f"Error in is_suspicious: {e}")
        return False

# Function to suggest next steps if suspicious
def suggest_next_steps(client, conversation_text):
    try:
        response = client.generate(
            model="command-xlarge-nightly",
            prompt=f"Suggest safe actions to take in a potential scam situation based on the following conversation.\n\nConversation:\n{conversation_text}",
            max_tokens=100
        )
        return response.generations[0].text
    except Exception as e:
        return f"Unable to suggest next steps: {e}"

# New function to extract names from the conversation
def extract_names(client, conversation_text):
    try:
        response = client.generate(
            model="command-xlarge-nightly",
            prompt=f"Extract and list all names mentioned in the following conversation.\n\nConversation:\n{conversation_text}",
            max_tokens=50
        )
        return response.generations[0].text
    except Exception as e:
        return f"Error extracting names: {e}"

# New function to identify companies mentioned in the conversation
def identify_companies(client, conversation_text):
    try:
        response = client.generate(
            model="command-xlarge-nightly",
            prompt=f"Identify and list all companies or organizations mentioned in the following conversation.\n\nConversation:\n{conversation_text}",
            max_tokens=50
        )
        return response.generations[0].text
    except Exception as e:
        return f"Error identifying companies: {e}"

# Function to run all analysis functions in parallel
def run_parallel_analysis(client, conversation_text):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(analyze_conversation, client, conversation_text): "General Analysis",
            executor.submit(is_suspicious, client, conversation_text): "Suspicion Check",
            executor.submit(suggest_next_steps, client, conversation_text): "Suggested Next Steps",
            executor.submit(extract_names, client, conversation_text): "Extracted Names",
            executor.submit(identify_companies, client, conversation_text): "Identified Companies"
        }
        
        results = {}
        for future in as_completed(futures):
            results[futures[future]] = future.result()
    
    return results

# Function to handle speech recognition and analysis in a separate thread
def analyze_clip_thread(client, conversation_text):
    print(f"\nRecognized Text: {conversation_text}")
    
    results = run_parallel_analysis(client, conversation_text)
    
    if results["Suspicion Check"]:
        print("ALERT: Suspicious activity detected!")
        print("Analysis:", results["General Analysis"])
        print("Extracted Names:", results["Extracted Names"])
        print("Identified Companies:", results["Identified Companies"])
        print("Suggested Actions:", results["Suggested Next Steps"])
    else:
        print("Conversation appears safe.")
        print("Extracted Names:", results["Extracted Names"])
        print("Identified Companies:", results["Identified Companies"])

# Function to handle speech recognition and analysis
def listen_and_analyze_clip(client, recognizer, microphone):
    with microphone as source:
        print("\nListening ")
        try:
            audio = recognizer.listen(source, timeout=15)
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period.")
            return

    try:
        conversation_text = recognizer.recognize_google(audio)
        threading.Thread(target=analyze_clip_thread, args=(client, conversation_text)).start()
    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from the service; {e}")

# Function to start real-time monitoring
def start_monitoring(client):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    while True:
        listen_and_analyze_clip(client, recognizer, microphone)
        time.sleep(1)  # Short delay to prevent excessive CPU usage

# Main function to set up and run the real-time monitoring
def run_real_time_monitoring(api_key):
    client = init_cohere(api_key)
    print("Starting real-time scam monitoring...")
    
    start_monitoring(client)

# Example usage
if __name__ == "__main__":
    api_key = "" #Add the cohere api key here.   
    run_real_time_monitoring(api_key)

sys.stderr = stderr
