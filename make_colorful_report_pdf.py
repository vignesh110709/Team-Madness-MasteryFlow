from fpdf import FPDF
import sys, os

sys.path.append(os.getcwd())
try:
    import questions_db
except ImportError:
    questions_db = None

class PremiumReportPDF(FPDF):
    def header(self):
        # Dark Background
        self.set_fill_color(10, 25, 47)
        self.rect(0, 0, 210, 297, 'F')
        
        # Header strip
        self.set_fill_color(249, 115, 22) # Orange strip
        self.rect(0, 0, 210, 2, 'F')
        
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(14, 165, 233)
        self.set_y(8)
        self.cell(0, 10, "MASTERYFLOW V2 - PREMIUM CURRICULUM REPORT", align="C")
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(136, 146, 176)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def page_title(self, title):
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(249, 115, 22) # Orange
        self.cell(0, 15, title, align="C", ln=True)
        self.ln(5)

    def chapter_title(self, title):
        self.set_fill_color(17, 34, 64)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(14, 165, 233) # Light Blue
        self.cell(0, 12, f"  {title}", fill=True, ln=True)
        self.ln(4)
        
    def section_title(self, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(250, 204, 21) # Yellow for sections
        self.cell(0, 8, title, ln=True)
        self.ln(2)

    def body_text(self, text):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(226, 232, 240)
        text = text.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(190, 6, text)
        self.ln(4)
        
    def question_block(self, q_text, options, answer, rationale):
        # Draw a highlighted box for the question
        self.set_fill_color(17, 34, 64) # Dark blue block
        
        # Question text
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(248, 250, 252)
        q_clean = q_text.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(190, 7, f"Q: {q_clean}", fill=True)
        
        # Options
        self.set_font("Helvetica", "I", 10)
        self.set_text_color(148, 163, 184)
        opt_clean = options.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(190, 6, f"Options: {opt_clean}", fill=True)
        
        # Answer & Rationale
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(56, 189, 248) # Bright blue for answer
        ans_clean = answer.encode('latin-1', 'replace').decode('latin-1')
        rat_clean = rationale.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(190, 6, f"Answer: {ans_clean}", fill=True)
        
        self.set_font("Helvetica", "", 10)
        self.set_text_color(167, 243, 208) # Mint green for rationale
        self.multi_cell(190, 6, f"Rationale: {rat_clean}", fill=True)
        self.ln(4)

def generate_report():
    pdf = PremiumReportPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # PAGE 1: TITLE & EXECUTIVE SUMMARY
    pdf.add_page()
    pdf.set_y(80)
    pdf.page_title("MASTERYFLOW V2")
    pdf.set_font("Helvetica", "I", 14)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 10, "Premium Curriculum Analysis & Documentation", align="C", ln=True)
    pdf.ln(30)
    
    pdf.chapter_title("1. Executive Summary")
    pdf.body_text("MasteryFlow V2 is a dual-purpose, premium digital ecosystem designed to revolutionize both education and event management. Built as a rapid prototype using Python and Streamlit, it demonstrates how complex, AI-driven applications can be engineered with extreme efficiency while maintaining a stunning, glassmorphism-based UI.")
    
    # PAGE 2: ADAPTIVE LEARNING ARCHITECTURE
    pdf.add_page()
    pdf.chapter_title("2. Adaptive Learning Engine Architecture")
    pdf.body_text("Unlike traditional 'black-box' educational AI, MasteryFlow V2 utilizes a strict 'Teacher-in-the-Loop' architecture. The system models knowledge using a prerequisite directed acyclic graph (DAG).")
    
    pdf.section_title("Zero-Knowledge & Privacy")
    pdf.body_text("Student data privacy is paramount. MasteryFlow proposes an End-to-End Encrypted (E2EE) data model using libsodium, meaning the server processes interactions without knowing the identity or the plaintext performance data of the student.")
    
    pdf.section_title("Dynamic Difficulty Adjustment")
    pdf.body_text("As students answer questions, their mastery score (from 0.0 to 1.0) is dynamically updated based on: \n- Correctness of the answer\n- Reported confidence level (1-5)\n- Time taken to respond\n- Utilization of hints")

    # PAGE 3: EVENT PLATFORM
    pdf.add_page()
    pdf.chapter_title("3. Event Experience Platform")
    pdf.body_text("The second half of MasteryFlow V2 focuses on seamless event management. It replaces the need for 5 separate applications with a single unified dashboard.")
    
    pdf.section_title("Features Breakdown")
    pdf.body_text("- AI Invitation Generator: Premium themed copy in multiple languages.")
    pdf.body_text("- Cinematic Previews: Animated HTML/CSS trailers.")
    pdf.body_text("- Smart RSVP & QR Check-in: Live scanning to prevent duplicates.")
    pdf.body_text("- Live Memory Wall: Real-time photo gallery.")

    # PAGES 4+: CURRICULUM ANALYSIS
    if questions_db:
        subjects = ["Computer Science", "Biology", "Physics", "Chemistry", "Mathematics"]
        
        for subject in subjects:
            pdf.add_page()
            pdf.page_title(f"{subject.upper()} CURRICULUM")
            pdf.body_text(f"The {subject} curriculum is fully integrated into the Adaptive Learning Engine. It consists of 15 carefully curated questions spanning Easy, Medium, and Difficult cognitive levels.")
            
            qs = [q for q in questions_db.Q if q[1] == subject]
            easy_qs = [q for q in qs if q[2] == 1]
            med_qs = [q for q in qs if q[2] == 3]
            diff_qs = [q for q in qs if q[2] == 4]
            
            pdf.chapter_title("Level 1: Foundation (Easy)")
            for q in easy_qs:
                pdf.question_block(q[4], ', '.join(q[5]), q[6], q[7])
                
            pdf.add_page()
            pdf.chapter_title("Level 2: Application (Medium)")
            for q in med_qs:
                pdf.question_block(q[4], ', '.join(q[5]), q[6], q[7])
                
            pdf.add_page()
            pdf.chapter_title("Level 3: Mastery (Difficult)")
            for q in diff_qs:
                pdf.question_block(q[4], ', '.join(q[5]), q[6], q[7])

    pdf.output("MasteryFlow_Premium_Report.pdf")
    print("Report generated successfully.")

if __name__ == "__main__":
    generate_report()
