# Presentation Slides: AI Chatbot using Python and Gemini API

This file outlines the slide deck content for your college assignment project presentation. You can easily copy these contents into Microsoft PowerPoint, Google Slides, or a Markdown slide viewer (like Marp).

---

## Slide 1: Title Slide
### AI Chatbot Development using Python and Gemini API
**A Modular Python Application Project**

*Presented by:*
- **Team Member 1 (Lead Developer)** - Main controller, thread handling, integration
- **Team Member 2 (UI Designer)** - Tkinter graphical design, fonts, aesthetics
- **Team Member 3 (API Specialist)** - Gemini client configuration, model parameters
- *Course Name:* Python Programming Laboratory
- *Submission Date:* May 20, 2026

---

## Slide 2: Introduction
* **Concept**: Conversational AI chatbot executing locally on a desktop but powered by state-of-the-art cloud language models.
* **Core Goal**: Develop a user-friendly chat assistant GUI that allows users to ask general queries, get smart answers, and log histories.
* **Design Philosophy**: High modularity, thread safety, clear error messages, and beginner-friendly Python styling.

---

## Slide 3: Project Objectives
* **Modular Structure**: Demonstrate standard software engineering principles by separating UI, I/O, and business logic.
* **Gemini LLM Integration**: Connect directly to Google Gemini's high-speed model (`gemini-1.5-flash`).
* **Enhanced Usability**: Avoid terminal interfaces; design a graphical canvas with buttons and keyboard listeners.
* **Non-Blocking Logic**: Use background threads to ensure UI responsiveness.
* **Persistent Records**: Allow export of chats with precise stamps.

---

## Slide 4: Technologies Used
* **Backend Language**: Python 3.8+ (Compatible with Python 3.14+)
* **GUI Engine**: Tkinter (Python standard library)
* **API Integration**: Direct HTTP POST via `urllib.request` (Zero external packages!)
* **System Settings**: Built-in `.env` file parser (no `python-dotenv` required)
* **Concurrency**: `threading` module (Standard Python)
* **File Persistence**: UTF-8 encoded text writer (`open()`)


---

## Slide 5: Project Directory Structure
A clean file structure that isolates responsibilities:
```
chatbot_project/
├── main.py            # Bootstrap application, coordinates events & threads
├── gui.py            # Builds frames, buttons, text box, handles colors
├── ai_chat.py        # Initializes Gemini model, makes request calls
├── history.py        # Generates text outputs and parses file writing
├── requirements.txt  # Project libraries list
└── README.md         # Usage docs and diagrams
```

---

## Slide 6: System Architecture Diagram
```
             [ User ]
                │ (Interacts)
                ▼
         ┌──────────────┐
         │ Tkinter GUI  │  ◄─── (gui.py - View)
         └──────┬───────┘
                │ (Triggers callback)
                ▼
         ┌──────────────┐
         │  Controller  │  ◄─── (main.py - Controller)
         └──────┬───────┘
          ┌─────┴──────┐
          ▼            ▼
     ┌──────────┐ ┌──────────┐
     │ Gemini   │ │ History  │ ◄─── (Models)
     │ Client   │ │ Logger   │
     └──────────┘ └──────────┘
```

---

## Slide 7: Functional Workflow (How it Works)
1. **Startup**: `main.py` runs, loads `.env` file, and opens the Tkinter window.
2. **Input**: User enters text in the input box and presses **Send** or **Enter**.
3. **Execution**: 
   - User's message is immediately stamped and printed to the chat space.
   - A background thread is generated to request Gemini API data.
   - The GUI remains active (showing "AI is processing...") and does not lock up.
4. **Rendering**: Once Gemini replies, the thread notifies the GUI to render the text.
5. **Persistence**: The user can export the chat log to a text file with one click.

---

## Slide 8: Key Features
* **DateTime Stamp**: Every query and reply is marked with an exact timestamp `[YYYY-MM-DD HH:MM:SS]`.
* **Multi-Threading**: The interface stays fluid even during network delays.
* **Worry-Free Key Setup**: The GUI pops up an input box if the API key is missing.
* **Format Styling**: Text rendering distinguishes User (blue), AI (green), and System (orange) responses.
* **Control Buttons**: Quick clear, save, and exit triggers.

---

## Slide 9: Team Member Contributions
* **Member 1 (Lead Developer)**:
  - Coded `main.py` entry logic.
  - Implemented multi-threaded background workers to resolve GUI freezing.
  - Assembled separate components and compiled `requirements.txt`.
* **Member 2 (UI Designer)**:
  - Designed the look-and-feel in `gui.py`.
  - Configured custom tags, fonts, colors, and layout paddings.
  - Developed the API key prompt dialog.
* **Member 3 (API Specialist)**:
  - Configured SDK in `ai_chat.py`.
  - Implemented logic for appending chat context for conversational memory.
  - Authored the project `README.md` and report documentation.

---

## Slide 10: Future Scope
* **SQLite Database**: Save conversations permanently to local databases rather than text files.
* **Multimodality**: Allow users to upload images (Gemini Vision) directly in Tkinter.
* **Voice Activation**: Implement speech-to-text (STT) and text-to-speech (TTS) features.
* **Custom Personalities**: Pre-load academic tutor, code debugger, or language translation system instructions.

---

## Slide 11: Output Screenshots
*(Placeholders for your submission)*

> **Instructions**: Start your app using `python main.py`, take screenshots of:
> 1. Startup screen showing API Key warning.
> 2. API Key Entry Pop-up window.
> 3. Active conversation with timestamps.
> 4. Exporting chat history using Save Chat Log.
>
> Paste your screenshots here!
