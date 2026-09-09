# Modular AI Chatbot using Python and Gemini API

This project is a clean, modular, and beginner-friendly AI Chatbot application designed for a college engineering Python assignment. It uses **Tkinter** for the Graphical User Interface (GUI) and the **Google Gemini API** for intelligence, structured specifically to demonstrate software engineering separation of concerns.

---

## 🏗️ Project Architecture & Data Flow

The project is split into four distinct modules to allow team collaboration and clean division of labor.

### 🔌 System Architecture
The diagram below illustrates how data and control flow through the system:

```mermaid
graph LR
    User([User]) <--> GUI[gui.py - Tkinter GUI]
    GUI <--> Main[main.py - Controller]
    Main <--> AI[ai_chat.py - Gemini API Client]
    Main --> Hist[history.py - Save Logic]
    Hist --> File[(history_log.txt)]
    AI <--> GenAI[Google Gemini Cloud Service]

    style User fill:#d5f5e3,stroke:#27ae60,stroke-width:2px
    style GUI fill:#ebf5fb,stroke:#2980b9,stroke-width:2px
    style Main fill:#fef9e7,stroke:#f1c40f,stroke-width:2px
    style AI fill:#f5eef8,stroke:#8e44ad,stroke-width:2px
    style Hist fill:#fdf2e9,stroke:#e67e22,stroke-width:2px
    style File fill:#eaecee,stroke:#7f8c8d,stroke-width:2px
```

### 🔁 Application Lifecycle (Flowchart)
Here is the functional logical path from starting the application to handling a chat query:

```mermaid
flowchart TD
    Start([1. Start main.py]) --> LoadEnv[2. Load .env config]
    LoadEnv --> InitGui[3. Initialize Tkinter GUI & widgets]
    InitGui --> CheckAPI{4. Is GEMINI_API_KEY set?}
    
    CheckAPI -- Yes --> Ready[5. AI Client configured. Wait for user input]
    CheckAPI -- No --> PromptKey[5. Show setup warning in Chat Area]
    
    PromptKey --> UserType[6. User types message & presses Send/Enter]
    Ready --> UserType
    
    UserType --> CheckClient{7. Is Client Configured?}
    CheckClient -- No --> PromptPopup[8. Show Popup Box for API Key]
    PromptPopup --> InputKey[9. User inputs key & Submits]
    InputKey --> InitClient[10. Initialize Gemini API Client]
    InitClient --> SaveMsg[11. Save & Render User message with timestamp]
    CheckClient -- Yes --> SaveMsg
    
    SaveMsg --> ShowThinking[12. Render System: 'AI is processing...' placeholder]
    ShowThinking --> RunThread[13. Spin up Background Worker Thread]
    
    subgraph Background Thread
        RunThread --> CallGemini[14. Query Gemini API gemini-1.5-flash]
        CallGemini --> ReturnResp[15. Fetch response text or error]
    end
    
    ReturnResp --> PostMain[16. Return response to Main Thread]
    PostMain --> SaveResp[17. Save & Render AI response with timestamp]
    SaveResp --> Wait[18. Idle: Wait for next message]
    
    Wait --> ClearChat{User clicks Clear Chat?}
    ClearChat -- Yes --> ActionClear[19. Wipe Screen & Clear Memory List]
    ActionClear --> Wait
    
    Wait --> SaveFile{User clicks Save Chat Log?}
    SaveFile -- Yes --> ActionSave[20. Write Memory List to file via history.py]
    ActionSave --> Wait
    
    Wait --> ExitApp{User clicks Exit?}
    ExitApp -- Yes --> ActionExit([21. Destroy Tkinter main window])
```

---

## 📁 File Descriptions 

| File | Module Name | Primary Responsibility |
| :--- | :--- | :--- | :--- |
| **`main.py`** | **Controller** | Entry point; handles app orchestration, thread safety, and triggers callbacks. | 
| **`gui.py`** | **View** | Tkinter widgets construction, color palettes, event bindings, and text renders. | 
| **`ai_chat.py`** | **Model (AI)** | Directly queries the Gemini REST API using Python's standard `urllib.request`. | 
| **`history.py`** | **Model (File I/O)**| Text formatting, generating timestamp-based filenames, and file writing. | 
---

## 🚀 Installation & Usage Guide

### Prerequisites
Make sure you have **Python 3.8+** installed on your system. This codebase is fully compatible with pre-release versions such as Python 3.14. You can verify your version by running:
```bash
python --version
```

### Step 1: Set Up your API Key
1. Obtain a free Gemini API Key from Google AI Studio.
2. Duplicate the `.env.template` file and rename it to `.env`:
   ```bash
   copy .env.template .env
   ```
3. Open `.env` in a text editor and replace `your_gemini_api_key_here` with your actual key:
   ```env
   GEMINI_API_KEY=AIzaSyD_ExampleKey123...
   ```
*(Note: If you do not create a `.env` file, the application will automatically pop up a dialog asking for your API Key when you send your first message).*

### Step 2: Run the Application
Since this project uses **only** the Python Standard Library, there are **no external dependencies to install**! You do not need to run `pip install`. Simply start the application by running:
```bash
python main.py
```

---

## 💡 Key Coding Concepts Used (For Viva / Presentation)
- **Zero-Dependency REST API Connection**: Explains how client-server web apps query cloud APIs directly using Python's built-in `urllib.request` and `json` libraries.
- **Object-Oriented Programming (OOP)**: Using classes (`ChatbotGUI`, `GeminiChatClient`, `ChatbotController`) to represent system blocks.
- **Multithreading (`threading` module)**: Moving the API call off the main thread. This prevents the Tkinter application from freezing or showing a "Not Responding" status during network latency.
- **Callback Pattern**: The GUI triggers callback hooks passed to it by `main.py`, showing proper decoupling.
- **File I/O (Context Managers)**: Using `with open(...)` to safely write text files with automatic handle closures.

