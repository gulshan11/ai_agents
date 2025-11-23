import requests
import json
import random
import datetime

# Configuration
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL = "tinyllama"

# 1. Define the Topics Rotation
TOPICS = [
    "The hidden costs of microservices adoption in mid-sized teams.",
    "How to effectively push back against unrealistic product deadlines as a senior lead.",
    "The art of writing technical design documents (RFCs) that people actually read.",
    "Mentoring junior devs: Teaching them *how to think* vs just giving answers.",
    "Database schema design mistakes that haunt you 3 years later."
]

# Pick a topic based on the week number so it rotates predictably
week_num = datetime.date.today().isocalendar()[1]
todays_topic = TOPICS[week_num % len(TOPICS)]

# 2. Craft the Prompts
system_prompt = """
You are a cynical but helpful Principal Software Engineer. 
Your target audience is Mid-level to Senior Software Engineers.
Write a LinkedIn post (under 200 words) based on the provided topic.
The tone should be professional but authentic—a peer sharing a hard-earned lesson.
End with a thought-provoking question to encourage comments.
Add 3-5 relevant, professional hashtags at the very end.
Do NOT use cheesy opening hooks like "I'm thrilled to announce..."
"""

user_prompt = f"Write a post about: {todays_topic}"

# 3. Call Ollama
payload = {
    "model": MODEL,
    "system": system_prompt,
    "prompt": user_prompt,
    "stream": False
}

try:
    response = requests.post(OLLAMA_ENDPOINT, json=payload)
    response_text = response.json()['response']

    # 4. Output (For now, save to a file)
    filename = f"draft_post_{datetime.date.today()}.txt"
    with open(filename, "w") as f:
        f.write(response_text)
    
    print(f"Successfully generated draft: {filename}")
    print("-" * 20)
    print(response_text)

except Exception as e:
    print(f"Error communicating with Ollama: {e}")