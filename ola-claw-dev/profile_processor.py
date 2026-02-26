import os
import json
import requests
import shutil
import time
import sys

STAGING_DIR = "/data/openclaw/workspace/profile_staging"
COMPLETED_DIR = "/data/openclaw/workspace/profile_completed"
OUTPUT_FILE = "/data/openclaw/workspace/extracted_traits.jsonl"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:7b"

PROMPT_TEMPLATE = """Analyze the following text and extract factual bullet points about the subject 'Lord Xar'.
Focus on: Career, Technical Skills, Projects, Trading, Hobbies, Tool Preferences.
Output ONLY a JSON array of strings. 

TEXT:
{text}
"""

def process_file(file_path):
    print(f"[*] Processing: {file_path}")
    sys.stdout.flush()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.strip():
            return []

        payload = {
            "model": MODEL,
            "prompt": PROMPT_TEMPLATE.format(text=content),
            "stream": False,
            "format": "json"
        }

        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        
        raw_output = response.json().get('response', '[]')
        traits = json.loads(raw_output)
        
        if isinstance(traits, list) and traits:
            with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
                for trait in traits:
                    entry = {
                        "source": os.path.basename(file_path),
                        "trait": trait,
                        "timestamp": time.time()
                    }
                    f.write(json.dumps(entry) + "\n")
            print(f"[+] Extracted {len(traits)} traits")
        else:
            print(f"[-] No traits found")
        sys.stdout.flush()
        return traits

    except Exception as e:
        print(f"[!] Error: {e}")
        sys.stdout.flush()
        return None

def main():
    print("[*] Engine active.")
    sys.stdout.flush()
    while True:
        files = [f for f in os.listdir(STAGING_DIR) if f.endswith('.txt')]
        if not files:
            time.sleep(2)
            continue
        
        for filename in files:
            staging_path = os.path.join(STAGING_DIR, filename)
            completed_path = os.path.join(COMPLETED_DIR, filename)
            
            result = process_file(staging_path)
            if result is not None:
                shutil.move(staging_path, completed_path)
                print(f"[OK] {filename}")
                sys.stdout.flush()

if __name__ == "__main__":
    main()
