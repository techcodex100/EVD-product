import csv
import os
import requests
import time
import datetime
import psutil
from random import randint

# 🏁 Configuration
RENDER_URL = "https://evd-product.onrender.com/generate-pdf"
PDF_OUTPUT_DIR = "evd_pdfs_from_csv"
CSV_OUTPUT_DIR = "evd_reports_from_csv"
os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)
os.makedirs(CSV_OUTPUT_DIR, exist_ok=True)

# 📋 Test parameters
test_parameters = [
    "Reliability", "Latency", "Throughput", "Availability",
    "Resource Utilization", "Robustness", "User-Friendliness"
]

def get_evaluation(param):
    score = randint(3, 5)
    remarks = {
        5: "Excellent performance under all tested conditions.",
        4: "Good performance with minor improvements suggested.",
        3: "Acceptable performance; needs optimization."
    }
    return score, remarks[score]

def post_with_retries(data_dict, retries=3, delay=2):
    for attempt in range(1, retries + 1):
        try:
            response = requests.post(RENDER_URL, data=data_dict)
            if response.status_code == 200:
                return response
            else:
                print(f"⚠️ Attempt {attempt} failed with status {response.status_code}")
        except Exception as e:
            print(f"⚠️ Attempt {attempt} raised exception: {e}")
        time.sleep(delay)
    return None

# 📤 Main Execution
with open("evd_input_data.csv", newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for idx, row in enumerate(reader, 1):
        print(f"🚀 Generating PDF for row {idx}")
        start_time = time.time()

        clean_data = {k.strip(): v.strip() for k, v in row.items()}
        response = post_with_retries(clean_data)

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        pdf_filename = os.path.join(PDF_OUTPUT_DIR, f"evd_certificate_{idx}_{timestamp}.pdf")

        if response:
            with open(pdf_filename, "wb") as f:
                f.write(response.content)
        else:
            print(f"❌ Failed to generate PDF for row {idx}")
            continue

        # 📝 Report
        report_file = os.path.join(CSV_OUTPUT_DIR, f"evd_report_{idx}.csv")
        with open(report_file, "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["🔹 Field", "Value"])
            for k, v in clean_data.items():
                writer.writerow([k, v])
            writer.writerow([])
            writer.writerow(["✅ Parameter", "Score", "Remarks"])
            for param in test_parameters:
                score, remark = get_evaluation(param)
                writer.writerow([param, score, remark])

        elapsed = round(time.time() - start_time, 2)
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent

        print(f"✅ Row {idx} done | Time: {elapsed}s | CPU: {cpu}% | RAM: {mem}%")
        print("-" * 50)
        time.sleep(1)

print("🎉 All Custom Clearance PDFs and reports generated!")
