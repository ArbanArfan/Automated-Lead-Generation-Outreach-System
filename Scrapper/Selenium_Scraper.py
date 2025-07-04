import json
import re
import time
import random
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

KEYWORDS = [
    "SaaS", "MVP", "early-stage startup", "product launch", "prototype",
    "software startup", "Artificial Intelligence", "AI-powered", "Machine Learning",
    "Generative AI", "NLP", "Full-stack development", "Mobile app", "MERN stack",
    "React Native", "Next.js", "Flutter", "Automation tools", "Business automation",
    "Workflow automation", "Zapier alternative", "Pre-seed", "Seed funding",
    "B2B SaaS", "YC-backed", "Tech startup"
]

# --- Functions ---
def get_domain(url):
    if not url:
        return ""
    try:
        parsed = urlparse(url)
        return parsed.netloc.replace("www.", "")
    except:
        return ""

def guess_emails(name, startup_name):
    name = name.lower()
    parts = name.split()
    if not domain or not parts:
        return []
    first = parts[0]
    last = parts[-1]
    initials = first[0] if first else ""
    guesses = [
        f"{first}@{startup_name}.com",
        f"{first}{last}@{startup_name}.com",
        f"{first}.{last}@{startup_name}.com",
        f"{initials}{last}@{startup_name}.com",
    ]
    return guesses

def append_to_json(file_path, data):
    try:
        with open(file_path, "r+", encoding="utf-8") as f:
            try:
                existing = json.load(f)
            except:
                existing = []
            existing.append(data)
            f.seek(0)
            json.dump(existing, f, ensure_ascii=False, indent=2)
    except FileNotFoundError:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([data], f, ensure_ascii=False, indent=2)

# --- Setup ---
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

# --- Start ---
try:
    driver.get("https://www.ycombinator.com/companies")
    time.sleep(random.uniform(3, 5))

    for keyword in KEYWORDS:
        print(f"\n🔍 Searching for keyword: {keyword}")
        search_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Search...']"))
        )
        driver.execute_script("arguments[0].value = '';", search_input)
        time.sleep(random.uniform(0.5, 1.0))
        search_input.send_keys(keyword)
        time.sleep(random.uniform(1.5, 2.5))

        company_cards = driver.find_elements(By.XPATH, "//a[contains(@href, '/companies/')]")
        last_count = 0
        scroll_attempts = 0

        while len(company_cards) < 100 and scroll_attempts < 10:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(1.5, 2.5))
            new_cards = driver.find_elements(By.XPATH, "//a[contains(@href, '/companies/')]")
            if len(new_cards) == last_count:
                break
            company_cards = new_cards
            last_count = len(new_cards)
            scroll_attempts += 1

        company_links = []
        for elem in company_cards[:20]:
            url = elem.get_attribute("href")
            if url and "/companies/" in url:
                company_links.append(url)

        for company_url in company_links:
            print(f"➡ Visiting: {company_url}")
            driver.get(company_url)
            time.sleep(random.uniform(2, 4))
            soup = BeautifulSoup(driver.page_source, "html.parser")

            startup_name = soup.find("h1").text.strip() if soup.find("h1") else "Unknown"
            if startup_name.lower() in ["twitter", "footer", "header", "Twitter","founder directory","header directory"]:
                print(f"❌ Skipping: {startup_name} (invalid name)")
                continue

            # Startup Description
            description = ""
            founders_header = soup.find(string=lambda t: t and "Founders" in t)
            if founders_header:
                desc_paras = founders_header.find_all_previous("p")
                if desc_paras:
                    description = " ".join(p.get_text(strip=True) for p in desc_paras[::-1])
            else:
                fallback = soup.find_all("p", limit=2)
                description = " ".join(p.get_text(strip=True) for p in fallback)

            # Website URL (not a YC link)
            site_url = ""
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if href.startswith("http") and not any(x in href for x in ["ycombinator.com", "startupschool.org"]):
                    site_url = href
                    break
            domain = get_domain(site_url)

            # Founders
            founders = []
            founder_links = soup.find_all("a", href=lambda h: h and "linkedin.com/in" in h)
            for a in founder_links:
                if a.text.strip():
                    founder_name = a.text.strip()
                else:
                    img = a.find_previous("img", alt=True)
                    founder_name = img['alt'].strip() if img and img.has_attr('alt') else "Unknown"

                if founder_name.lower() in ["twitter", "footer", "header", "twitter account"]:
                    print(f"❌ Skipping founder: {founder_name} (invalid name)")
                    continue

                linkedin_url = a["href"]
                email = ""

                
                guesses = guess_emails(founder_name, startup_name.lower().replace(" ", ""))
                email = guesses[0]

                founders.append({
                    "Name": founder_name,
                    "Role": "Founder",
                    "LinkedIn": linkedin_url,
                    "Email": email
                })

            company_data = {
                "Startup Name": startup_name,
                "Startup URL": site_url,
                "Startup Description": description,
                "Startup Keyword": keyword,
                "Founders": founders
            }

            append_to_json("final.json", company_data)
            print(f"✅ Saved: {startup_name}")

        driver.get("https://www.ycombinator.com/companies")
        time.sleep(random.uniform(2, 3))

finally:
    driver.quit()
    print("\n✅ Scraping completed. Data saved to final.json")
