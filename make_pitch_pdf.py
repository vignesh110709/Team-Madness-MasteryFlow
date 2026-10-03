from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("Courier", "B", 14)
        self.cell(0, 10, "MasteryFlow V2 - Hackathon Presentation Pitch", border=False, ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Courier", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def make_pdf():
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Courier", size=11)

    text = """
Slide 1: Title Screen
---------------------
Visual: Show the new Cinematic Intro playing on your screen.
Speaker: "Hello judges, we are the creators of MasteryFlow V2. We believe that technology should empower human connection and growth -- whether that is in the classroom learning complex topics, or in the real world experiencing events. Today, we are excited to show you a platform that does exactly that: MasteryFlow V2."

Slide 2: The Problem
--------------------
Speaker: "We identified two major problems in today's digital landscape:
1. In Education: Learning platforms rely heavily on black-box AI that teachers can't control, and they hoard student data without privacy. 
2. In Events: Organizing a modern event requires 5 different apps -- one for invitations, one for RSVPs, one for ticketing, and another for photos.
We solved both problems under one unified, premium ecosystem."

Slide 3: The Solution (Part 1 - Adaptive Learning)
--------------------------------------------------
Speaker: "First, our Adaptive Learning Engine. It is a transparent, 'Teacher-in-the-loop' platform. 
Instead of a black-box AI guessing what a student knows, our engine uses a strict prerequisite knowledge graph. 
Most importantly, it is designed with Zero-Knowledge architecture -- meaning student data is encrypted and completely private. The teacher remains the ultimate authority and can override the AI at any time."

Slide 4: The Solution (Part 2 - Event Experience)
-------------------------------------------------
Speaker: "Second, our Event Experience Platform. We built an AI-powered system that handles an event from start to finish. From generating the invitation copy with AI, to cinematic video previews, to QR code check-ins and a live memory wall for guests. It is an end-to-end premium experience."

==================================================

Live Demo Script (How to show the app)
======================================

Step 1: The Cinematic Intro
---------------------------
Action: Open the app and let the 10-second cinematic intro play out.
Say: "We built a premium, game-style cinematic engine using pure CSS animations to give users a breathtaking first impression."

Step 2: The Event Platform Demo
-------------------------------
Action: Click on "EXPLORE EVENT PLATFORM".
Say: "Let's say we are organizing TechFest 2026. From our dashboard, the host can use our AI Generator to instantly create invitation copy in multiple languages and moods."
Action: Click through the tabs. Show the Cinematic Preview, and then show the Smart RSVP Dashboard.
Say: "We also feature a live QR scanner for check-ins, and a Live Event Memory Wall where guests can upload photos in real-time."

Step 3: The Adaptive Learning Demo
----------------------------------
Action: Refresh the page, skip the intro, and click "START YOUR JOURNEY".
Say: "Now let's look at the Adaptive Learning side, currently loaded with a 75-question database across 5 subjects."
Action: Go to the Practice Arena, select 'Computer Science' or 'Physics', choose an answer, and click Submit & Adapt.
Say: "The engine instantly calculates the student's mastery. Notice how it provides transparent reasoning -- telling the user exactly why they are advancing or being held back based on prerequisites."
Action: Switch to the Teacher Dashboard tab.
Say: "Finally, this is the Teacher Command Center. The AI recommends actions, but the teacher can always step in and apply a manual override. It is AI assisting humans, not replacing them."

==================================================

Key Selling Points to highlight for Q&A:
----------------------------------------
1. Design: We focused heavily on UI/UX. We used glassmorphism, dynamic gradients, and custom keyframe animations because user engagement directly correlates with visual quality.
2. Architecture: We didn't rely on massive heavy frameworks. We built this highly responsive, dual-platform prototype entirely in Python using Streamlit, proving that complex, beautiful UIs can be rapidly engineered.
3. The 75-Question DB: The learning engine isn't just a UI mock. It is fully integrated with a real database of 75 questions across 5 subjects, dynamically adapting the difficulty based on the user's responses.
"""
    
    # Sanitize text to latin-1 to avoid fpdf errors with standard courier font
    sanitized_text = text.encode('latin-1', 'replace').decode('latin-1')
    
    pdf.multi_cell(0, 7, sanitized_text)
    pdf.output("MasteryFlow_Presentation.pdf")
    print("PDF generated successfully.")

if __name__ == "__main__":
    make_pdf()
