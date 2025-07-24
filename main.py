from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

app = FastAPI()

# Path to your background image
BACKGROUND_IMAGE = r"C:/Users/Lenovo/OneDrive/Desktop/customclearance/static/back.jpg"

@app.get("/", response_class=HTMLResponse)
def serve_form():
    return """
    <html>
        <body>
            <h2>Custom Clearance PDF Generator</h2>
            <form action="/generate-pdf" method="post">
                Shipping Bill No: <input type="text" name="shipping_bill_no"><br>
                Invoice No: <input type="text" name="invoice_no"><br>
                Nature of Transaction: <input type="text" name="nature_of_transaction"><br>
                Sellers and Buyers: <input type="text" name="sellers_buyers"><br>
                Influenced Price: <input type="text" name="influenced_price"><br>
                Terms of Payment: <input type="text" name="terms_payment"><br>
                Terms of Delivery: <input type="text" name="terms_delivery"><br>
                Place: <input type="text" name="place"><br>
                Date: <input type="text" name="date"><br><br>
                <input type="submit" value="Generate PDF">
            </form>
        </body>
    </html>
    """

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
            raise FileNotFoundError(f"Image not found at {BACKGROUND_IMAGE}")

        output_pdf = "custom_clearance_output.pdf"
        c = canvas.Canvas(output_pdf, pagesize=A4)
        width, height = A4

        # Draw background image
        c.drawImage(BACKGROUND_IMAGE, 0, 0, width=width, height=height)

        # Set font for form data
        c.setFont("Helvetica-Bold", 11)

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
