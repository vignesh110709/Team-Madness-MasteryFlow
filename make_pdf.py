import os
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Courier', 'B', 12)
        self.cell(0, 10, 'MasteryFlow_V2 - Project Source Code', new_x="LMARGIN", new_y="NEXT", align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Courier', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf():
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Courier", size=10)
    
    files_to_include = ['README.md', 'requirements.txt', 'app.py']
    
    for filename in files_to_include:
        if not os.path.exists(filename):
            continue
            
        # Title of the file
        pdf.set_font("Courier", 'B', 12)
        pdf.cell(0, 10, f'--- {filename} ---', new_x="LMARGIN", new_y="NEXT", align='L')
        pdf.set_font("Courier", size=10)
        
        # Content of the file
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                # Sanitize line to latin-1 to avoid font errors with emojis
                safe_line = line.encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(0, 5, text=safe_line)
                
        pdf.ln(5)

    pdf.output("MasteryFlow_Project.pdf")

if __name__ == "__main__":
    create_pdf()
