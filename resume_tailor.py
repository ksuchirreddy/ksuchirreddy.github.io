#!/usr/bin/env python3
"""
Automated Dynamic Resume Tailoring Engine for K. Suchir Reddy
Generates ATS-optimized, high-impact tailored PDF resumes for each target company/domain
without altering project truth or core facts.
"""

import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent
RESUMES_DIR = BASE_DIR / "resumes"
RESUMES_DIR.mkdir(parents=True, exist_ok=True)

# Master Profile Data
CANDIDATE = {
    "name": "K. Suchir Reddy",
    "email": "ksuchirreddy@gmail.com",
    "phone": "+91 7899597757",
    "location": "Bengaluru, Karnataka, India",
    "linkedin": "https://linkedin.com/in/ksuchirreddy",
    "github": "https://github.com/ksuchirreddy",
    "portfolio": "https://ksuchirreddy.github.io",
    "education": {
        "degree": "Bachelor of Engineering (B.E.) — Computer Science & Business Systems",
        "institution": "Dayananda Sagar College of Engineering (DSCE), Bengaluru",
        "year": "4th Year Undergraduate (Batch 2026)",
        "cpi": "8.15 / 10.0"
    }
}

PROJECTS_DATA = {
    "ast": {
        "title": "Multi-Model Code Generation & Benchmarking Engine",
        "tech": "Python, PyTorch, Transformers, AST (Abstract Syntax Trees), Evaluation Metrics",
        "bullets": [
            "Built an automated evaluation pipeline measuring LLM-generated code across runtime latency, memory, and syntactic correctness.",
            "Utilized Abstract Syntax Tree (AST) parsing in Python to validate grammatical code structures without execution overhead.",
            "Benchmarked multi-model inference performance across varied prompt complexities with structured JSON logging."
        ]
    },
    "traffic_cv": {
        "title": "Adaptive Traffic Signal Optimization using Computer Vision",
        "tech": "Python, OpenCV, YOLO, Real-Time Video Streams, Dynamic Scheduling",
        "bullets": [
            "Developed real-time vehicle density detection from multi-camera feeds using OpenCV and YOLO to dynamically adjust green signal timing.",
            "Designed low-latency image processing pipelines reducing simulated intersection bottlenecks and waiting delays.",
            "Structured robust video stream preprocessing and bounding-box telemetry for dynamic signal phase allocation."
        ]
    },
    "content_moderator": {
        "title": "AI Content Moderator & Social Platform",
        "tech": "Python, Flask, FastAPI, NLP, MySQL, Scikit-learn, REST APIs",
        "bullets": [
            "Engineered high-throughput REST APIs in Flask/FastAPI for automated real-time text toxicity classification and content filtering.",
            "Architected relational MySQL database schemas managing user profiles, flagged content queues, and audit logs.",
            "Built responsive web interfaces with complete frontend-to-backend data flow and validation."
        ]
    }
}

