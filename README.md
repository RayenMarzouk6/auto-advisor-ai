# 🧠 AutoAdvisor – AI-Powered Business Strategy Assistant

**AutoAdvisor** is an AI-powered assistant that transforms raw business ideas into **validated, actionable strategies**.
It leverages **advanced language models** and **autonomous AI agents** to rephrase ideas, analyze feasibility, and generate a **comprehensive strategic report**, including **SWOT analysis** and recommendations.

---

## 🚀 Features

* 🛠️ **Model Selection** – Choose the desired version of Google's **Gemini AI models**.
* ✅ **LLM Validation** – Automatically checks if your input is a valid business idea.
* ♻️ **Auto-Correction** – Rephrases unclear or incomplete ideas into well-defined business concepts.
* 🧠 **Autonomous Agent Workflow** – Specialized AI agents collaborate to analyze and refine business ideas.
* 🔍 **Real-Time Web Search** – Agents use live web data via **SerperAPI** for up-to-date insights.
* 📊 **SWOT Analysis** – Identifies *Strengths, Weaknesses, Opportunities,* and *Threats* for your idea.
* 📄 **PDF Export** – Generates Unicode-compatible PDF reports for offline sharing or printing.
* 🌐 **Streamlit Web Interface** – Clean and intuitive UI for entrepreneurs and business strategists.

---

## 🧩 Tech Stack

| Technology            | Purpose                          |
| --------------------- | -------------------------------- |
| **Python 3.11+**      | Main programming language        |
| **Streamlit**         | Interactive web interface        |
| **LangChain**         | LLM orchestration framework      |
| **Google Gemini API** | AI model for strategy generation |
| **CrewAI / LiteLLM**  | Optional agent coordination      |
| **SerperAPI**         | Real-time web search integration |
| **MarkdownPDF**       | PDF report generation            |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/auto-advisor-ai.git
cd auto-advisor-ai
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Add Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-1.5-flash
```

---

## ▶️ Run the Application

Launch the Streamlit app:

```bash
streamlit run main.py
```

Then open your browser at **[http://localhost:8501](http://localhost:8501)**

---

## 📁 Project Structure

```
auto-advisor-ai/
│
├── build_agents.py        # AI agent creation and validation logic
├── main.py                # Streamlit app entry point
├── reports/               # Generated PDF reports
├── requirements.txt       # Dependencies
├── .env                   # Environment variables (not pushed to GitHub)
├── .gitignore             # Ignored files
└── README.md              # Documentation
```

---

## 🧠 How It Works

1. The user submits a **business idea** via the Streamlit interface.
2. The system validates and reformulates the idea using **Gemini AI**.
3. Multiple **AI agents** analyze the idea’s potential and generate insights.
4. A **strategic report** (including SWOT analysis) is compiled and exported as PDF.

---

## 📜 License

This project is released under the **MIT License**.
Feel free to use, modify, and distribute with proper attribution.

---

## 💬 Author

Developed by **Rayen Marzouk**
🎓 IT Student | 💡 Passionate about AI, Software Development, and Innovation
🔗 [Linkedin Profile](https://www.linkedin.com/in/rayen-marzouk-109a3226a/)

---
