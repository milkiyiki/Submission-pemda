import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

def scrape_page(page_number):
    url = f"https://fashion-studio.dicoding.dev/?page={page_number}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Gagal memuat halaman {page_number}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all("div", class_="product-card")

    page_data = []
    for item in items:
        try:
            title = item.find("h3", class_="product-title").text.strip()
            price = item.find("span", class_="product-price").text.strip()
            rating = item.find("span", class_="product-rating").text.strip()
            colors = item.find("span", class_="product-colors").text.strip()
            size = item.find("span", class_="product-size").text.strip()
            gender = item.find("span", class_="product-gender").text.strip()

            data = {
                "Title": title,
                "Price": price,
                "Rating": rating,
                "Colors": colors,
                "Size": size,
                "Gender": gender,
                "Timestamp": datetime.now().isoformat()
            }

            page_data.append(data)

        except Exception as e:
            print(f"[WARNING] Data tidak lengkap di halaman {page_number}, dilewati. {e}")
            continue

    return page_data

def scrape_all(pages=50, delay=1):
    all_data = []
    for page in range(1, pages + 1):
        print(f"[INFO] Scraping halaman {page}")
        data = scrape_page(page)
        all_data.extend(data)
        time.sleep(delay)  # Hindari terlalu cepat (rate limit)

    df = pd.DataFrame(all_data)
    return df
