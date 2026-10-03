from fpdf import FPDF

class PremiumPDF(FPDF):
    def header(self):
        # Draw dark background for the whole page
        self.set_fill_color(10, 25, 47) # #0a192f
        self.rect(0, 0, 210, 297, 'F')
        
        # Header Box
        self.set_fill_color(17, 34, 64) # #112240
        self.rect(10, 10, 190, 20, 'F')
        
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(249, 115, 22) # Orange
        self.set_xy(10, 14)
        self.cell(190, 10, "MASTERYFLOW V2", align="C")
        
        self.set_font("Helvetica", "I", 11)
        self.set_text_color(14, 165, 233) # Light Blue
        self.set_xy(10, 21)
        self.cell(190, 10, "Hackathon Presentation Pitch", align="C")
        self.set_y(40)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(136, 146, 176) # #8892b0
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(14, 165, 233) # Blue
        self.cell(0, 10, title)
        self.ln(12)
        
    def chapter_body(self, text):
        self.set_font("Helvetica", "", 12)
        self.set_text_color(248, 250, 252) # White
        # Sanitize
        text = text.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 7, text)
        self.ln(8)
        
    def highlight_box(self, text):
        self.set_fill_color(249, 115, 22) # Orange
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 12)
        text = text.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 10, text, fill=True)
        self.ln(5)

def make_pdf():
    pdf = PremiumPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # SLIDE 1
    pdf.chapter_title("Slide 1: Title Screen")
    pdf.highlight_box("  Visual: Show the new Cinematic Intro playing on your screen.")
    pdf.chapter_body('Speaker: "Hello judges, we are the creators of MasteryFlow V2. We believe that technology should empower human connection and growth -- whether that is in the classroom learning complex topics, or in the real world experiencing events. Today, we are excited to show you a platform that does exactly that: MasteryFlow V2."')
    
    # SLIDE 2
    pdf.chapter_title("Slide 2: The Problem")
    pdf.chapter_body('Speaker: "We identified two major problems in today\'s digital landscape:\n1. In Education: Learning platforms rely heavily on black-box AI that teachers can\'t control, and they hoard student data without privacy.\n2. In Events: Organizing a modern event requires 5 different apps -- one for invitations, one for RSVPs, one for ticketing, and another for photos.\n\nWe solved both problems under one unified, premium ecosystem."')

    # SLIDE 3
    pdf.chapter_title("Slide 3: The Solution (Part 1 - Adaptive Learning)")
    pdf.chapter_body('Speaker: "First, our Adaptive Learning Engine. It is a transparent, Teacher-in-the-loop platform.\nInstead of a black-box AI guessing what a student knows, our engine uses a strict prerequisite knowledge graph.\nMost importantly, it is designed with Zero-Knowledge architecture -- meaning student data is encrypted and completely private. The teacher remains the ultimate authority and can override the AI at any time."')

    pdf.add_page()
    
    # SLIDE 4
    pdf.chapter_title("Slide 4: The Solution (Part 2 - Event Experience)")
    pdf.chapter_body('Speaker: "Second, our Event Experience Platform. We built an AI-powered system that handles an event from start to finish. From generating the invitation copy with AI, to cinematic video previews, to QR code check-ins and a live memory wall for guests. It is an end-to-end premium experience."')

    # SLIDE 5: SYNERGY
    pdf.chapter_title("Slide 5: The Synergy (Pre-Requisite Screening)")
    pdf.chapter_body('Speaker: "You might be wondering how Events and Learning connect. We designed MasteryFlow for high-end academic and corporate workshops. Before a guest is allowed to RSVP to an advanced workshop (like an AI Bootcamp), they must use our Adaptive Learning Engine to prove their foundational knowledge in Computer Science and Mathematics. We do not just manage tickets -- we ensure the audience is actually prepared for the event."')
    
    # SLIDE 6: OPENAI
    pdf.chapter_title("Slide 6: Live OpenAI Integration (The AI Mentor)")
    pdf.chapter_body('Speaker: "Lastly, we implemented a live integration with OpenAI. Instead of a standard backend, we built an AI Mentor directly into the Learning Engine. When a student makes a mistake, the AI analyzes their exact wrong answer, explains the logical flaw, teaches the concept using a real-world analogy, and provides an actionable training tip. We also integrated Flow AI into the Event Platform to handle live guest queries."')
    
    # DEMO
    pdf.set_font("Helvetica", "B", 18)
    self_color = pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, "LIVE DEMO SCRIPT")
    pdf.ln(15)
    
    pdf.highlight_box("  Step 1: The Cinematic Intro")
    pdf.chapter_body('Action: Open the app and let the 10-second cinematic intro play out.\nSay: "We built a premium, game-style cinematic engine using pure CSS animations to give users a breathtaking first impression."')
    
    pdf.highlight_box("  Step 2: The Event Platform Demo")
    pdf.chapter_body('Action: Click on \'EXPLORE EVENT PLATFORM\'.\nSay: "Let\'s say we are organizing TechFest 2026. From our dashboard, the host can use our AI Generator to instantly create invitation copy in multiple languages and moods."\nAction: Click through the tabs. Show the Cinematic Preview, and then show the Smart RSVP Dashboard.\nSay: "We also feature a live QR scanner for check-ins, and a Live Event Memory Wall where guests can upload photos in real-time."')

    pdf.add_page()
    
    pdf.highlight_box("  Step 3: The Adaptive Learning & AI Mentor Demo")
    pdf.chapter_body('Action: Refresh the page, skip the intro, and click \'START YOUR JOURNEY\'.\nSay: "Now let\'s look at the Adaptive Learning side, loaded with our 75-question database."\nAction: Go to the Practice Arena and intentionally choose a WRONG answer.\nSay: "Watch what happens. Instead of just telling the student they are wrong, our live AI Mentor generates a custom coaching session. It explains the flaw in logic, gives an analogy, and trains them to never make that mistake again."\nAction: Switch to the Teacher Dashboard tab.\nSay: "Finally, this is the Teacher Command Center. The AI recommends actions, but the teacher can always step in and apply a manual override."')

    # SELLING POINTS
    pdf.chapter_title("Key Selling Points to highlight for Q&A:")
    pdf.chapter_body("1. Design: We focused heavily on UI/UX. We used glassmorphism, dynamic gradients, and custom keyframe animations because user engagement directly correlates with visual quality.\n\n2. Architecture: We built this highly responsive, dual-platform prototype entirely in Python using Streamlit, proving that complex, beautiful UIs can be rapidly engineered.\n\n3. Advanced Features: We integrated a LIVE 75-question database and live OpenAI functionality (AI Mentor & Flow Assistant) directly into the prototype. It is not just a UI mock, it is a fully functional product.")

    pdf.output("MasteryFlow_Presentation.pdf")
    print("PDF generated successfully.")

if __name__ == "__main__":
    make_pdf()
