from flask import Flask, request, jsonify
import requests, re
from bs4 import BeautifulSoup

app = Flask(__name__)

BASE_URL = 'https://www.gsmarena.com/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/114.0.0.0 Safari/537.36'
}

@app.route('/')
def home():
    return jsonify({
        "message": "Selamat datang di GSM Arena Scraper API!",
        "endpoints": {
            "/brands": "Daftar semua merek",
            "/devices?url=URL_BRAND": "Daftar perangkat dari brand tertentu",
            "/specs?url=URL_PRODUK": "Spesifikasi & komentar dari produk tertentu"
        }
    })

@app.route('/brands')
def get_all_brands():
    url = 'https://www.gsmarena.com/makers.php3'
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        cells = soup.select('.st-text td')

        brands = []
        for cell in cells:
            link = cell.find('a')
            if link:
                href = link.get('href')
                full_url = BASE_URL + href
                name = link.get_text(separator=" ", strip=True)
                brand_name = re.sub(r'\s*\d+\s*devices', '', name)
                brands.append({
                    "brand": brand_name.strip(),
                    "link": full_url
                })
        return jsonify(brands)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/devices')
def get_devices():
    user_input = request.args.get('url')
    if not user_input or not user_input.startswith('https://www.gsmarena.com/'):
        return jsonify({"error": "URL tidak valid atau tidak ada"}), 400

    devices = []
    try:
        while True:
            response = requests.get(user_input, headers=HEADERS)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            device_links = soup.select('.makers li a')

            for link in device_links:
                href = link.get('href')
                full_url = BASE_URL + href
                model = link.select_one('span').text.strip()
                devices.append({
                    "model": model,
                    "link": full_url
                })

            next_button = soup.select_one('.nav-pages a[title="Next page"]')
            if next_button:
                user_input = BASE_URL + next_button.get('href')
            else:
                break
        return jsonify(devices)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/specs')
def get_specs():
    url = request.args.get('url')
    if not url or not url.startswith('https://www.gsmarena.com/'):
        return jsonify({"error": "URL tidak valid atau tidak ada"}), 400

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        specs = {}
        specs_section = soup.find('div', id='specs-list')
        if specs_section:
            tables = specs_section.find_all('table')
            for table in tables:
                category = table.find('th').text.strip() if table.find('th') else "Unknown"
                rows = table.find_all('tr')
                specs[category] = {}
                for row in rows:
                    ttl = row.find('td', class_='ttl')
                    nfo = row.find('td', class_='nfo')
                    if ttl and nfo:
                        specs[category][ttl.text.strip()] = nfo.text.strip()

        comments = []
        user_threads = soup.find_all('div', class_='user-thread')
        for thread in user_threads[:3]:
            name_tag = thread.find('li', class_='uname') or thread.find('li', class_='uname2')
            name = name_tag.text.strip() if name_tag else "Anonymous"
            time = thread.find('time').text.strip()
            comment = thread.find('p', class_='uopin').text.strip()
            comments.append({
                "name": name,
                "time": time,
                "comment": comment
            })

        return jsonify({
            "specifications": specs,
            "user_comments": comments
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False) # True
