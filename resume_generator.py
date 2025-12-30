from fpdf import FPDF
from datetime import datetime
import os

# ---------- FIX 1: SAFE TEXT ----------
def clean_text(text: str) -> str:
    return (
        text.replace("•", "-")
            .replace("–", "-")
            .replace("—", "-")
            .encode("latin-1", "ignore")
            .decode("latin-1")
    )

# ---------- PDF CLASS ----------
class ResumePDF(FPDF):

    def header(self):
        self.set_fill_color(30, 144, 255)
        self.rect(0, 0, 210, 35, "F")

        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 22)
        self.set_xy(10, 12)
        self.cell(0, 10, clean_text(self.name), ln=True)

        self.set_font("Helvetica", "", 12)
        self.cell(0, 8, clean_text(self.job_role))
        self.ln(20)

    def section_title(self, title):
        self.set_text_color(30, 144, 255)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, clean_text(title), ln=True)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def section_body(self, text):
        self.set_text_color(40, 40, 40)
        self.set_font("Helvetica", "", 11)
        self.multi_cell(0, 8, clean_text(text))
        self.ln(2)

# ---------- MAIN FUNCTION ----------
def generate_resume(name, skills, experience, education, job_role):
    pdf = ResumePDF()
    pdf.name = name
    pdf.job_role = job_role

    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # PROFILE
    pdf.section_title("PROFILE SUMMARY")
    pdf.section_body(
        f"{job_role} with {experience} years of practical experience. "
        f"Strong foundation in {education}. Passionate about solving real-world "
        f"problems and building efficient, scalable systems."
    )

    # SKILLS
    pdf.section_title("TECHNICAL SKILLS")
    pdf.section_body(
        f"- Programming & Tools: {skills}\n"
        "- Technologies: Machine Learning, Data Analysis, APIs\n"
        "- Soft Skills: Communication, Adaptability, Problem Solving"
    )

    # EXPERIENCE
    pdf.section_title("PROFESSIONAL EXPERIENCE")
    pdf.section_body(
        "- Developed and deployed Python-based applications\n"
        "- Applied ML techniques for prediction and optimization\n"
        "- Worked on data preprocessing and feature engineering\n"
        "- Collaborated in team-based development environments"
    )

    # PROJECTS
    pdf.section_title("PROJECTS")
    pdf.section_body(
        "- Resume & Job Recommendation System (ML-based)\n"
        "- Real-time Analytics Dashboard\n"
        "- Predictive Models using supervised learning"
    )

    # EDUCATION
    pdf.section_title("EDUCATION")
    pdf.section_body(
        f"{education} Degree\n"
        "Specialization in Artificial Intelligence and Software Engineering"
    )

    # FOOTER
    pdf.ln(10)
    pdf.set_text_color(120, 120, 120)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(
        0,
        10,
        clean_text(f"Generated on {datetime.now().strftime('%d %B %Y')}"),
        align="C"
    )

    output_dir = "generated_resumes"
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{output_dir}/{name.replace(' ', '_')}_Resume.pdf"
    pdf.output(filename)

    return filename
