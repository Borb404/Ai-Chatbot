import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
import re

class ChatbotGUI:
    
    def __init__(self, root, on_send_click, on_clear_click, on_save_click):
        """
        Initializes the window layout, widgets, and configures event bindings.
        
        Parameters:
        - root (tk.Tk): The main Tkinter root window.
        - on_send_click (callable): Function to call when user sends a message.
        - on_clear_click (callable): Function to call when clearing chat log.
        - on_save_click (callable): Function to call when saving chat log to file.
        """
        self.root = root
        self.on_send_click = on_send_click
        self.on_clear_click = on_clear_click
        self.on_save_click = on_save_click

        # Configure window settings
        self.root.title("College Project: AI Chatbot using Gemini & Python")
        self.root.geometry("600x650")
        self.root.minsize(500, 500) # prevent shrinking too much
        
        # Color Palette - Professional/Modern styling (Slate/Blue theme)
        self.COLOR_PRIMARY = "#2C3E50"    # Dark blue-gray for headers
        self.COLOR_BG = "#ECF0F1"         # Very light gray background
        self.COLOR_CARD_BG = "#FFFFFF"    # White background for text areas
        self.COLOR_TEXT = "#2C3E50"       # Dark text
        self.COLOR_ACCENT = "#2980B9"     # Accent blue for buttons
        self.COLOR_SUCCESS = "#27AE60"    # Green for save/success indicators
        self.COLOR_DANGER = "#C0392B"     # Red for exit button
        self.COLOR_SECONDARY = "#7F8C8D"  # Neutral gray for secondary elements
        
        # Set overall background color of the root window
        self.root.configure(bg=self.COLOR_BG)

        # ----------------------------------------------------
        # 1. HEADER SECTION
        # ----------------------------------------------------
        self.header_frame = tk.Frame(self.root, bg=self.COLOR_PRIMARY, height=60)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)
        self.header_frame.pack_propagate(False) # lock height

        self.title_label = tk.Label(
            self.header_frame, 
            text="AI Chatbot Assistant (Gemini API)", 
            font=("Helvetica", 14, "bold"), 
            fg="white", 
            bg=self.COLOR_PRIMARY
        )
        self.title_label.pack(pady=15)

        # ----------------------------------------------------
        # 2. CHAT DISPLAY AREA (Scrollable text box)
        # ----------------------------------------------------
        self.display_frame = tk.Frame(self.root, bg=self.COLOR_BG)
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # ScrolledText acts as our chat area.
        # state=tk.DISABLED makes it read-only so users can't type directly into it.
        self.chat_display = ScrolledText(
            self.display_frame, 
            wrap=tk.WORD, 
            bg=self.COLOR_CARD_BG, 
            fg=self.COLOR_TEXT, 
            font=("Arial", 10), 
            padx=10, 
            pady=10,
            borderwidth=1,
            relief=tk.SOLID
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED) # Disable typing at first

        # Configure custom text tags for formatting (makes User and AI messages distinct)
        self.chat_display.tag_config("user_tag", foreground="#2980B9", font=("Arial", 10, "bold"), spacing1=6)
        self.chat_display.tag_config("ai_tag", foreground="#27AE60", font=("Arial", 10, "bold"), spacing1=6)
        self.chat_display.tag_config("time_tag", foreground="#7F8C8D", font=("Arial", 8, "italic"), spacing1=6)
        self.chat_display.tag_config("text_tag", foreground="#2C3E50", font=("Arial", 10), lmargin1=10, lmargin2=10, spacing3=3)
        self.chat_display.tag_config("system_tag", foreground="#D35400", font=("Arial", 9, "bold"), spacing1=6)
        self.chat_display.tag_config("system_text_tag", foreground="#D35400", font=("Arial", 10, "italic"), lmargin1=10, lmargin2=10, spacing3=3)
        
        # Markdown inline styling tags
        self.chat_display.tag_config("bold_text_tag", foreground="#2C3E50", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("italic_text_tag", foreground="#2C3E50", font=("Arial", 10, "italic"))
        self.chat_display.tag_config("bold_italic_tag", foreground="#2C3E50", font=("Arial", 10, "bold italic"))
        self.chat_display.tag_config("inline_code_tag", foreground="#C7254E", background="#F2F4F4", font=("Courier New", 9))
        
        # Markdown block styling tags
        self.chat_display.tag_config("code_block_tag", foreground="#232B2B", background="#F2F4F4", font=("Courier New", 9), lmargin1=30, lmargin2=30, spacing1=3, spacing3=3)
        self.chat_display.tag_config("bullet_tag", foreground="#2C3E50", font=("Arial", 10), lmargin1=25, lmargin2=35, spacing3=3)
        self.chat_display.tag_config("list_tag", foreground="#2C3E50", font=("Arial", 10), lmargin1=25, lmargin2=35, spacing3=3)
        
        # Headings tags
        self.chat_display.tag_config("h1_tag", foreground="#1B2631", font=("Arial", 13, "bold"), spacing1=10, spacing3=5, lmargin1=10, lmargin2=10)
        self.chat_display.tag_config("h2_tag", foreground="#1B2631", font=("Arial", 11, "bold"), spacing1=8, spacing3=4, lmargin1=10, lmargin2=10)
        self.chat_display.tag_config("h3_tag", foreground="#2C3E50", font=("Arial", 10, "bold"), spacing1=6, spacing3=3, lmargin1=10, lmargin2=10)

        # ----------------------------------------------------
        # 3. INPUT AREA (For typing messages)
        # ----------------------------------------------------
        self.input_frame = tk.Frame(self.root, bg=self.COLOR_BG)
        self.input_frame.pack(fill=tk.X, padx=15, pady=5)

        self.input_box = tk.Entry(
            self.input_frame, 
            font=("Arial", 11), 
            bg=self.COLOR_CARD_BG, 
            fg=self.COLOR_TEXT,
            borderwidth=1,
            relief=tk.SOLID
        )
        self.input_box.pack(fill=tk.X, ipady=8, expand=True)
        self.input_box.focus() # Place blinking cursor in input box by default
        
        # Bind the Enter key to automatically send the message
        self.input_box.bind("<Return>", self._on_enter_pressed)

        # ----------------------------------------------------
        # 4. CONTROL PANEL (Buttons: Send, Clear, Save, Exit)
        # ----------------------------------------------------
        self.control_frame = tk.Frame(self.root, bg=self.COLOR_BG)
        self.control_frame.pack(fill=tk.X, padx=15, pady=15)

        # Adjust column widths so they stretch evenly
        self.control_frame.columnconfigure(0, weight=1)
        self.control_frame.columnconfigure(1, weight=1)
        self.control_frame.columnconfigure(2, weight=1)
        self.control_frame.columnconfigure(3, weight=1)

        # BUTTON 1: Send Message
        self.btn_send = tk.Button(
            self.control_frame, 
            text="Send Message", 
            command=self._handle_send,
            bg=self.COLOR_ACCENT, 
            fg="white", 
            font=("Arial", 9, "bold"),
            relief=tk.FLAT,
            activebackground="#1F618D",
            activeforeground="white",
            cursor="hand2"
        )
        self.btn_send.grid(row=0, column=0, padx=5, ipady=6, sticky="ew")

        # BUTTON 2: Clear Chat
        self.btn_clear = tk.Button(
            self.control_frame, 
            text="Clear Chat", 
            command=self._handle_clear,
            bg=self.COLOR_SECONDARY, 
            fg="white", 
            font=("Arial", 9, "bold"),
            relief=tk.FLAT,
            activebackground="#5D6D7E",
            activeforeground="white",
            cursor="hand2"
        )
        self.btn_clear.grid(row=0, column=1, padx=5, ipady=6, sticky="ew")

        # BUTTON 3: Save History
        self.btn_save = tk.Button(
            self.control_frame, 
            text="Save Chat Log", 
            command=self._handle_save,
            bg=self.COLOR_SUCCESS, 
            fg="white", 
            font=("Arial", 9, "bold"),
            relief=tk.FLAT,
            activebackground="#1E8449",
            activeforeground="white",
            cursor="hand2"
        )
        self.btn_save.grid(row=0, column=2, padx=5, ipady=6, sticky="ew")

        # BUTTON 4: Exit Application
        self.btn_exit = tk.Button(
            self.control_frame, 
            text="Exit Project", 
            command=self._handle_exit,
            bg=self.COLOR_DANGER, 
            fg="white", 
            font=("Arial", 9, "bold"),
            relief=tk.FLAT,
            activebackground="#943126",
            activeforeground="white",
            cursor="hand2"
        )
        self.btn_exit.grid(row=0, column=3, padx=5, ipady=6, sticky="ew")

        # Bind hover events to buttons for dynamic feedback
        self._setup_button_hovers()

    # ----------------------------------------------------
    # EVENT HANDLERS & INTERNAL METHODS
    # ----------------------------------------------------
    
    def _setup_button_hovers(self):
        """Adds mouse-hover styling to control buttons for premium interactive feel."""
        def bind_hover(btn, hover_bg, normal_bg):
            btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
            btn.bind("<Leave>", lambda e: btn.config(bg=normal_bg))
            
        bind_hover(self.btn_send, "#1F618D", self.COLOR_ACCENT)
        bind_hover(self.btn_clear, "#5D6D7E", self.COLOR_SECONDARY)
        bind_hover(self.btn_save, "#1E8449", self.COLOR_SUCCESS)
        bind_hover(self.btn_exit, "#943126", self.COLOR_DANGER)

    def show_typing_placeholder(self, timestamp=None):
        """
        Appends a temporary "AI is processing..." message to the chat display
        and marks its location so it can be cleanly removed later.
        """
        if not timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.chat_display.config(state=tk.NORMAL)
        
        # Mark the start of the placeholder
        self.chat_display.mark_set("placeholder_start", "insert")
        self.chat_display.mark_gravity("placeholder_start", tk.LEFT) # keep mark at start
        
        # Insert placeholder text
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "time_tag")
        self.chat_display.insert(tk.END, "System Notification: ", "system_tag")
        self.chat_display.insert(tk.END, "AI is processing...\n\n", "system_text_tag")
        
        # Mark the end of the placeholder
        self.chat_display.mark_set("placeholder_end", "insert")
        self.chat_display.mark_gravity("placeholder_end", tk.RIGHT)
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def remove_typing_placeholder(self):
        """
        Removes the temporary typing placeholder if it exists on screen.
        """
        self.chat_display.config(state=tk.NORMAL)
        try:
            # Check if mark exists by trying to get its index
            self.chat_display.index("placeholder_start")
            self.chat_display.index("placeholder_end")
            self.chat_display.delete("placeholder_start", "placeholder_end")
        except Exception:
            pass
        
        # Clean up the marks
        try:
            self.chat_display.mark_unset("placeholder_start")
            self.chat_display.mark_unset("placeholder_end")
        except Exception:
            pass
            
        self.chat_display.config(state=tk.DISABLED)

    def _insert_styled_text(self, text, base_tag):
        """
        Parses a single line of text for inline formatting (**bold**, *italic*, `code`)
        and inserts it with the appropriate tags.
        """
        i = 0
        n = len(text)
        
        # Active styles
        bold = False
        italic = False
        code = False
        
        # We will accumulate text and insert when style changes
        current_chunk = []
        
        def flush():
            nonlocal current_chunk
            if not current_chunk:
                return
            chunk_text = "".join(current_chunk)
            current_chunk = []
            
            # Determine tag based on current states
            if code:
                tag = "inline_code_tag"
            elif bold and italic:
                tag = "bold_italic_tag"
            elif bold:
                tag = "bold_text_tag"
            elif italic:
                tag = "italic_text_tag"
            else:
                tag = base_tag
                
            self.chat_display.insert(tk.END, chunk_text, tag)

        while i < n:
            # Check for inline code: `code`
            if text[i] == '`':
                flush()
                code = not code
                i += 1
                continue
                
            # If in code mode, we treat everything literally until the next backtick
            if code:
                current_chunk.append(text[i])
                i += 1
                continue
                
            # Check for bold: **
            if i + 1 < n and text[i:i+2] == '**':
                flush()
                bold = not bold
                i += 2
                continue
                
            # Check for italic: * or _
            if text[i] == '*' or text[i] == '_':
                flush()
                italic = not italic
                i += 1
                continue
                
            # Regular character
            current_chunk.append(text[i])
            i += 1
            
        flush()

    def clean_latex_markup(self, text):
        r"""
        Cleans up common LaTeX formatting generated by LLMs, such as temperature scales
        (e.g., $35^\circ\text{C}$ -> 35°C) and simple inline math numbers (e.g., $5$ -> 5).
        """
        if not text:
            return text
        
        # 1. Replace temperature LaTeX markup like $35^\circ\text{C}$ or 35^\circ\text{C} or $35^\circ C$
        text = re.sub(r'\$?([+-]?[0-9]+(?:\.[0-9]+)?)\^\\circ\\text\{([CFcf])\}\$?', r'\1°\2', text)
        text = re.sub(r'\$?([+-]?[0-9]+(?:\.[0-9]+)?)\^\\circ\s*([CFcf])\$?', r'\1°\2', text)
        
        # 2. Replace general degree symbol expressions like 35^\circ
        text = re.sub(r'([+-]?[0-9]+(?:\.[0-9]+)?)\^\\circ', r'\1°', text)
        
        # 3. Clean up simple numeric variables wrapped in dollar signs (e.g., $35$ -> 35, $-2.5$ -> -2.5)
        text = re.sub(r'\$([+-]?[0-9]+(?:\.[0-9]+)?)\$', r'\1', text)
        
        # 4. Clean up other LaTeX math symbols occasionally returned
        text = text.replace(r'\times', '×')
        text = text.replace(r'\div', '÷')
        text = text.replace(r'\pm', '±')
        text = text.replace(r'\ge', '≥')
        text = text.replace(r'\le', '≤')
        text = text.replace(r'\neq', '≠')
        text = text.replace(r'\approx', '≈')
        
        return text

    def append_message(self, sender, message, timestamp=None):
        """
        Appends a formatted message with sender and date/time timestamp to the text area.
        Parses Markdown formatting (bold, italics, headings, code blocks, lists) and applies styling.
        
        Parameters:
        - sender (str): 'User', 'AI', or 'System'
        - message (str): Content of the message.
        - timestamp (str, optional): Current date/time. If None, it generates one.
        """
        if not timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 1. Enable editing on the widget momentarily
        self.chat_display.config(state=tk.NORMAL)
        
        # 2. Append timestamp
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "time_tag")
        
        # 3. Append Sender prefix based on who sent it
        base_tag = "text_tag"
        if sender == "User":
            self.chat_display.insert(tk.END, "User: ", "user_tag")
        elif sender == "AI":
            # Add AI label on its own line for structured layout
            self.chat_display.insert(tk.END, "AI Assistant:\n", "ai_tag")
        else:
            self.chat_display.insert(tk.END, "System Notification: ", "system_tag")
            base_tag = "system_text_tag"

        # 4. Clean leading/trailing spaces/newlines from response
        clean_msg = message.strip()
        # Clean LaTeX formatting before splitting into lines
        clean_msg = self.clean_latex_markup(clean_msg)
        lines = clean_msg.split("\n")
        in_code_block = False
        
        for line in lines:
            # Check code block toggle
            if line.strip().startswith("```"):
                if in_code_block:
                    in_code_block = False
                    # Add newline space at end of block
                    self.chat_display.insert(tk.END, "\n", "code_block_tag")
                else:
                    in_code_block = True
                    # Add newline space before block starts
                    self.chat_display.insert(tk.END, "\n", base_tag)
                continue
                
            if in_code_block:
                # Render inside a code block with monospace, background highlight and left margin
                self.chat_display.insert(tk.END, f"  {line}\n", "code_block_tag")
                continue
                
            # Parse headings
            if line.startswith("# "):
                self._insert_styled_text(line[2:], "h1_tag")
                self.chat_display.insert(tk.END, "\n", "h1_tag")
            elif line.startswith("## "):
                self._insert_styled_text(line[3:], "h2_tag")
                self.chat_display.insert(tk.END, "\n", "h2_tag")
            elif line.startswith("### "):
                self._insert_styled_text(line[4:], "h3_tag")
                self.chat_display.insert(tk.END, "\n", "h3_tag")
            # Parse bullet list items
            elif line.strip().startswith("* ") or line.strip().startswith("- ") or line.strip().startswith("• "):
                # strip standard bullet chars
                bullet_content = line.strip().lstrip("*-•").strip()
                self.chat_display.insert(tk.END, "  • ", "bullet_tag")
                self._insert_styled_text(bullet_content, "bullet_tag")
                self.chat_display.insert(tk.END, "\n", "bullet_tag")
            # Parse numbered list items
            elif line.strip() and line.strip().split(".")[0].isdigit() and line.strip().startswith(line.strip().split(".")[0] + ". "):
                parts = line.strip().split(". ", 1)
                num = parts[0]
                content = parts[1]
                self.chat_display.insert(tk.END, f"  {num}. ", "list_tag")
                self._insert_styled_text(content, "list_tag")
                self.chat_display.insert(tk.END, "\n", "list_tag")
            else:
                # Standard line of text
                self._insert_styled_text(line, base_tag)
                self.chat_display.insert(tk.END, "\n", base_tag)
                
        # Append empty separating line at the end
        self.chat_display.insert(tk.END, "\n", base_tag)
        
        # 5. Scroll automatically to the bottom
        self.chat_display.see(tk.END)
        
        # 6. Disable editing again to protect history
        self.chat_display.config(state=tk.DISABLED)

    def prompt_api_key(self):
        """
        Opens a popup dialog box to safely retrieve the Gemini API key from the user
        if not set in the environment variables.
        
        Returns:
        - str: The API key input by user, or None if cancelled.
        """
        # Create a simple top-level popup dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("API Key Required")
        dialog.geometry("400x150")
        dialog.resizable(False, False)
        dialog.configure(bg=self.COLOR_BG)
        
        # Make the dialog modal (captures focus)
        dialog.transient(self.root)
        dialog.grab_set()

        label = tk.Label(
            dialog, 
            text="Enter your Gemini API Key to continue:", 
            bg=self.COLOR_BG, 
            fg=self.COLOR_TEXT, 
            font=("Arial", 10, "bold")
        )
        label.pack(pady=10)

        entry = tk.Entry(dialog, show="*", font=("Arial", 10), width=45)
        entry.pack(pady=5)
        entry.focus()

        key_value = {"key": None} # mutable reference to store value

        def submit():
            key_value["key"] = entry.get().strip()
            dialog.destroy()

        btn_ok = tk.Button(
            dialog, 
            text="Submit Key", 
            command=submit, 
            bg=self.COLOR_ACCENT, 
            fg="white"
        )
        btn_ok.pack(pady=10)

        # Wait for the dialog window to be closed/destroyed
        self.root.wait_window(dialog)
        return key_value["key"]

    def clear_screen(self):
        """
        Clears the chat text area.
        """
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete('1.0', tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def _on_enter_pressed(self, event):
        """
        Triggered when Enter key is pressed inside the input box.
        """
        self._handle_send()

    def _handle_send(self):
        """
        Processes text sending: fetches text from input box and calls parent controller.
        """
        text = self.input_box.get().strip()
        if text:
            # Clear input box immediately so user can type the next message
            self.input_box.delete(0, tk.END)
            # Invoke the callback function registered in main.py
            self.on_send_click(text)

    def _handle_clear(self):
        """
        Asks user for confirmation and triggers clear callback if approved.
        """
        confirm = messagebox.askyesno("Clear Chat History", "Are you sure you want to clear the current chat display?")
        if confirm:
            self.on_clear_click()

    def _handle_save(self):
        """
        Opens a standard save file dialog and calls save callback.
        """
        # Suggest a default filename (can be customized by controller)
        suggested_name = "chat_log.txt"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=suggested_name,
            title="Save Chat Logs"
        )
        if file_path:
            self.on_save_click(file_path)

    def _handle_exit(self):
        """
        Prompts confirmation before exiting the Tkinter window.
        """
        confirm = messagebox.askyesno("Exit Chatbot", "Do you want to exit the application?")
        if confirm:
            self.root.destroy()
