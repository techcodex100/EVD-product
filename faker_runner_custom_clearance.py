import os
import time
import datetime
import requests
import psutil
from faker import Faker

fake = Faker()

RENDER_URL = "https://evd-product.onrender.com/generate-pdf"
pdf_output_dir = "rendered_custom_clearance_pdfs"
os.makedirs(pdf_output_dir, exist_ok=True)

MAX_RETRIES = 5
DELAY_BETWEEN_REQUESTS = 2  # seconds

def generate_fake_data():
    return {
        "shipping_bill_no": f"SB-{fake.random_number(digits=6)}",
        "invoice_no": f"INV-{fake.random_number(digits=5)}",
        "nature_of_transaction": fake.random_element(elements=["Export", "Import", "Re-export"]),
        "sellers_buyers": fake.name() + " / " + fake.company(),
        "influenced_price": f"USD {fake.random_int(min=1000, max=50000)}",
        "terms_payment": fake.random_element(elements=["Advance", "LC", "DA", "DP"]),
        "terms_delivery": fake.random_element(elements=["FOB", "CIF", "CFR"]),
        "place": fake.city(),
        "date": fake.date()
    }

for i in range(1, 51):
    payload = generate_fake_data()
    start_time = time.time()

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(RENDER_URL, data=payload)
            if response.status_code == 200:
                break
            else:
                print(f"[{i}] ⚠️ Attempt {attempt} failed - Status {response.status_code}")
        except Exception as e:
            print(f"[{i}] ❌ Exception: {e}")
        time.sleep(3)

    if response.status_code != 200:
        print(f"[{i}] ❌ Skipped after {MAX_RETRIES} attempts.")
        continue

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"custom_clearance_{i}_{timestamp}.pdf"
    filepath = os.path.join(pdf_output_dir, filename)

    with open(filepath, "wb") as f:
        f.write(response.content)

    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    elapsed = round(time.time() - start_time, 2)

    print(f"✅ [{i}/50] PDF Generated: {filename}")
    print(f"   CPU: {cpu}% | RAM: {mem}% | Time: {elapsed}s")
    print("-" * 50)

    time.sleep(DELAY_BETWEEN_REQUESTS)

print("🎉 All 50 Custom Clearance PDFs generated.")
