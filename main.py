import os
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKGROUND_IMAGE = os.path.join(BASE_DIR, "static", "back.jpg")

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/generate-pdf")
def generate_pdf(
    shipping_bill_no: str = Form(...),
    invoice_no: str = Form(...),
    nature_of_transaction: str = Form(...),
    sellers_buyers: str = Form(...),
    influenced_price: str = Form(...),
    terms_payment: str = Form(...),
    terms_delivery: str = Form(...),
    place: str = Form(...),
    date: str = Form(...)
):
    try:
        if not os.path.exists(BACKGROUND_IMAGE):
            raise FileNotFoundError(f"Image not found: {BACKGROUND_IMAGE}")

        output_pdf = "custom_clearance_output.pdf"
        c = canvas.Canvas(output_pdf, pagesize=A4)
        width, height = A4

        # Draw background
        c.drawImage(BACKGROUND_IMAGE, 0, 0, width=width, height=height)

        # Add user inputs
        
        c.setFont("Helvetica-Bold", 11)
        y = height - 100
        gap = 22
        c.drawString(250, 700, f"{shipping_bill_no}")
        c.drawString(200, 665, f"{invoice_no}")
        c.drawString(240, 635, f"{nature_of_transaction}")
        c.drawString(410, 485, f"{sellers_buyers}")
        c.drawString(490, 450, f"{influenced_price}")
        c.drawString(200, 420, f"{terms_payment}")
        c.drawString(200, 380, f"{terms_delivery}")
        c.drawString(115, 160, f"{place}")
        c.drawString(110, 140, f"{date}")

        c.showPage()
        c.save()

        return FileResponse(output_pdf, filename="custom_clearance.pdf", media_type="application/pdf")

    except Exception as e:
        return HTMLResponse(content=f"<h2>Error: {str(e)}</h2>", status_code=500)
