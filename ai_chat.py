import urllib.request
import json
from datetime import datetime

class GeminiChatClient:
    
    def __init__(self):
        self.api_key = None
        self.api_key_configured = False

    def initialize_client(self, api_key):
        
        if not api_key or api_key.strip() == "":
            self.api_key_configured = False
            return False
            
        self.api_key = api_key.strip()
        self.api_key_configured = True
        return True

    def get_response(self, user_message, chat_history=None):
       
        if not self.api_key_configured or not self.api_key:
            return "Error: Gemini API key is not configured. Please set a valid API key."

        
        models_to_try = [
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
            "gemini-3.5-flash",
            "gemini-flash-latest"
        ]

        last_error = None

        # Loop through each candidate model
        for model_name in models_to_try:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
                
                # Format conversation history for multi-turn dialogue
                contents = []
                if chat_history:
                    for entry in chat_history:
                        if entry.get("sender") == "User":
                            contents.append({
                                "role": "user",
                                "parts": [{"text": entry.get("message", "")}]
                            })
                        elif entry.get("sender") == "AI":
                            contents.append({
                                "role": "model",
                                "parts": [{"text": entry.get("message", "")}]
                            })
                
                # Append current user prompt
                contents.append({
                    "role": "user",
                    "parts": [{"text": user_message}]
                })
                
                # Provide the current date and time to Gemini
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Prepare POST payload
                payload = {
                    "systemInstruction": {
                        "parts": [
                            {
                                "text": (
                                    f"The current date and time is {current_datetime}. "
                                    "Use this as the authoritative current date and time when answering "
                                    "questions about today, tomorrow, yesterday, dates, or time."
                                )
                            }
                        ]
                    },
                    "contents": contents
                }

                data = json.dumps(payload).encode("utf-8")
                headers = {"Content-Type": "application/json"}

                req = urllib.request.Request(url, data=data, headers=headers, method="POST")
                
                # Send API request with a 5 second timeout (to switch models fast if one hangs or is slow)
                with urllib.request.urlopen(req, timeout=5) as response:
                    response_data = response.read().decode("utf-8")
                    result = json.loads(response_data)
                    
                    candidates = result.get("candidates", [])
                    if candidates:
                        content = candidates[0].get("content", {})
                        parts = content.get("parts", [])
                        if parts:
                            return parts[0].get("text", "")
                    
                    last_error = "Received empty response from API."
                    print(f"Model '{model_name}' returned empty response. Trying next model...")
                    
            except urllib.error.HTTPError as e:
                last_error = f"HTTP {e.code}"
                try:
                    error_body = e.read().decode("utf-8")
                    error_json = json.loads(error_body)
                    api_msg = error_json.get("error", {}).get("message", "")
                    if api_msg:
                        last_error = f"API HTTP Error ({e.code}): {api_msg}"
                except Exception:
                    pass

                # Early exit conditions where switching models won't help:
                # 400 (Bad request query structure) or 403 (Invalid API Key)
                if e.code in (400, 403):
                    print(f"Fatal API error on model '{model_name}': {last_error}")
                    return last_error

                print(f"Model '{model_name}' failed with {last_error}. Switching immediately to fallback model...")
                
            except Exception as e:
                last_error = f"Connection error: {str(e)}"
                print(f"Model '{model_name}' connection failed: {last_error}. Switching immediately to fallback model...")
        
        # If all API calls fail, activate presentation safety fallback
        # This keeps the user's live demo working even if the Gemini servers are down or offline
        local_response = self.get_local_fallback_response(user_message)
        print(f"\n[SYSTEM ALERT] All Gemini API models failed to respond. Last Error: {last_error}")
        print("Switched to Local Fallback for presentation safety.\n")
        return (
            f"⚠️ [Notice: Running in presentation fallback mode]\n\n"
            f"{local_response}"
        )

    def get_local_fallback_response(self, user_message):
        """
        Generates simulated smart responses locally to ensure the user can demonstrate
        the UI functionalities (sending, clearing, exporting) even without active server access.
        """
        msg_lower = user_message.lower()
        if any(greet in msg_lower for greet in ["hello", "hi", "hey", "hola"]):
            return ("Hello! I am your local fallback assistant. The Gemini API is currently offline "
                    "or busy, but I can still help demonstrate the application features!")
        elif any(keyword in msg_lower for keyword in ["feature", "help", "capability"]):
            return ("This application features:\n"
                    "1. Real-time message logs with precise timestamps\n"
                    "2. Thread-safe background execution to prevent Tkinter window freezes\n"
                    "3. Exportable chat transcripts saved to a file\n"
                    "4. Wiping memory and cleaning screen\n"
                    "5. Multi-model fallback mechanisms")
        elif any(keyword in msg_lower for keyword in ["save", "log", "export", "history"]):
            return ("To save this conversation, click the 'Save Chat Log' button in the panel below. "
                    "It will export this dialogue to a local .txt file.")
        elif "clear" in msg_lower:
            return "To clear this window and wipe the logs from memory, click the 'Clear Chat' button."
        elif "exit" in msg_lower:
            return "To close the application, click 'Exit Project' or close the window."
        else:
            return (f"I received your message: '{user_message}'. Since the API is currently busy, "
                    f"I am responding in local demonstration mode to show that the message loop "
                    f"remains fully functional!")


