import urllib.request
import json
import os

# Custom dotenv loader
def load_dotenv():
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(dotenv_path):
        try:
            with open(dotenv_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, value = line.split("=", 1)
                        os.environ[key.strip()] = value.strip().strip('"').strip("'")
        except Exception as e:
            print(f"Warning: Failed to load .env: {e}")

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY environment variable or .env file is missing.")
else:
    print(f"Using API Key: {api_key[:8]}...{api_key[-4:] if len(api_key) > 8 else ''}")
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            models = data.get("models", [])
            print("\nAvailable models that support generateContent:")
            for m in models:
                methods = m.get("supportedGenerationMethods", [])
                if "generateContent" in methods:
                    print(f"- {m.get('name')}")
    except Exception as e:
        print(f"API Request Failed: {e}")
