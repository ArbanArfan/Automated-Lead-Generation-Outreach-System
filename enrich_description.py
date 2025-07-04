import csv
import requests
from bs4 import BeautifulSoup

def get_description(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Try to get meta description first
        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"):
            return meta["content"].strip()

        # Try Open Graph description
        og = soup.find("meta", property="og:description")
        if og and og.get("content"):
            return og["content"].strip()

        # Fallback: first paragraph with decent length
        paragraphs = soup.find_all("p")
        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) > 40:
                return text

    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
    return ""


# --- Read and enrich CSV ---
input_file = "final_output.csv"
output_file = "final_output_enriched.csv"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", newline="", encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        if not row["Description"] or row["Description"].strip() == "":
            print(f"🔍 Fetching description for: {row['Startup URL']}")
            desc = get_description(row["Startup URL"])
            row["Description"] = desc
        writer.writerow(row)

print("✅ Descriptions updated. Saved to final_output_enriched.csv")
