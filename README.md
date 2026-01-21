# Plivo IVR Demo – Forward Deployed Engineer Assignment

This project demonstrates a multi-level Interactive Voice Response (IVR) system built using Plivo’s Voice API. It supports outbound calling, language selection, audio playback, call forwarding to a live agent, and graceful handling of invalid inputs.

---

## Features

- Outbound call trigger via REST API
- Web-based UI to initiate calls
- Multi-level IVR menu
- Language selection (English and Spanish)
- Audio playback
- Live agent call forwarding
- Invalid input handling
- No-input fallback handling
- Production-style IVR looping logic

---

## Tech Stack

- Python
- Flask
- Plivo Voice API
- Plivo XML
- HTML, CSS, JavaScript
- ngrok (for public webhook exposure)

---

## IVR Flow

1. User initiates outbound call
2. Level 1: Language selection
   - Press 1 for English
   - Press 2 for Spanish
3. Level 2: Options
   - Press 1: Play audio
   - Press 2: Connect to live agent
4. Invalid input → Menu repeats
5. No input → Menu repeats

---

## Project Structure

plivo_ivr_demo/
├── app.py
├── templates/
│ └── index.html
├── requirements.txt
├── README.md
├── .gitignore
└── .env (not committed)

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/SwarLodaya/plivo-ivr-demo.git
cd plivo_ivr_demo

