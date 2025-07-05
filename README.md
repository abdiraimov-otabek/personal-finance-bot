# 💸 PFB — Personal Finance Bot

Telegram bot for managing personal finances directly from chat.  
Track income, expenses, and budgets — all in one minimal and fast bot.

Built with **Python** + **Aiogram 3**, backed by a simple DB, designed for Gen Z speed.

---

## 🧠 Core Features

- ➕ Add income and expenses  
- 📊 View daily/weekly/monthly summaries  
- 🧾 Categorize transactions  
- 💰 Track balance  
- ⏰ Set budgets and get notified if close to limit  
- 📥 Export data as CSV 
- 🔐 Admin-only access (no public usage)

---

## ⚙️ Tech Stack

- Python 3.11+  
- Aiogram 3  
- SQLite (can be upgraded to PostgreSQL)  

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/abdiraimov-otabek/pfb-bot.git
cd pfb-bot

### 2. Setup virtual environment
```bash
python -m venv venv
source venv/bin/activate

### 3. Install requirements
```bash
pip install -r requirements.txt

### 4. Configure .env
```env
BOT_TOKEN=your_telegram_bot_token
ADMIN_ID=your_telegram_id

### 5. Run the bot
```bash
python main.py
