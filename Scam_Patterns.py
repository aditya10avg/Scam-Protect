import openai
import speech_recognition as sr
import threading
import time
import os
import sys
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed

# Suppress warnings
warnings.filterwarnings("ignore")

# Redirect stderr to devnull to suppress ALSA errors
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')

# Function to initialize OpenAI client
def init_openai(api_key):
    return openai.OpenAI(api_key=api_key)

# Function to analyze the conversation
def analyze_conversation(client, conversation_text):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an FBI agent who can understand the most likely patterns in financial scam calls. You will sort out important data like the name of the person, the company they are associated with, and all other information that could help track or identify if the person is legit by running a background check. You will also provide time-to-time suggestions to the user to handle the situation wisely."},
                {"role": "user", "content": conversation_text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing conversation: {e}"

# Function to predict if the conversation is suspicious
def is_suspicious(client, conversation_text):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in identifying suspicious patterns in phone calls. Analyze the following conversation and determine if it seems suspiciou.If suspicious just give a word suspicious in output."},
                {"role": "user", "content": conversation_text}
            ]
        )
        return "suspicious" in response.choices[0].message.content.lower()
    except Exception as e:
        print(f"Error in is_suspicious: {e}")
        return False

# Function to suggest next steps if suspicious
def suggest_next_steps(client, conversation_text):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You suggest safe actions to take in a potential scam situation.Help the user know if the person is a fraud or a con man by asking some questions which could reveal the identity.It could be like why do you need my credit card number since you are from the same company and you must be knowing it."},
                {"role": "user", "content": conversation_text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Unable to suggest next steps: {e}"

# New function to extract names from the conversation
def extract_names(client, conversation_text):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Extract and list all names mentioned in the following conversation.For instance ,if the person is introducing himself with his company name just return only those in output."},
                {"role": "user", "content": conversation_text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error extracting names: {e}"

# New function to identify companies mentioned in the conversation
def identify_companies(client, conversation_text):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Identify and list all companies or organizations mentioned in the following conversation."},
                {"role": "user", "content": conversation_text}
            ]
        )
        return response.choices[0].message.content
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
    client = init_openai(api_key)
    print("Starting real-time scam monitoring...")
    
    start_monitoring(client)

# Example usage
if __name__ == "__main__":
    api_key = ""  
    run_real_time_monitoring(api_key)

# Restore stderr
sys.stderr = stderr

                    