from fpdf import FPDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=16)
pdf.cell(0, 10, text="RoomieMatch Pro - Roommate Agreement", new_x="LMARGIN", new_y="NEXT", align='C')

pdf.ln(10)
pdf.set_font("Arial", size=12)

pdf.cell(0, 10, text="Date: 2026-04-05", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 10, text="Resident Name: Test User", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 10, text="Email: test@example.com", new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)

text = (
    "This agreement is to verify that the resident has agreed to the terms and "
    "conditions set forth by RoomieMatch Pro for shared living arrangements. "
    "The resident agrees to maintain appropriate cleanliness and noise levels "
    "based on their profile selections."
)
pdf.multi_cell(0, 10, text=text, new_x="LMARGIN", new_y="NEXT")

pdf.ln(20)
pdf.cell(0, 10, text="Signature: __________________________", new_x="LMARGIN", new_y="NEXT")

pdf.output()
print("Success!")
