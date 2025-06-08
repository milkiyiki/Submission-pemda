from utils.extract import scrape_all_pages
from utils.transform import clean_data
from utils.load import save_to_csv, save_to_gsheets, save_to_postgresql
import pandas as pd

def run_etl():
    print("[1] Menjalankan proses extract...")
    raw_data = scrape_all_pages()

    if raw_data.empty:
        print("Gagal mengambil data. ETL dihentikan.")
        return

    print(f"[2] Extract selesai. {len(raw_data)} data berhasil diambil.")
    
    print("[3] Menjalankan proses transform...")
    cleaned_data = clean_data(raw_data)
    print(f"[4] Transform selesai. {len(cleaned_data)} data bersih.")

    print("[5] Menyimpan data ke CSV...")
    save_to_csv(cleaned_data, "products.csv")

    print("[6] Menyimpan data ke Google Sheets...")
    save_to_gsheets(cleaned_data)

    print("[7] Menyimpan data ke PostgreSQL...")
    save_to_postgresql(cleaned_data)

    print("[8] ETL pipeline selesai.")

if __name__ == "__main__":
    run_etl()
