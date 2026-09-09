import os
from datetime import datetime

def generate_default_filename():
    """
    Generates a default filename for saving chat history.
    Format: chat_history_YYYYMMDD_HHMMSS.txt
    Example: chat_history_20260520_183015.txt
    """
    now = datetime.now()
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")
    return f"chat_history_{timestamp_str}.txt"

def save_chat_to_file(chat_log, file_path):
    """
    Saves the list of chat messages to a plain text file.
    
    Parameters:
    - chat_log (list): A list of dictionaries representing the conversation.
                       Each dictionary has:
                       - 'sender': 'User' or 'AI'
                       - 'time': string (timestamp)
                       - 'message': string (text content)
    - file_path (str): The full path of the file to save the log to.
    
    Returns:
    - bool: True if saved successfully, False if an error occurred.
    """
    try:
        # Open the file in write mode ('w') with UTF-8 encoding to support special characters
        with open(file_path, 'w', encoding='utf-8') as file:
            # Write a nice header at the top of the file
            file.write("==================================================\n")
            file.write("               AI CHATBOT HISTORY                 \n")
            file.write(f" Saved On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("==================================================\n\n")
            
            # Loop through each message and write it to the file
            for entry in chat_log:
                sender = entry.get('sender', 'Unknown')
                timestamp = entry.get('time', '')
                message = entry.get('message', '')
                
                # Write the message with structured formatting
                file.write(f"[{timestamp}] {sender}:\n")
                file.write(f"{message}\n")
                file.write("-" * 50 + "\n") # separator line
                
        return True
    except Exception as e:
        # Print the error to console for debugging purposes
        print(f"Error saving chat history: {e}")
        return False
