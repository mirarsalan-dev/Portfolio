import os
import io
import requests
from flask import Blueprint, render_template, send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from flask import jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    # --- Your existing GitHub API Logic remains exactly the same ---
    github_username = "mirarsalan-dev" 
    url = f"https://api.github.com/users/mirarsalan-dev/repos"
    github_token = os.getenv('GITHUB_TOKEN')
    
    headers = {}
    if github_token:
        headers['Authorization'] = f'token {github_token}'
    
    try:
        params = {'sort': 'updated', 'direction': 'desc'}
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status() 
        repos = response.json()
        repos = [repo for repo in repos if not repo['fork']]
    except requests.RequestException as e:
        print(f"Error fetching GitHub repos: {e}")
        repos = [] 

    return render_template('index.html', projects=repos)

@main_bp.app_errorhandler(404)
def page_not_found(e):
    # render a template specifically for 404s
    return render_template('404.html'), 404

# --- NEW: Dynamic Resume Generation Route ---
@main_bp.route('/download-resume')
def download_resume():
    # Create an in-memory buffer to hold the PDF
    buffer = io.BytesIO()
    
    # Setup the Document layout
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    Story = []
    styles = getSampleStyleSheet()

    # Define Custom Styles for a premium look
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=24, spaceAfter=14)
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=16, spaceAfter=10, textColor=colors.HexColor('#2563eb'))
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=11, spaceAfter=8, leading=16)

    # 1. Header Section
    Story.append(Paragraph("<b>Arsalan Mir</b>", title_style))
    Story.append(Paragraph("Full-Stack Developer | Python, Java, Flask, Flet", body_style))
    Story.append(Paragraph("Nala Sopara, Maharashtra | mirarsalan2006@gmail.com | https://api.github.com/users/mirarsalan-dev/", body_style))
    Story.append(Spacer(1, 16))

    # 2. Profile Summary
    Story.append(Paragraph("Profile Summary", heading_style))
    Story.append(Paragraph("Information Technology Engineering student and independent full-stack developer. Passionate about engineering robust backend architectures and premium user interfaces, bridging scalable logic with seamless aesthetics.", body_style))
    Story.append(Spacer(1, 16))

    # 3. Tech Arsenal
    Story.append(Paragraph("Tech Arsenal", heading_style))
    Story.append(Paragraph("<b>Core Backend & Logic:</b> Python, Java, Flask, Socket Programming", body_style))
    Story.append(Paragraph("<b>Data & Cloud:</b> Firebase RTDB, SQL, JSON Protocols", body_style))
    Story.append(Paragraph("<b>Frontend & UI:</b> HTML/CSS, Tailwind, Flet (Python UI), Java Swing", body_style))
    Story.append(Spacer(1, 16))

    # 4. Engineering Journey & Education
    Story.append(Paragraph("Engineering Journey", heading_style))
    Story.append(Paragraph("<b>Independent Full-Stack Developer</b> (2024 - Present)", body_style))
    Story.append(Paragraph("Designing and engineering custom solutions for clients. Built dynamic business platforms like Ultra Fitness Center and developed comprehensive desktop network applications utilizing pure Java Socket Programming.", body_style))
    Story.append(Spacer(1, 10))
    
    Story.append(Paragraph("<b>B.E. Information Technology</b> (In Progress)", body_style))
    Story.append(Paragraph("Theem College of Engineering", body_style))
    Story.append(Paragraph("Specializing in software engineering, backend architectures, and database management. Developed a role-based Academic Grade System with Firebase integration and automated PDF report generation.", body_style))
    Story.append(Spacer(1, 16))

    # Build the PDF into the buffer
    doc.build(Story)
    
    # Move the buffer's position back to the beginning so it can be read
    buffer.seek(0)

    # Send the dynamically generated file to the user
    return send_file(
        buffer,
        as_attachment=True,
        download_name='Arsalan_Mir_Resume.pdf',
        mimetype='application/pdf'
    )

@main_bp.route('/api/github-activity')
@main_bp.route('/api/github-activity')
def github_activity():
    github_username = "mirarsalan-dev"
    # FIX: Dropped '/public' to allow private commits, added '?per_page=100' for maximum history
    url = f"https://api.github.com/users/{github_username}/events?per_page=100"
    github_token = os.getenv('GITHUB_TOKEN')
    
    headers = {}
    if github_token:
        headers['Authorization'] = f'token {github_token}'
        
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        print(f"Error fetching GitHub events: {e}")
        return jsonify([])
        
# --- NEW: Public Resume API Route ---
@main_bp.route('/api/resume')
def api_resume():
    """Returns a JSON payload of the developer's resume."""
    resume_data = {
        "developer": "Arsalan Mir",
        "status": "Available for opportunities",
        "location": "Maharashtra, India",
        "education": {
            "degree": "B.E. Information Technology",
            "institution": "Theem College of Engineering",
            "status": "In Progress"
        },
        "tech_stack": {
            "backend": ["Python", "Java", "Flask", "Socket Programming"],
            "frontend": ["HTML/CSS", "Tailwind", "Flet", "Java Swing"],
            "database": ["Firebase RTDB", "SQL", "JSON Protocols"]
        },
        "recent_roles": [
            {
                "title": "Frontend Development Intern",
                "company": "CodeAlpha",
                "date": "July 2026"
            },
            {
                "title": "Web Developer Intern",
                "company": "Codec Technologies",
                "date": "Dec 2025 - Jan 2026"
            }
        ],
        "message": "Send a POST request to https://formspree.io/f/xpqbjqqp to get in touch."
    }
    
    # jsonify automatically sets the correct application/json headers
    return jsonify(resume_data)

@main_bp.route('/uses')
def uses():
    return render_template('uses.html')