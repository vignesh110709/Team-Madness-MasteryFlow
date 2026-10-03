from fpdf import FPDF
import sys
import os

# Import the questions to automatically generate the curriculum pages
sys.path.append(os.getcwd())
try:
    import questions_db
except ImportError:
    questions_db = None

class ReportPDF(FPDF):
    def header(self):
        self.set_fill_color(10, 25, 47)
        self.rect(0, 0, 210, 15, 'F')
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(255, 255, 255)
        self.set_y(4)
        self.cell(0, 7, "MASTERYFLOW V2 - COMPREHENSIVE PROJECT REPORT", align="C")
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(14, 165, 233)
        self.cell(0, 10, title, ln=True)
        self.ln(4)
        
    def section_title(self, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(249, 115, 22)
        self.cell(0, 8, title, ln=True)
        self.ln(2)

    def body_text(self, text):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(40, 40, 40)
        # Sanitize text
        text = text.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 6, text)
        self.ln(4)

def generate_report():
    pdf = ReportPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # PAGE 1: TITLE & EXECUTIVE SUMMARY
    pdf.add_page()
    pdf.set_y(60)
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(10, 25, 47)
    pdf.cell(0, 15, "MASTERYFLOW V2", align="C", ln=True)
    pdf.set_font("Helvetica", "I", 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, "Comprehensive Project Documentation & Curriculum Analysis", align="C", ln=True)
    pdf.ln(30)
    
    pdf.chapter_title("1. Executive Summary")
    pdf.body_text("MasteryFlow V2 is a dual-purpose, premium digital ecosystem designed to revolutionize both education and event management. Built as a rapid prototype using Python and Streamlit, it demonstrates how complex, AI-driven applications can be engineered with extreme efficiency while maintaining a stunning, glassmorphism-based UI.")
    pdf.body_text("The platform is divided into two primary modules: The Adaptive Learning Engine and the Event Experience Platform. Together, they represent the convergence of secure, privacy-first data handling and engaging user experiences.")
    
    # PAGE 2: ADAPTIVE LEARNING ARCHITECTURE
    pdf.add_page()
    pdf.chapter_title("2. Adaptive Learning Engine Architecture")
    pdf.body_text("Unlike traditional 'black-box' educational AI, MasteryFlow V2 utilizes a strict 'Teacher-in-the-Loop' architecture. The system models knowledge using a prerequisite directed acyclic graph (DAG).")
    
    pdf.section_title("Zero-Knowledge & Privacy")
    pdf.body_text("Student data privacy is paramount. MasteryFlow proposes an End-to-End Encrypted (E2EE) data model using libsodium, meaning the server processes interactions without knowing the identity or the plaintext performance data of the student. All mastery states are calculated locally or within secure enclaves.")
    
    pdf.section_title("Dynamic Difficulty Adjustment")
    pdf.body_text("As students answer questions, their mastery score (from 0.0 to 1.0) is dynamically updated based on: \n- Correctness of the answer\n- Reported confidence level (1-5)\n- Time taken to respond\n- Utilization of hints\n\nIf a student struggles, the engine detects weak prerequisites and automatically suggests remedial questions before allowing progression.")

    # PAGE 3: EVENT PLATFORM
    pdf.add_page()
    pdf.chapter_title("3. Event Experience Platform")
    pdf.body_text("The second half of MasteryFlow V2 focuses on seamless event management. It replaces the need for 5 separate applications (invitations, ticketing, RSVPs, photo sharing, scheduling) with a single unified dashboard.")
    
    pdf.section_title("Features Breakdown")
    pdf.body_text("- AI Invitation Generator: Hosts input basic details, and the AI generates premium, themed invitation copy in multiple languages (English, Tamil, Tanglish).")
    pdf.body_text("- Cinematic Previews: Generates animated HTML/CSS trailers for events.")
    pdf.body_text("- Smart RSVP & QR Check-in: Hosts can generate personalized links. On the day of the event, a built-in QR scanner verifies tokens to prevent duplicate entries.")
    pdf.body_text("- Live Memory Wall: A dynamic photo gallery where guests can upload memories in real-time.")
    pdf.body_text("- Flow AI: A conversational assistant that answers guest queries about venue, parking, and scheduling using event context.")

    # PAGES 4+: CURRICULUM ANALYSIS
    if questions_db:
        subjects = ["Computer Science", "Biology", "Physics", "Chemistry", "Mathematics"]
        
        for subject in subjects:
            pdf.add_page()
            pdf.chapter_title(f"Detailed Curriculum: {subject}")
            pdf.body_text(f"The {subject} curriculum is fully integrated into the Adaptive Learning Engine. It consists of 15 carefully curated questions spanning Easy, Medium, and Difficult cognitive levels. Below is the detailed breakdown of the internal knowledge graph for this subject.")
            
            # Filter questions for this subject
            qs = [q for q in questions_db.Q if q[1] == subject]
            
            easy_qs = [q for q in qs if q[2] == 1]
            med_qs = [q for q in qs if q[2] == 3]
            diff_qs = [q for q in qs if q[2] == 4]
            
            pdf.section_title("Level 1: Foundation (Easy)")
            pdf.body_text("These questions focus on the recall of basic facts, definitions, and core principles. They serve as the baseline entry point for the adaptive algorithm.")
            for q in easy_qs:
                pdf.body_text(f"Q: {q[4]}")
                pdf.body_text(f"Options: {', '.join(q[5])}")
                pdf.body_text(f"Answer: {q[6]} | Rationale: {q[7]}\n")
                
            pdf.add_page()
            pdf.section_title("Level 2: Application (Medium)")
            pdf.body_text("These questions require students to apply formulas, perform simple calculations, or connect multiple foundational concepts.")
            for q in med_qs:
                pdf.body_text(f"Q: {q[4]}")
                pdf.body_text(f"Options: {', '.join(q[5])}")
                pdf.body_text(f"Answer: {q[6]} | Rationale: {q[7]}\n")
                
            pdf.add_page()
            pdf.section_title("Level 3: Mastery (Difficult)")
            pdf.body_text("These questions test deep multi-step reasoning, edge cases, and conceptual synthesis. The engine only serves these when prerequisite mastery exceeds 85%.")
            for q in diff_qs:
                pdf.body_text(f"Q: {q[4]}")
                pdf.body_text(f"Options: {', '.join(q[5])}")
                pdf.body_text(f"Answer: {q[6]} | Rationale: {q[7]}\n")
    else:
        pdf.add_page()
        pdf.chapter_title("Curriculum Analysis")
        pdf.body_text("Error: Could not load questions_db.py to generate curriculum analysis.")

    pdf.output("MasteryFlow_Detailed_Report.pdf")
    print("Report generated successfully.")

if __name__ == "__main__":
    generate_report()
