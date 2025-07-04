🚀 Automated YC Startup Lead Scraper
This project scrapes startups from the Y Combinator Startup Directory based on specific keywords. It extracts detailed startup and founder data and saves it in both JSON and CSV formats — making it easy to build lead lists for outreach or market research.

📌 Features
✅ Search startups by custom keyword list

✅ Scrape up to 100 companies per keyword

✅ Extract:

Startup Name

Startup Website URL

Description

Matching Keyword

Founders’ Name, Role, LinkedIn, Email

✅ Guess missing founder emails using domain + name

✅ Save results live to final.json

✅ Convert final.json to final_output.csv with structured outreach columns

🗂 Project Structure
pgsql
Copy
Edit
automated-lead-scraper/
│
├── main.py                → Main scraper using Selenium + BeautifulSoup
├── json_to_csv.py         → Converts final.json to outreach-ready CSV
├── final.json             → Scraped startup data (auto-created)
├── final_output.csv       → Processed CSV output for emails
├── requirements.txt       → All Python dependencies
└── README.md              → You’re reading it :)
🛠 Setup Instructions
1. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
Make sure Google Chrome is installed and chromedriver is compatible with your Chrome version.

2. Set Up chromedriver (Optional if auto-detected)
Download from: https://sites.google.com/chromium.org/driver/

Place chromedriver in project root or add to your system PATH.

3. Run the Scraper
bash
Copy
Edit
python main.py
This will create or update final.json in real time.

4. Convert JSON to CSV
bash
Copy
Edit
python json_to_csv.py
This generates a formatted final_output.csv with one row per startup (first founder only), plus placeholder columns for outreach tracking.

⚙️ Customization
Edit KEYWORDS list in main.py to search for different industries or startup types.

Adjust number of startups per keyword (default = 100).

Modify or extend the email templates in the CSV output script.

💡 Future Ideas
Add LinkedIn scraping for job titles / roles

Integrate email verification or enrichment API

Auto-send outreach emails via Gmail or SMTP

Store results in a database (MongoDB / PostgreSQL)

Export all founders as separate rows

