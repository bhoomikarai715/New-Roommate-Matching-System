from fastapi import APIRouter, Depends
from fastapi.responses import Response
from datetime import datetime
from backend.models.entities import User
from backend.routes.auth import get_current_user

router = APIRouter(prefix="/api/agreement", tags=["agreement"])

@router.get("/download")
def download_agreement(current_user: User = Depends(get_current_user)):
    try:
        from fpdf import FPDF
    except ImportError:
        return Response(content="PDF Generation is unavailable in this environment.", status_code=400)
        
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(0, 10, text="RoomieMatch Pro - Roommate Agreement", new_x="LMARGIN", new_y="NEXT", align='C')
    
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    pdf.cell(0, 10, text=f"Date: {date_str}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, text=f"Resident Name: {current_user.full_name}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, text=f"Email: {current_user.email}", new_x="LMARGIN", new_y="NEXT")
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
    
    pdf_bytes = bytes(pdf.output())
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=agreement.pdf"}
    )