def generate_resume_html(company: str, role: str, domain: str, prioritized_skills: list, summary_focus: str, project_order: list) -> str:
    # Build skills string
    skills_html = ""
    for category, items in prioritized_skills:
        skills_html += f"<div class='skill-row'><strong>{category}:</strong> {', '.join(items)}</div>"

    # Build projects HTML
    projects_html = ""
    for p_key in project_order:
        proj = PROJECTS_DATA[p_key]
        bullets_html = "".join([f"<li>{b}</li>" for b in proj["bullets"]])
        projects_html += f"""
        <div class="project-item">
            <div class="project-header">
                <span class="project-title">{proj['title']}</span>
                <span class="project-tech">[{proj['tech']}]</span>
            </div>
            <ul class="project-bullets">
                {bullets_html}
            </ul>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    @page {{
        size: A4;
        margin: 12mm 14mm 12mm 14mm;
    }}
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}
    body {{
        font-family: 'Helvetica Neue', Arial, sans-serif;
        color: #1a202c;
        line-height: 1.35;
        font-size: 9.8pt;
    }}
    .header {{
        text-align: center;
        border-bottom: 2px solid #2b6cb0;
        padding-bottom: 6px;
        margin-bottom: 10px;
    }}
    .name {{
        font-size: 19pt;
        font-weight: 800;
        letter-spacing: 0.5px;
        color: #1a365d;
        text-transform: uppercase;
    }}
    .tagline {{
        font-size: 10pt;
        font-weight: 600;
        color: #2b6cb0;
        margin-top: 2px;
    }}
    .contact-bar {{
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 4px;
        font-size: 8.8pt;
        color: #4a5568;
    }}
    .contact-bar a {{
        color: #2b6cb0;
        text-decoration: none;
    }}
    .section-title {{
        font-size: 10.5pt;
        font-weight: 800;
        text-transform: uppercase;
        color: #1a365d;
        border-bottom: 1px solid #cbd5e0;
        padding-bottom: 2px;
        margin-top: 9px;
        margin-bottom: 5px;
        letter-spacing: 0.4px;
    }}
    .summary-text {{
        font-size: 9.3pt;
        color: #2d3748;
        text-align: justify;
    }}
    .education-item {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 2px;
    }}
    .edu-inst {{
        font-weight: 700;
        color: #2d3748;
    }}
    .edu-degree {{
        font-size: 9.2pt;
        color: #4a5568;
    }}
    .edu-cpi {{
        font-weight: 700;
        color: #2b6cb0;
    }}
    .skill-row {{
        margin-bottom: 3px;
        font-size: 9.2pt;
    }}
    .skill-row strong {{
        color: #2d3748;
    }}
    .project-item {{
        margin-bottom: 7px;
    }}
    .project-header {{
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 2px;
    }}
    .project-title {{
        font-weight: 700;
        color: #2b6cb0;
        font-size: 9.6pt;
    }}
    .project-tech {{
        font-size: 8.2pt;
        color: #718096;
        font-family: monospace;
    }}
    .project-bullets {{
        padding-left: 16px;
    }}
    .project-bullets li {{
        margin-bottom: 2px;
        font-size: 9.1pt;
        color: #2d3748;
    }}
    .tailor-badge {{
        font-size: 7.5pt;
        color: #a0aec0;
        text-align: right;
        margin-top: 4px;
    }}
</style>
</head>
<body>

<div class="header">
    <div class="name">{CANDIDATE['name']}</div>
    <div class="tagline">{role} · {domain}</div>
    <div class="contact-bar">
        <span>📍 {CANDIDATE['location']}</span>
        <span>📞 {CANDIDATE['phone']}</span>
        <span>✉️ <a href="mailto:{CANDIDATE['email']}">{CANDIDATE['email']}</a></span>
        <span>🌐 <a href="{CANDIDATE['portfolio']}">ksuchirreddy.github.io</a></span>
        <span>💻 <a href="{CANDIDATE['github']}">GitHub</a></span>
        <span>🔗 <a href="{CANDIDATE['linkedin']}">LinkedIn</a></span>
    </div>
</div>

<div class="section-title">Professional Summary</div>
<div class="summary-text">
    {summary_focus}
</div>

<div class="section-title">Education</div>
<div class="education-item">
    <div>
        <div class="edu-inst">{CANDIDATE['education']['institution']}</div>
        <div class="edu-degree">{CANDIDATE['education']['degree']}</div>
    </div>
    <div style="text-align: right;">
        <div class="edu-cpi">CPI: {CANDIDATE['education']['cpi']}</div>
        <div style="font-size: 8.5pt; color: #718096;">{CANDIDATE['education']['year']}</div>
    </div>
</div>

<div class="section-title">Technical Skills</div>
{skills_html}

<div class="section-title">Key Engineering Projects</div>
{projects_html}

<div class="section-title">Leadership & Academic Mentorship</div>
<div style="font-size: 9.1pt; color: #2d3748;">
    <strong>AI Enthusiast & Peer Mentor (DSCE):</strong> Hosted hands-on mentoring sessions for engineering peers, guiding students through practical machine learning workflows, algorithms, and clean production code practices.
</div>

<div class="tailor-badge">Tailored for {company} · K. Suchir Reddy Portfolio Profile</div>

</body>
</html>
"""
    return html

