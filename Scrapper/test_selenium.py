from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Test Selenium setup
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.ycombinator.com/companies?query=saas")
    print("Selenium setup successful!")
    driver.quit()
except Exception as e:
    print(f"Selenium setup failed: {e}")
