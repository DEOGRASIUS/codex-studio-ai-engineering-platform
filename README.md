# Codex Studio – AI Engineering Platform

Codex Studio is an AI-powered software engineering platform that guides software projects through a structured engineering workflow. Instead of relying on disconnected tools, the platform simulates a complete software engineering team where each AI engineer performs a specialized role in the development process.



## Overview

Codex Studio helps developers and teams transform software ideas into structured engineering deliverables. Each project progresses through multiple engineering stages, generating documentation and artifacts while maintaining approvals, feedback, and workflow history.



## Features

- User Authentication
- Project Creation and Management
- AI-Assisted Engineering Workflow
- Sequential Engineering Pipeline
- Approval and Review System
- AI-Generated Engineering Artifacts
- Project Dashboard
- Responsive User Interface



## Engineering Workflow

Every project passes through the following engineers:

1. Requirements Analyst
2. Project Manager
3. System Architect
4. UI/UX Designer
5. Database Engineer
6. Backend Engineer
7. Frontend Engineer
8. QA Engineer
9. Documentation Engineer

Each engineer generates outputs that become inputs for the next stage.


## Technology Stack

### Backend
- Python
- Django

### Frontend
- HTML
- CSS
- JavaScript

### Database
- SQLite (Development)

### AI
- Google Gemini API

### Deployment
- Render
- WhiteNoise

### Version Control
- Git
- GitHub


##  Project Structure

accounts/
agents/
config/
projects/
static/
templates/
media/
requirements.txt
manage.py
README.md


## Installation

Clone the repository:

```bash
git clone https://github.com/DEOGRASIUS/codex-studio-ai-engineering-platform.git
```

Navigate into the project:

```bash
cd codex-studio-ai-engineering-platform
```

Create a virtual environment:

```bash
python -m venv deo_studio
```

Activate it:

Windows

```bash
deo_studio\Scripts\activate
```

Linux/macOS

```bash
source deo_studio/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file.

Example:

```text
SECRET_KEY=your_secret_key
DEBUG=True
AI_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key
```

Run migrations:

```bash
python manage.py migrate
```

Collect static files:

```bash
python manage.py collectstatic
```

Run the development server:

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000
```

---

## Live Demo

Deployed on Render.
```
https://codex-studio-ai-engineering-platform.onrender.com
```


##  Future Improvements

- OpenAI support
- Anthropic Claude support
- Multi-agent collaboration
- Code generation
- GitHub integration
- Architecture diagrams
- Sprint planning
- CI/CD generation
- Team collaboration
- PDF export
- Word export


## 👨‍💻 Author

**Deograsius Obalim**

Software Engineering Student

GitHub:
https://github.com/DEOGRASIUS/codex-studio-ai-engineering-platform.git

---

## License

This project was developed as part of a hackathon submission and is available for educational purposes.