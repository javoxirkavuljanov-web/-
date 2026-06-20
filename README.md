# 💸 Telegram Expense Tracker Bot

A clean, simple Telegram bot for tracking personal income and expenses. Built with Python, aiogram 3.x, SQLite, and SQLAlchemy. Supports English and Russian.

---

## 🗂 Project Structure

```
expense_bot/
├── main.py                  # Entry point
├── config.py                # Bot token config
├── requirements.txt
├── .env.example
├── database/
│   ├── __init__.py
│   └── models.py            # SQLAlchemy models (User, Expense, Income)
├── handlers/
│   ├── __init__.py
│   ├── states.py            # FSM states
│   ├── start.py             # /start, language selection, main menu
│   ├── expense.py           # Add/delete/view expenses
│   ├── income.py            # Add/delete/view incomes
│   └── statistics.py        # Stats, history, monthly summary
├── services/
│   ├── __init__.py
│   ├── user_service.py      # User CRUD + language
│   ├── expense_service.py   # Expense CRUD + queries
│   └── income_service.py    # Income CRUD + queries
├── keyboards/
│   └── __init__.py          # All inline keyboards
└── localization/
    ├── __init__.py          # get_text() loader
    ├── en.json              # English strings
    └── ru.json              # Russian strings
```

---

## ⚙️ Setup

### 1. Clone the project

```bash
git clone <your-repo-url>
cd expense_bot
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your `.env` file

```bash
cp .env.example .env
```

Open `.env` and paste your bot token:

```
BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRsTUVwxYZ
```

> Get your token from [@BotFather](https://t.me/BotFather) on Telegram.

### 5. Run the bot

```bash
python main.py
```

The SQLite database (`bot.db`) is created automatically on first run.

---

## 🤖 Features

| Feature | Description |
|---|---|
| Add Expense | Choose category → enter amount → optional description |
| Add Income | Enter amount → optional description |
| Delete Records | Tap any record in the list to delete it |
| Statistics | Total income, expenses, and balance |
| Monthly Summary | Breakdown by category for the current month |
| Last 10 Transactions | Mixed income + expense history |
| Multi-language | English 🇬🇧 and Russian 🇷🇺 — chosen at /start |

### Expense Categories

🍔 Food · 🚗 Transport · 🛍 Shopping · 🎮 Entertainment · 📚 Education · 💊 Health · 🧾 Bills · 📦 Other

---

## 🧱 Tech Stack

- **Python 3.11+**
- **aiogram 3.x** — async Telegram bot framework
- **SQLite** — simple file-based database, zero setup
- **SQLAlchemy 2.x** — ORM for clean database access
- **python-dotenv** — environment variable management

---

## 📌 Notes

- All data is stored locally in `bot.db` (SQLite)
- FSM (Finite State Machine) is used for multi-step flows (add expense/income)
- Each user's data is isolated by their Telegram ID
- Language preference is saved per user and persists across sessions
