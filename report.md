# Academic Project Report

**Project Title:** AI Chatbot Application Using Python and Gemini API  
**Course Name:** First Year Engineering - Python Programming Lab  
**Date of Submission:** May 20, 2026  

---

## 1. Abstract
This project presents the design and implementation of a desktop-based Artificial Intelligence (AI) Chatbot application. Developed using Python, the chatbot integrates the Google Gemini API to generate smart, contextual responses. The Graphical User Interface (GUI) is constructed using Tkinter, providing a user-friendly and responsive workspace. Key features include timestamped message logs, conversation clearance, runtime API configuration, and the ability to export chat logs to external text files. To ensure a professional software implementation, the project is split into separate modules (Model-View-Controller pattern) and uses multithreading to guarantee a responsive interface during network request execution.

---

## 2. Introduction
Conversational AI has become a cornerstone of modern customer support, educational assistance, and interactive applications. By learning how to design a simple chatbot, students gain crucial experience in:
- Connecting local programs to cloud APIs (Software as a Service - SaaS integration).
- Building graphical user interfaces (GUIs) that handle human inputs.
- Managing memory state and file persistence.
- Writing clean, structured code suitable for multi-developer team environments.

This report documents the architectural design, program execution flow, functional code modules, and implementation details of our AI Chatbot project.

---

## 3. Project Objectives
The main objectives of this development project are:
1. **API Integration**: Establish secure and reliable connections to Google’s Gemini large language model (LLM) to fetch text responses.
2. **Graphical User Interface**: Design a lightweight, clean desktop window using Python's standard `tkinter` library.
3. **Modular Design**: Divide the project into specific code modules (`main.py`, `gui.py`, `ai_chat.py`, and `history.py`) to simulate real-world industry practices and divide workload among three team members.
4. **Local Data Persistence**: Provide options to format and save active chat transcripts to a local text file.
5. **Thread Safety**: Implement asynchronous worker threads to prevent application hangs while querying web APIs.

---

## 4. Technologies Used
- **Programming Language**: Python 3.8+ (Fully compatible with Python 3.14+)
- **GUI Framework**: Tkinter (Python standard library)
- **AI Completion API**: Google Gemini REST API (queried via standard `urllib.request`)
- **Environment Management**: Custom pure-Python `.env` parser (zero external library requirements)
- **Threading Library**: Standard Python `threading` module
- **Data Format**: Text Files (`.txt`) for history logs

---

## 5. Architectural Design
The application utilizes a modular design resembling the Model-View-Controller (MVC) architecture. This approach separates user presentation, data manipulation, and orchestration logic.

### 5.1 Architecture Diagram
```
              ┌────────────────────────┐
              │          User          │
              └───────────┬────────────┘
                          │ (Interacts)
                          ▼
              ┌────────────────────────┐
              │      Tkinter GUI       │  <─── (gui.py - View)
              └───────────┬────────────┘
                          │ (Callback triggers)
                          ▼
              ┌────────────────────────┐
              │   Chatbot Controller   │  <─── (main.py - Orchestrator)
              └─────┬──────────────┬───┘
                    │              │
       (Runs async) │              │ (Local I/O)
                    ▼              ▼
     ┌──────────────────┐    ┌──────────────────┐
     │    Gemini API    │    │   History File   │
     │(ai_chat.py-Model)│    │(history.py-Model)│
     └──────────────────┘    └──────────────────┘
            ▲                      ▲
    (Cloud) │                      │ (Writes)
            ▼                      ▼
  ┌───────────────────┐    ┌──────────────────┐
  │ Google GenAI Cloud│    │  chat_log.txt    │
  └───────────────────┘    └──────────────────┘
```

---

## 6. Functional Module Descriptions

### Module 1: Orchestration & Main Control (`main.py`)
Developed by **Member 1 (Lead Developer)**.  
The core driver of the application. It instantiates the Tkinter root window and configures the `GeminiChatClient` and `ChatbotGUI`. It contains a custom, lightweight, pure-Python `.env` parser that loads API key files without third-party libraries. To ensure the Tkinter screen never locks up during API call lag, `main.py` starts a daemon worker thread (`threading.Thread`) whenever a message is sent.

### Module 2: Graphical User Interface (`gui.py`)
Developed by **Member 2 (UI Designer)**.  
Builds the UI grid, configures colors (slate grey and blue theme), sets fonts, and handles user actions. Message boxes are customized with tag ranges to display timestamps, user tags, and AI response tags with different foreground colors. It supports a fallback popup prompt for API keys if the `.env` configuration is absent.

### Module 3: Gemini API Connector (`ai_chat.py`)
Developed by **Member 3 (AI/API Specialist)**.  
Handles connection and request payloads to Google Gemini's REST API. It uses standard `urllib.request` to execute a POST request directly, bypassing the `google-generativeai` and `protobuf` packages. It manages history parsing into the API's multi-turn schema and completions using the `gemini-1.5-flash` model.

### Module 4: Chat History Exporter (`history.py`)
Collaboratively Developed.  
Writes the accumulated Python list of chat dictionary objects to a file formatted with line separators, stamps, and labels.


---

## 7. Key Features
1. **Dynamic Timestamps**: Automatically logs and renders the exact date and time (`YYYY-MM-DD HH:MM:SS`) for both user queries and bot replies.
2. **Smooth Non-Blocking Threading**: Avoids standard single-threaded Tkinter freezes when processing API calls by sending requests to a background thread.
3. **API Key Dialog Fallback**: Allows runtime manual key configuration if standard `.env` configuration is omitted.
4. **Conversation Memory**: Maintains structural logs during the active session to provide context-aware responses.

---

## 8. Conclusion & Future Enhancements
The project successfully meets all requirements of a modular college computer science project. In future updates, the application can be expanded to support:
- Voice recognition and Text-To-Speech (TTS).
- Database persistence (SQLite) instead of flat text file logs.
- Image inputs (using Multimodal Gemini capabilities).
