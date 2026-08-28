import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
RESUME_PATH = BASE_DIR / "Suchir_Resume.pdf"
DASHBOARD_PATH = BASE_DIR / "dashboard.html"
BROWSER_PROFILE_DIR = BASE_DIR / ".browser_profile"

# Candidate Profile (Loaded from CLAUDE.md)
CANDIDATE = {
    "full_name": "K. Suchir Reddy",
    "first_name": "Suchir",
    "last_name": "Reddy",
    "email": "ksuchirreddy@gmail.com",
    "phone": "+91 7899597757",
    "location": "Bengaluru, Karnataka, India",
    "city": "Bengaluru",
    "state": "Karnataka",
    "country": "India",
    "linkedin": "https://linkedin.com/in/ksuchirreddy",
    "github": "https://github.com/ksuchirreddy",
    "portfolio": "https://ksuchirreddy.github.io",
    "education": {
        "degree": "Bachelor of Engineering (B.E.) — 4th Year Undergraduate",
        "current_year": "4th Year (Final Year)",
        "institution": "Dayananda Sagar College of Engineering (DSCE), Bengaluru",
        "field_of_study": "Computer Science & Engineering",
        "start_year": "2022",
        "graduation_year": "2026",
        "cpi": "8.15",
        "cpi_max": "10.0",
    },
    "projects": {
        "ast_benchmarking": {
            "title": "Multi-Model Code Generation & Benchmarking Engine",
            "skills": "Python, PyTorch, Transformers, AST Analysis",
            "description": "Built an automated benchmarking pipeline in Python and PyTorch evaluating LLM-generated code. Analyzed syntactic validity with Abstract Syntax Trees (AST) and benchmarked execution latency and memory overhead across models.",
        },
        "traffic_cv": {
            "title": "Adaptive Traffic Signal Optimization using Computer Vision",
            "skills": "Python, OpenCV, YOLO, Real-Time Video Processing",
            "description": "Engineered real-time vehicle density detection on live video feeds to dynamically adjust green signal timing, eliminating traffic congestion.",
        },
        "content_moderator": {
            "title": "AI Content Moderator & Social Platform",
            "skills": "Python, NLP, TensorFlow, MySQL, Scikit-learn, Flask",
            "description": "Developed an end-to-end NLP classification pipeline for toxicity detection connected to a MySQL relational database with Flask REST APIs.",
        },
        "mentorship": {
            "title": "AI Enthusiast & Peer Mentor",
            "duration": "Jan 2025 – Present",
            "description": "Guided students on ML model architectures, algorithms, and clean-code practices.",
        }
    }
}

# Email Notification Settings
EMAIL_CONFIG = {
    "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    "smtp_port": int(os.getenv("SMTP_PORT", 587)),
    "sender_email": os.getenv("SENDER_EMAIL", "ksuchirreddy@gmail.com"),
    "sender_password": os.getenv("SENDER_PASSWORD", ""),  # App Password or token
    "recipient_email": os.getenv("RECIPIENT_EMAIL", "ksuchirreddy@gmail.com"),
    "notify_on_auth_required": True,
    "notify_on_submission": True,
}
