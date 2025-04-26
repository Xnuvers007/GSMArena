import requests, re
from bs4 import BeautifulSoup

url = 'https://www.gsmarena.com/makers.php3'
base_url = 'https://www.gsmarena.com/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/114.0.0.0 Safari/537.36'
}

def get_all():
  try:
      response = requests.get(url, headers=headers)
      response.raise_for_status()
  except requests.exceptions.RequestException as e:
      print(f"Error: Tidak dapat mengambil data dari GSM Arena. {e}")
      exit(1)

  soup = BeautifulSoup(response.text, 'html.parser')
  cells = soup.select('.st-text td')

  for cell in cells:
      link = cell.find('a')
      if link:
          href = link.get('href')
          full_url = base_url + href
          name = link.get_text(separator=" ", strip=True)

          brand_name = re.sub(r'\s*\d+\s*devices', '', name)
          print(f"Nama Merek: {brand_name.strip()}")
          print(f"Link: {full_url}")
          print("-" * 40)

def user():
  user_input = input("Masukkan Link untuk di-scrape: ")
  if user_input.startswith('https://www.gsmarena.com/'):
      try:
          while True:
              response = requests.get(user_input, headers=headers)
              response.raise_for_status()
              soup = BeautifulSoup(response.text, 'html.parser')
              device_links = soup.select('.makers li a')
              for link in device_links:
                  href = link.get('href')
                  full_url = base_url + href
                  device_model = link.select_one('span').text.strip()  # Ekstrak nama model perangkat
                  print(f"Model Perangkat: {device_model} - Link: {full_url}")
              next_button = soup.select_one('.nav-pages a[class="prevnextbutton"][title="Next page"]')
              if next_button:
                  user_input = base_url + next_button.get('href')
                  print(f"Next URL: {user_input}")
              else:
                  print("Tidak ada halaman berikutnya.")
                  break
      except requests.exceptions.RequestException as e:
          print(f"Error: Tidak dapat mengambil halaman yang ditentukan. {e}")
  else:
      print("URL tidak valid. Silakan masukkan link GSM Arena yang valid.")

def getspecs():
    userwant = input("Masukkan link spesifikasi: ")
    if userwant.startswith('https://www.gsmarena.com/'):
        try:
            response = requests.get(userwant, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            specs_section = soup.find('div', id='specs-list')
            tables = specs_section.find_all('table')

            user_threads = soup.find_all('div', class_='user-thread')
            if user_threads:
                print("\n=== Komentar Pengguna (Beberapa Terbaru) ===")
                for thread in user_threads[:3]:
                    name = thread.find('li', class_='uname') or thread.find('li', class_='uname2')
                    name_text = name.text.strip() if name else "Anonymous"
                    time = thread.find('time').text.strip()
                    comment = thread.find('p', class_='uopin').text.strip()
                    print(f"\n{name_text} ({time}):\n{comment}")
            else:
                print("Tidak ada komentar pengguna yang ditemukan.")

            for table in tables:
                category = table.find('th')
                if category:
                    print(f"\n=== {category.text.strip()} ===")

                rows = table.find_all('tr')
                for row in rows:
                    ttl = row.find('td', class_='ttl')
                    nfo = row.find('td', class_='nfo')
                    if ttl and nfo:
                        label = ttl.text.strip().replace('\xa0', ' ')
                        value = nfo.text.strip().replace('\xa0', ' ')
                        print(f"{label}: {value}")

        except requests.exceptions.RequestException as e:
            print(f"Error: Tidak dapat mengambil spesifikasi dari halaman. {e}")
    else:
        print("URL tidak valid. Silakan masukkan link GSMArena yang valid.")

def main():
    print("Pilih opsi:")
    print("1. Ambil semua merek / get all brands")
    print("2. Ambil perangkat dari link tertentu / get devices from specific link")
    print("3. Ambil spesifikasi dari link tertentu /get specs from specific link")
    print("4. Keluar / exit")
    choice = input("Masukkan pilihan (1/2/3/4): ")

    if choice == '1':
        get_all()
    elif choice == '2':
        user()
    elif choice == '3':
        getspecs()
    elif choice == '4':
        print("Keluar dari program. / Exiting.")
        exit(0)
    else:
        print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
