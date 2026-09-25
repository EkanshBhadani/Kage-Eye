# 🎌 MAL Form Monitor

A lightweight Python automation tool that connects **MyAnimeList 🗨️ + Google Forms 📋 + Excel 📊** to automatically process forum-based form submissions.

## ✨ Features

- 🎌 **MyAnimeList API Integration**
- 🔎 Automatic forum submission detection
- 👤 Username extraction & matching
- 📋 Google Sheets response retrieval
- 🕒 Automatically selects the latest form submission
- 🧮 Automatic score parsing
- ✅ Pass / ❌ Fail / ⚠️ Missing detection
- 🔁 Duplicate processing prevention
- 💾 Persistent processing state
- 📊 Automatic Excel report generation
- 📝 Results, Summary & Audit Log sheets
- 📜 Detailed application logging
- 👥 Supports multiple forum & form submissions

## 🔄 How It Works

```text
🗨️ MAL Forum
     ↓
🌐 MAL API
     ↓
👤 Extract Username
     ↓
📋 Google Sheets
     ↓
🔍 Find Latest Submission
     ↓
🧮 Parse Score
     ↓
💾 Check State
     ↓
┌───────┬───────┬─────────┐
│   ✅  │   ❌  │   ⚠️    │
│ Passed│ Failed│ Missing │
└───────┴───────┴─────────┘
     ↓
📊 Excel Report
     ↓
📝 Log File

📁 Project Structure

mal-form-monitor/
│
├── 🐍 main.py
├── ⚙️ config.py
├── 🎌 mal_client.py
├── 📋 sheets_client.py
├── 💾 state_manager.py
├── 📊 report_writer.py
├── 📝 logger_setup.py
│
├── 📦 requirements.txt
├── 🔐 .env
│
└── data/
    ├── 📊 results.xlsx
    ├── 💾 processed_state.json
    └── 📝 monitor.log

🛠️ Tech Stack

🐍 Python

🎌 MyAnimeList API v2

📋 Google Sheets

🐼 Pandas

🌐 Requests

📊 OpenPyXL

🔐 python-dotenv


🚀 Version 1.0.0

Status: 🟢 Core system operational
Version: 1.0.0

> Built to make MAL-based form monitoring faster, cleaner, and more automated. 🎯x