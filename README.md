# 🏆 Quiz Master – KBC Inspired Quiz Application

![Django](https://img.shields.io/badge/Django-4.2-green?style=flat-square&logo=django)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?style=flat-square&logo=bootstrap)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?style=flat-square&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

> A full-stack web quiz application inspired by **Kaun Banega Crorepati (KBC)** — built with Django, Bootstrap 5, and vanilla JavaScript. Features 15 progressive levels, lifelines, a countdown timer, leaderboard, and a complete admin panel.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Database Models](#-database-models)
- [Installation & Setup](#-installation--setup)
- [Running the Project](#-running-the-project)
- [Application URLs](#-application-urls)
- [Game Rules](#-game-rules)
- [Prize Ladder](#-prize-ladder)
- [Lifelines](#-lifelines)
- [Admin Panel](#-admin-panel)
- [Screenshots](#-screenshots)
- [Troubleshooting](#-troubleshooting)
- [Future Enhancements](#-future-enhancements)
- [Author](#-author)

---

## ✨ Features

### 🔐 Authentication System
- User Registration with email validation
- Secure Login / Logout
- Django's built-in password hashing (PBKDF2)
- Personal User Dashboard

### 🎮 Quiz System
- 15 progressive question levels (Easy → Medium → Hard)
- Multiple choice questions with 4 options (A, B, C, D)
- 30-second countdown timer per question (JavaScript)
- Wrong answer → Game Over
- Correct answer → Advance to next level
- Keyboard shortcuts (press A / B / C / D to answer)
- Auto-submit on timer expiry

### 🆘 Lifelines (One use each)
- **50-50** — Eliminates 2 wrong options
- **Skip** — Replaces current question with a new one
- **Audience Poll** — Shows simulated poll percentages

### 💰 Score System
- Increasing prize money per level (₹1,000 → ₹1,00,00,000)
- Safe Havens at Level 5 (₹10,000) and Level 10 (₹3,20,000)
- Quit option to walk away with your safe haven amount
- All game sessions saved to the database

### 🏅 Leaderboard
- Top 10 players by best score
- One entry per user (personal best)
- Publicly accessible (no login required)

### 🛠️ Admin Panel
- Add, Edit, Delete questions
- Filter by level and difficulty
- View all game sessions (read-only)
- Manage users with game stats

---

## 🛠 Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| Backend    | Python 3.10+, Django 4.2 |
| Frontend   | HTML5, CSS3, Bootstrap 5.3 |
| JavaScript | Vanilla JS (no frameworks) |
| Database   | SQLite (default Django)  |
| Icons      | Bootstrap Icons 1.10     |
| Auth       | Django Authentication System |

---

## 📁 Project Structure

```
KBC/                       ← Django Project Root
│
├── manage.py
├── db.sqlite3                    ← Auto-generated on migrate
├── requirements.txt
│
├── KBC/                   ← Project Config Package
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── quiz/                         ← Main Application
│   ├── __init__.py
│   ├── admin.py                  ← Admin panel config
│   ├── apps.py
│   ├── forms.py                  ← Register & Login forms
│   ├── models.py                 ← Question, GameSession models
│   ├── urls.py                   ← App-level URL routes
│   ├── views.py                  ← All view logic
│   ├── migrations/
│   │   └── __init__.py
│   └── management/
│       └── commands/
│           └── seed_questions.py ← Sample data seeder
│
├── Templates/                    ← HTML Templates
│   ├── base.html                 ← Master layout (Navbar, Footer)
│   ├── home.html                 ← Landing page
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   └── quiz/
│       ├── dashboard.html        ← User dashboard
│       ├── play.html             ← Main game screen
│       ├── result.html           ← Win / Lose / Quit result
│       └── leaderboard.html      ← Top 10 scores
│
└── static/
    ├── css/
    │   └── style.css             ← Custom KBC-themed dark UI
    └── js/
        └── quiz.js               ← Timer, keyboard shortcuts, lifelines
```

---

## 🗃 Database Models

### `Question`
| Field            | Type        | Description                        |
|------------------|-------------|------------------------------------|
| `text`           | TextField   | The question text                  |
| `option_a/b/c/d` | CharField   | Four answer options                |
| `correct_option` | CharField   | Correct answer (A, B, C, or D)     |
| `difficulty`     | CharField   | easy / medium / hard               |
| `level`          | PositiveInt | Question level (1–15)              |

### `GameSession`
| Field               | Type        | Description                          |
|---------------------|-------------|--------------------------------------|
| `user`              | ForeignKey  | Linked to Django User                |
| `started_at`        | DateTime    | Game start timestamp                 |
| `ended_at`          | DateTime    | Game end timestamp                   |
| `current_level`     | PositiveInt | Current question level (1–15)        |
| `score`             | PositiveInt | Current prize amount                 |
| `status`            | CharField   | active / won / lost / quit           |
| `lifeline_5050`     | BooleanField| 50-50 available?                     |
| `lifeline_skip`     | BooleanField| Skip available?                      |
| `lifeline_poll`     | BooleanField| Audience poll available?             |
| `current_question`  | ForeignKey  | Active question being answered       |
| `eliminated_options`| CharField   | Options removed by 50-50             |

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git (optional)

### Step 1 — Clone or Download the Project

```bash
git clone https://github.com/Apoorav-Mukherjee/KBC-Quiz-App.git
cd KBC
```

### Step 2 — Create a Virtual Environment

```bash
python -m venv venv
```

**Activate it:**

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt` contents:
```
Django>=4.2,<5.0
```

### Step 4 — Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5 — Seed Sample Questions

```bash
python manage.py seed_questions
```

This loads **30 questions** (2 per level) across all 15 levels.

### Step 6 — Create a Superuser (Admin Access)

```bash
python manage.py createsuperuser
```

Enter your desired username, email, and password when prompted.

---

## 🚀 Running the Project

```bash
python manage.py runserver
```

Open your browser and visit: **http://127.0.0.1:8000/**

---

## 🌐 Application URLs

| URL                          | Page                    | Access        |
|------------------------------|-------------------------|---------------|
| `/`                          | Home / Landing Page     | Public        |
| `/register/`                 | User Registration       | Public        |
| `/login/`                    | User Login              | Public        |
| `/logout/`                   | Logout                  | Logged In     |
| `/dashboard/`                | User Dashboard          | Logged In     |
| `/game/start/`               | Start New Game          | Logged In     |
| `/game/play/`                | Game Screen             | Logged In     |
| `/game/answer/`              | Submit Answer (POST)    | Logged In     |
| `/game/quit/`                | Quit Game               | Logged In     |
| `/game/result/`              | Result Screen           | Logged In     |
| `/game/lifeline/<type>/`     | Use Lifeline (POST)     | Logged In     |
| `/leaderboard/`              | Top 10 Scores           | Public        |
| `/admin/`                    | Django Admin Panel      | Superuser     |

**Lifeline types:** `fifty_fifty`, `skip`, `audience_poll`

---

## 🎮 Game Rules

1. Register or log in to start playing.
2. Each game has **15 questions** in increasing difficulty.
3. You have **30 seconds** to answer each question.
4. Selecting the **correct answer** moves you to the next level.
5. Selecting a **wrong answer** ends the game immediately.
6. If the **timer runs out**, it counts as a wrong answer.
7. You can use each **lifeline only once** per game.
8. You can **quit at any time** and keep your safe haven amount.
9. Reaching **Level 15 and answering correctly** wins the game.

---

## 💵 Prize Ladder

| Level | Prize (₹)       | Note           |
|-------|-----------------|----------------|
| 1     | ₹1,000          |                |
| 2     | ₹2,000          |                |
| 3     | ₹3,000          |                |
| 4     | ₹5,000          |                |
| **5** | **₹10,000**     | 🛡️ Safe Haven  |
| 6     | ₹20,000         |                |
| 7     | ₹40,000         |                |
| 8     | ₹80,000         |                |
| 9     | ₹1,60,000       |                |
| **10**| **₹3,20,000**   | 🛡️ Safe Haven  |
| 11    | ₹6,40,000       |                |
| 12    | ₹12,50,000      |                |
| 13    | ₹25,00,000      |                |
| 14    | ₹50,00,000      |                |
| **15**| **₹1,00,00,000**| 🏆 Grand Prize |

> **Safe Havens:** If you answer incorrectly after passing Level 5, you keep ₹10,000. After Level 10, you keep ₹3,20,000.

---

## 🆘 Lifelines

| Lifeline       | How It Works                                              |
|----------------|-----------------------------------------------------------|
| **50-50**      | Removes 2 incorrect options, leaving 1 wrong + 1 correct |
| **Skip**       | Replaces the current question with a different one        |
| **Audience Poll** | Shows a simulated % vote for each option (A/B/C/D)   |

Each lifeline can only be used **once per game session**.

---

## 🛠️ Admin Panel

Access at: **http://127.0.0.1:8000/admin/**

Login with your superuser credentials.

### What you can do:

**Questions**
- Add new questions with all 4 options and the correct answer
- Filter by level (1–15) or difficulty (easy/medium/hard)
- Search questions by text
- Edit or delete existing questions

**Game Sessions**
- View all player game sessions
- See lifelines used, level reached, and final score
- Filter by game status (active/won/lost/quit)
- Sessions are read-only to prevent tampering

**Users**
- View all registered users
- See total games played and personal best score per user
- Manage staff/superuser permissions

---

## 🖼️ Screenshots

> 
> 
| Page            | Description                          |
|-----------------|--------------------------------------|
| Home            | Landing page with prize preview      |
| Register/Login  | Auth forms with dark KBC theme       |
| Dashboard       | Stats, recent games, play button     |
| Game Screen     | Question, timer, lifelines, ladder   |
| Result Screen   | Win / Loss / Quit with final score   |
| Leaderboard     | Top 10 scores with medals            |
| Admin Panel     | Question management interface        |

---

## 🔧 Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic
```

Make sure `STATICFILES_DIRS` is set correctly in `settings.py`:
```python
STATICFILES_DIRS = [BASE_DIR / 'static']
```

### Migration errors — reset migrations
```bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations quiz
python manage.py migrate
```

### No questions in game
```bash
python manage.py seed_questions
```

### Port already in use
```bash
python manage.py runserver 8080
```
Then visit: http://127.0.0.1:8080/

### Forgot superuser password
```bash
python manage.py changepassword <username>
```

---

## 🚀 Future Enhancements

- [ ] Phone a Friend lifeline (simulated AI response)
- [ ] Category-based question sets (Science, History, Sports, etc.)
- [ ] Multiplayer / challenge a friend mode
- [ ] Email verification on registration
- [ ] Question import via CSV/Excel
- [ ] Animated transitions between levels
- [ ] Sound effects and background music
- [ ] Mobile app version using Django REST Framework + React Native
- [ ] PostgreSQL support for production deployment
- [ ] Docker containerization

---

## 📦 Dependencies

```
Django>=4.2,<5.0
```

All other dependencies (Bootstrap, Bootstrap Icons) are loaded via CDN in the base template.

---

## 👨‍💻 Author

**KBC-Quiz** — A College Academic Project

Built with ❤️ using **Django** + **Bootstrap 5**

---

## 📄 License

This project is licensed under the **MIT License** — free to use for educational purposes.

```
MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

> ⭐ If you found this project helpful, give it a star on GitHub!
