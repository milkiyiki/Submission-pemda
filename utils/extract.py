import time
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetching_content(url):
    session = requests.Session()
    response = session.get(url, headers=HEADERS)
    
    try:
        response.raise_for_status()
        return response.content
    
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan ketika melakukan requests terhadap {url}: {e}")
        return None

def extract_fashion_data(article):
    try:
        # Title
        title_element = article.find('h3', class_='product-title')
        title = title_element.text.strip()
        
        # Price
        price_container = article.find('div', class_='price-container')
        price_span = price_container.find('span', class_='price') if price_container else article.find('p', class_='price')
        price = price_span.text.strip()
        
        # All <p> elements
        p_tags = article.find_all('p')
        
        for p in p_tags:
            text = p.text.lower()
            if "rating" in text:
                rating = p.text.strip()
            if "colors" in text:
                color = p.text.strip()
            elif "size" in text:
                size = p.text.strip()
            elif "gender" in text:
                gender = p.text.strip()
        
        fashion = {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": color,
            "Size": size,
            "Gender": gender
        }
        
        return fashion
    
    except Exception as e:
        print(f'Gagal mengekstrak data fashion: {e}')
        
        return {
            "Title": "Unknown Product",
            "Price": "Price Unavailable",
            "Rating": "Invalid Rating",
            "Colors": "",
            "Size": "",
            "Gender": ""
        }

def scrape_fashion(base_url='https://fashion-studio.dicoding.dev', start_page=1, delay=2):
    data = []
    page_number = start_page
    
    try:
        while True:
            if page_number == 1:
                url = 'https://fashion-studio.dicoding.dev'
            else:
                url = base_url.format(page_number)
            
            print(f"Scraping halaman: {url}")
            
            content = fetching_content(url)
            if content:
                soup = BeautifulSoup(content, "html.parser") 
                articles_element = soup.find_all('div', class_='product-details')
                
                for article in articles_element:
                    fashion = extract_fashion_data(article)
                    data.append(fashion)
                
                next_button = soup.find('li', class_='page-item next')
                if next_button:
                    page_number += 1
                    time.sleep(delay)
                else:
                    break
            else:
                break
        
        return data
    
    except requests.exceptions.RequestException as e:
        print(f'Terjadi kesalahan saat mengakses situs web: {e}')
        return None
    
    except Exception as e:
        print(f'Terjadi kesalahan saat proses scraping: {e}')
        return None
