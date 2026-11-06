# 📰 The AI Times

### Your Daily Source for Artificial Intelligence News

**The AI Times** is an AI-focused news aggregation platform that collects, filters, and organizes the latest news and developments from the world of Artificial Intelligence.

The platform helps users stay updated on important developments in AI, Machine Learning, Deep Learning, Generative AI, Large Language Models, Robotics, and other emerging technologies.

Instead of browsing multiple news websites, users can explore AI-related news through a single platform with category-based filtering and personalized interests.

---

## ✨ Features

- **AI News Aggregation:** Fetches AI-related news articles using the NewsAPI.
- **Smart AI Filtering:** Filters articles based on relevant AI keywords and topics.
- **Category-Based Browsing:** Explore news across different AI domains.
- **User Authentication:** Registration, login, logout, and account management.
- **OTP Verification:** Email-based OTP verification during authentication workflows.
- **Personalized Interests:** Users can select their preferred AI topics.
- **Saved Articles:** Save interesting articles and access them later.
- **Automatic News Updates:** Scheduled news fetching using APScheduler.
- **Article Deduplication:** Prevents duplicate articles from being stored.
- **Responsive Web Interface:** Browse news through a web-based interface.

## 🧠 AI News Categories

The platform organizes articles into the following categories:

1. Artificial Intelligence
2. Machine Learning
3. Deep Learning
4. Generative AI
5. Large Language Models (LLMs)
6. Natural Language Processing (NLP)
7. Robotics & Automation
8. AI Research
9. Open Source AI
10. Coding Assistants

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| Flask-SQLAlchemy | Database management |
| HTML5 | Web page structure |
| CSS3 | Styling and layout |
| JavaScript | Frontend interactions |
| NewsAPI | Fetching news articles |
| APScheduler | Automated news updates |
| Authlib | Authentication integration |
| Requests | API communication |
| Python-dotenv | Environment variable management |
| Gunicorn | Production WSGI server |

## 📂 Project Structure

```text
The-AI-times/
│
├── data/
│   ├── data.py
│   └── interests.json
│
├── models/
│   ├── article.py
│   └── user.py
│
├── routes/
│   ├── auth.py
│   └── user.py
│
├── services/
│   ├── auth_service.py
│   ├── news_service.py
│   ├── otp_service.py
│   └── user_service.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│
├── utils/
│
├── .env.example
├── .gitignore
├── app.py
├── config.py
├── database.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation & Setup

Follow these steps to run The AI Times locally.

### 1. Clone the Repository

```bash
git clone https://github.com/rathodmilandipsinh-ui/The-AI-times.git
```

### 2. Navigate to the Project Directory

```bash
cd The-AI-times
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory.

Add the required configuration:

```env
SECRET_KEY=your_secret_key
DB_URL=your_database_connection_string
NEWSAPI_KEY=your_newsapi_key
MAIL_EMAIL=your_email_address
MAIL_PASSWORD=your_email_app_password
```

Replace the placeholder values with your actual credentials.

**Important:**
- Obtain your NewsAPI key from [NewsAPI](https://newsapi.org/).
- Configure a valid database connection string.
- Use an email app password where required.
- Never upload your `.env` file or expose API keys and passwords on GitHub.

### 6. Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

## 🔄 How It Works

The AI Times follows a simple news aggregation workflow:

1. The application sends AI-related search queries to NewsAPI.
2. News articles are retrieved from the API.
3. Articles are checked using keyword-based AI relevance filtering.
4. Relevant articles are categorized according to their topics.
5. Duplicate articles and articles without images are excluded.
6. Valid articles are stored in the configured database.
7. Users browse and filter the collected articles through the website.
8. APScheduler automatically triggers news fetching every 24 hours.

## 🔐 Security & Configuration

- Sensitive credentials are managed through environment variables.
- User authentication is handled through dedicated authentication services.
- Password handling uses secure password hashing mechanisms.
- The application uses Flask session management.
- Database configuration is maintained separately from application logic.

**Never commit API keys, email passwords, database credentials, or other secrets to the repository.**

## 🚀 Future Improvements

Potential improvements for future versions include:

- AI-powered article summarization.
- Advanced news recommendation systems.
- Improved search and filtering functionality.
- More AI technology categories.
- User notification system for important AI developments.
- Enhanced dashboard and analytics.
- Improved deployment and scalability.

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork this repository.
2. Create a new branch.
3. Make your changes.
4. Commit your changes.
5. Submit a Pull Request.

## 👨‍💻 Project Information

**Project Name:** The AI Times  
**Project Type:** Minor Project / Academic Project  
**Domain:** Artificial Intelligence & Web Development  
**Backend:** Python Flask  
**Repository:** [The AI Times on GitHub](https://github.com/rathodmilandipsinh-ui/The-AI-times)

## 📄 License

This project is developed for educational and learning purposes. Please contact the repository owner regarding reuse and distribution permissions.

---

<p align="center">
  <b>The AI Times</b><br>
  Stay Updated. Stay Informed. Stay Ahead in AI.
</p>
