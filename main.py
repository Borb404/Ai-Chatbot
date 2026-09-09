import os
import tkinter as tk
from tkinter import messagebox
import threading
from datetime import datetime


from gui import ChatbotGUI
from ai_chat import GeminiChatClient
from history import save_chat_to_file

def load_dotenv():
    """
    A simple, pure-Python implementation of dotenv parser.
    Reads a '.env' file in the current directory and sets environment variables.
    This eliminates the need to install the 'python-dotenv' package.
    """
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(dotenv_path):
        try:
            with open(dotenv_path, "r", encoding="utf-8") as file:
                for line in file:
                    # Remove leading/trailing whitespaces
                    line = line.strip()
                    # Skip empty lines and comment lines
                    if not line or line.startswith("#"):
                        continue
                    # Split at the first '=' symbol
                    if "=" in line:
                        key, value = line.split("=", 1)
                        # Set to os.environ (strip keys/values of whitespace/quotes)
                        os.environ[key.strip()] = value.strip().strip('"').strip("'")
        except Exception as e:
            print(f"Warning: Failed to load .env file manually: {e}")

class ChatbotController:
    """
    Main controller class for the application.
    Implements the MVC/Controller design pattern by linking model (AI & History)
    with the view (GUI) layer.
    """
    def __init__(self):
        # 1. Initialize variables
        self.chat_log = [] # Holds the list of message dicts: {'sender', 'message', 'time'}
        self.ai_client = GeminiChatClient()
        
        # 2. Try loading environment variables from a local .env file using our custom loader
        load_dotenv()
        
        # 3. Initialize Tkinter Root Window
        self.root = tk.Tk()
        
        # 4. Instantiate the View (GUI)
        # We pass self callback methods so that GUI actions invoke controller logic.
        self.gui = ChatbotGUI(
            root=self.root,
            on_send_click=self.handle_send,
            on_clear_click=self.handle_clear,
            on_save_click=self.handle_save
        )
        
        # 5. Bootstrap API configuration
        self.bootstrap_api()

    def bootstrap_api(self):
        """
        Attempts to automatically configure the Gemini API client using
        an environment variable (from system or .env file).
        """
        env_key = os.getenv("GEMINI_API_KEY")
        if env_key:
            success = self.ai_client.initialize_client(env_key)
            if success:
                self.gui.append_message(
                    sender="System", 
                    message="Welcome! Gemini API Client initialized successfully using env variable.",
                    timestamp=self.get_current_timestamp()
                )
                return
                
        # If API key is not found in env
        self.gui.append_message(
            sender="System",
            message="No API Key detected. You will be prompted to enter your Gemini API Key when you send your first message, or you can create a .env file with GEMINI_API_KEY.",
            timestamp=self.get_current_timestamp()
        )

    def get_current_timestamp(self):
        """Helper to get current time formatted as YYYY-MM-DD HH:MM:SS"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def handle_send(self, user_message):
        """
        Processes a sent message.
        Starts a background thread to fetch Gemini responses to prevent GUI freeze.
        """
        # If the API key is not configured yet, prompt the user for it
        if not self.ai_client.api_key_configured:
            api_key = self.gui.prompt_api_key()
            if not api_key:
                messagebox.showerror("Error", "Gemini API key is required to send messages.")
                return
                
            success = self.ai_client.initialize_client(api_key)
            if not success:
                messagebox.showerror("Error", "Invalid API key format or initialization failed.")
                return
            else:
                self.gui.append_message(
                    sender="System", 
                    message="API Client configured successfully!",
                    timestamp=self.get_current_timestamp()
                )

        # 1. Log the user's message in memory
        timestamp = self.get_current_timestamp()
        message_entry = {
            "sender": "User",
            "message": user_message,
            "time": timestamp
        }
        self.chat_log.append(message_entry)

        # 2. Render user message to the GUI chat display
        self.gui.append_message("User", user_message, timestamp)

        # 3. Add a temporary "Thinking..." placeholder from the System
        self.gui.show_typing_placeholder(self.get_current_timestamp())

        # Disable send button and input while waiting to avoid double requests
        self.gui.btn_send.config(state=tk.DISABLED)

        # 4. Spin up a separate worker thread to fetch the Gemini response.
        # This keeps the main Tkinter mainloop responsive, preventing 'Not Responding' crashes.
        api_thread = threading.Thread(
            target=self.fetch_ai_response_worker, 
            args=(user_message,),
            daemon=True # thread terminates automatically if window is closed
        )
        api_thread.start()

    def fetch_ai_response_worker(self, user_message):
        """
        Worker thread function that calls the Gemini API and updates the GUI.
        Runs in background.
        """
        # Call the Gemini model (passing memory list for contextual responses)
        ai_response = self.ai_client.get_response(user_message, self.chat_log[:-1])
        
        # Schedule GUI updates on the main Tkinter thread using root.after
        self.root.after(0, self.update_gui_with_response, ai_response)

    def update_gui_with_response(self, ai_response):
        """
        Updates the GUI with the AI response. Executed back on the main GUI thread.
        """
        # Re-enable the send button
        self.gui.btn_send.config(state=tk.NORMAL)

        # Clear the "AI is processing..." placeholder and append the official AI response
        self.gui.remove_typing_placeholder()
        
        timestamp = self.get_current_timestamp()
        
        # Log response in memory
        message_entry = {
            "sender": "AI",
            "message": ai_response,
            "time": timestamp
        }
        self.chat_log.append(message_entry)

        # Append to UI
        self.gui.append_message("AI", ai_response, timestamp)

    def handle_clear(self):
        """
        Clears the local memory logs and wipes the GUI chat text area.
        """
        self.chat_log.clear()
        self.gui.clear_screen()
        self.gui.append_message("System", "Chat screen cleared.", self.get_current_timestamp())

    def handle_save(self, file_path):
        """
        Delegates the saving of chat records to the history module.
        """
        if not self.chat_log:
            messagebox.showwarning("Save Failed", "There are no messages in the chat history to save.")
            return

        success = save_chat_to_file(self.chat_log, file_path)
        if success:
            messagebox.showinfo("Success", f"Chat history successfully saved to:\n{file_path}")
        else:
            messagebox.showerror("Error", "An error occurred while saving the chat log file.")

    def run(self):
        """
        Starts the Tkinter application event loop.
        """
        self.root.mainloop()

if __name__ == "__main__":
    # Standard entry check to execute the application
    app = ChatbotController()
    app.run()