def build_all_tailored_resumes():
    target_configs = [
        {
            "filename": "Suchir_Resume_IBM.pdf",
            "company": "IBM India",
            "role": "Software Developer Intern",
            "domain": "Backend & Systems",
            "summary": "4th-year Computer Science undergraduate at DSCE (CPI: 8.15) with solid foundations in software systems, algorithms, and clean architecture in Python, C++, Java, and SQL. Practical experience building AST syntax analysis pipelines and modular REST APIs.",
            "skills": [
                ("Languages", ["Python (Advanced)", "Java", "C++", "C", "SQL"]),
                ("Systems & Backend", ["Flask", "FastAPI", "RESTful APIs", "MySQL", "DBMS", "AST Parsing"]),
                ("Tools & Frameworks", ["Git / GitHub", "Docker (Basics)", "AWS S3", "Linux", "PyTorch"])
            ],
            "project_order": ["ast", "content_moderator", "traffic_cv"]
        },
        {
            "filename": "Suchir_Resume_SarvamAI.pdf",
            "company": "Sarvam AI",
            "role": "AI/ML Engineer Intern",
            "domain": "LLMs & PyTorch",
            "summary": "4th-year CS student at DSCE (CPI: 8.15) specializing in deep learning, LLMs, and model evaluation. Built automated AST benchmarking pipelines in PyTorch evaluating code generation quality, runtime latency, and syntactic validity.",
            "skills": [
                ("AI / Deep Learning", ["PyTorch", "Transformers", "LLM Evaluation", "AST Analysis", "Scikit-learn"]),
                ("Languages & Libraries", ["Python (Advanced)", "NumPy", "Pandas", "SQL", "C++"]),
                ("Backend & Tools", ["Flask", "FastAPI", "MySQL", "Git / GitHub", "Linux"])
            ],
            "project_order": ["ast", "traffic_cv", "content_moderator"]
        },
        {
            "filename": "Suchir_Resume_MerakiLabs.pdf",
            "company": "Meraki Labs",
            "role": "Computer Vision Intern",
            "domain": "OpenCV & Video Analytics",
            "summary": "4th-year CS undergraduate at DSCE (CPI: 8.15) experienced in real-time computer vision and image processing with OpenCV and YOLO. Engineered vehicle density detection pipelines from multi-camera feeds for dynamic traffic signal control.",
            "skills": [
                ("Computer Vision", ["OpenCV", "YOLO", "Video Stream Processing", "Object Detection", "Bounding Box Analysis"]),
                ("Machine Learning", ["PyTorch", "Scikit-learn", "NumPy", "Pandas", "Model Benchmarking"]),
                ("Languages & Systems", ["Python (Advanced)", "C++", "Flask", "Git / GitHub", "Linux"])
            ],
            "project_order": ["traffic_cv", "ast", "content_moderator"]
        },
        {
            "filename": "Suchir_Resume_MerkleScience.pdf",
            "company": "Merkle Science",
            "role": "Backend Engineering Intern",
            "domain": "Python & Relational Databases",
            "summary": "4th-year CS student at DSCE (CPI: 8.15) skilled in backend engineering, relational database schema design, and high-throughput Python REST APIs with MySQL, Flask, and FastAPI.",
            "skills": [
                ("Backend & Databases", ["Python", "MySQL", "PostgreSQL", "Flask", "FastAPI", "RESTful Architecture"]),
                ("Data & Pipelines", ["Pandas", "NumPy", "SQL Query Optimization", "ETL Pipelines", "AWS S3"]),
                ("Core Engineering", ["C++", "Java", "Git / GitHub", "Data Structures", "Linux"])
            ],
            "project_order": ["content_moderator", "ast", "traffic_cv"]
        },
        {
            "filename": "Suchir_Resume_MPL.pdf",
            "company": "MPL (Mobile Premier League)",
            "role": "Data Engineer Intern",
            "domain": "ETL, SQL & Data Modeling",
            "summary": "4th-year CS undergraduate at DSCE (CPI: 8.15) experienced in Python data pipelines (Pandas, NumPy), complex SQL querying, and relational data architecture with AWS S3 telemetry ingestion.",
            "skills": [
                ("Data Engineering", ["SQL", "Pandas", "NumPy", "ETL Pipelines", "Data Modeling", "AWS S3"]),
                ("Languages & Analytics", ["Python (Advanced)", "Power BI", "MySQL", "C++", "Scikit-learn"]),
                ("Backend & Infrastructure", ["Flask", "FastAPI", "Git / GitHub", "Linux", "REST APIs"])
            ],
            "project_order": ["content_moderator", "ast", "traffic_cv"]
        },
        {
            "filename": "Suchir_Resume_Fractal.pdf",
            "company": "Fractal Analytics",
            "role": "Software & Data Trainee Engineer",
            "domain": "Systems & Analytical Engineering",
            "summary": "4th-year CS student at DSCE (CPI: 8.15) with strong fundamentals in data structures, algorithms, and modular Python/Java engineering. Practical background in ML benchmarking and relational databases.",
            "skills": [
                ("Languages & Core CS", ["Python (Advanced)", "Java", "C++", "SQL", "Data Structures & Algorithms"]),
                ("Analytics & ML", ["Pandas", "NumPy", "Scikit-learn", "Power BI", "PyTorch"]),
                ("Systems & Databases", ["MySQL", "Flask", "REST APIs", "Git / GitHub", "Linux"])
            ],
            "project_order": ["ast", "content_moderator", "traffic_cv"]
        },
        {
            "filename": "Suchir_Resume_Flexio.pdf",
            "company": "Flexio",
            "role": "Python Full-Stack Developer Intern",
            "domain": "APIs & Web Platforms",
            "summary": "4th-year CS undergraduate at DSCE (CPI: 8.15) building full-stack web applications with Python backends (Flask/FastAPI), relational MySQL databases, and clean frontend integrations.",
            "skills": [
                ("Full-Stack & APIs", ["Python", "Flask", "FastAPI", "REST APIs", "MySQL", "HTML5", "CSS3", "JavaScript"]),
                ("Data & AI", ["Scikit-learn", "NLP", "Pandas", "NumPy", "Model Inference"]),
                ("Engineering Practices", ["Git / GitHub", "Clean Architecture", "Linux", "Testing & Debugging"])
            ],
            "project_order": ["content_moderator", "ast", "traffic_cv"]
        }
    ]

    print(f"🚀 Generating {len(target_configs)} Tailored PDF Resumes...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for cfg in target_configs:
            out_pdf = RESUMES_DIR / cfg["filename"]
            html_content = generate_resume_html(
                company=cfg["company"],
                role=cfg["role"],
                domain=cfg["domain"],
                prioritized_skills=cfg["skills"],
                summary_focus=cfg["summary"],
                project_order=cfg["project_order"]
            )
            
            page.set_content(html_content, wait_until="networkidle")
            page.pdf(
                path=str(out_pdf),
                format="A4",
                print_background=True,
                margin={"top": "10mm", "bottom": "10mm", "left": "12mm", "right": "12mm"}
            )
            print(f"✅ Generated: {out_pdf.name} for {cfg['company']} ({cfg['role']})")

        browser.close()

    print(f"\n🎉 All {len(target_configs)} Tailored Resumes successfully compiled in {RESUMES_DIR}!")

if __name__ == "__main__":
    build_all_tailored_resumes()
