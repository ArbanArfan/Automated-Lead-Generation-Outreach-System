import json
import csv

# Load data from final.json
with open("final.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Output CSV file
csv_file = "final_output.csv"

# Define the CSV column headers
headers = [
    "Startup Name",
    "Startup URL",
    "Description",
    "Keywords Matched",
    "Founder Name",
    "Founder Role",
    "Founder LinkedIn",
    "Founder Email",
    "Email Subject",
    "Email Message",
    "Followup-1 Subject",
    "Followup-1 Message",
    "Followup-2 Subject",
    "Followup-2 Message",
    "Status"
]

# Write to CSV
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()

    for company in data:
        # Skip if no founders or missing required founder info
        if not company.get("Founders"):
            continue

        founder = company["Founders"][0]

        if not founder.get("Name") or not founder.get("Email"):
            continue  # skip incomplete founder

        row = {
            "Startup Name": company.get("Startup Name", ""),
            "Startup URL": company.get("Startup URL", ""),
            "Description": company.get("Startup Description", ""),
            "Keywords Matched": company.get("Startup Keyword", ""),
            "Founder Name": founder.get("Name", ""),
            "Founder Role": founder.get("Role", ""),
            "Founder LinkedIn": founder.get("LinkedIn", ""),
            "Founder Email": founder.get("Email", ""),
            "Email Subject": "",
            "Email Message": "",
            "Followup-1 Subject": "",
            "Followup-1 Message": "",
            "Followup-2 Subject": "",
            "Followup-2 Message": "",
            "Status": "Pending"
        }

        writer.writerow(row)

print(f"✅ Done. Data written to {csv_file}")
