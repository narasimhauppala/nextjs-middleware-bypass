# Next.js Middleware Bypass Tester

A Python script to test Next.js applications for middleware bypass vulnerabilities. The tool attempts various bypass techniques and captures screenshots when potential vulnerabilities are detected.

## Features

- Tests multiple middleware bypass techniques
- Automatic screenshot capture for successful bypasses
- Support for multiple subdomains
- SSL verification bypass
- Headless browser testing
- Custom header manipulation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/narasimhauppala/nextjs-middleware-bypass/upload/main
cd nextjs-middleware-bypass
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Create a file containing target URLs/subdomains (one per line):
```text
example.com
subdomain.example.com
app.example.com
```

2. Run the script:
```bash
python script.py -f targets.txt
```

## Requirements

Create a `requirements.txt` file with:
```
requests
selenium
webdriver-manager
urllib3
```

## How it Works

The script:
1. Reads target URLs from the input file
2. Tests each URL with various middleware bypass headers
3. Captures screenshots when redirects (301, 302, 307, 308) are detected
4. Saves screenshots in the `screenshots` directory

### Bypass Headers Tested

- middleware:middleware:middleware:middleware:middleware
- middleware:root
- middleware:nextjs
- pages/_middleware
- _next/data
- middleware:rewrite:middleware
- middleware:middleware
- middleware:pages
- _next/data/middleware
- next-middleware
- _next/static

## Output Format

The script provides detailed output for each test:
```
[*] Testing: https://example.com

[>] Testing URL: https://example.com
[>] Header: middleware:nextjs
Status Code: 307

Important Response Headers:
location: /redirect
x-nextjs-match: true

[!] Redirect Detected!
[>] Redirect Location: /redirect
[+] Screenshot saved: screenshots/example.com__middleware_nextjs__20240401-120000.png
```

## Screenshots

Screenshots are saved in the `screenshots` directory with the following naming format:
```
{domain}__{header-value}__{timestamp}.png
```

## Disclaimer

This tool is for educational and security testing purposes only. Always obtain proper authorization before testing any websites or applications.

## Author

Your Name (@narasimhauppala)

## Acknowledgments

- Next.js Security Documentation
- CVE-2025-29927 Research

