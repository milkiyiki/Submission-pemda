from utils.extract import scrape_fashion
from utils.transform import transform_to_DataFrame, transform_data
from utils.load import store_to_postgre, store_to_csv, store_to_sheets

def main():
    BASE_URL = 'https://fashion-studio.dicoding.dev/page{}'
    all_fashion_data = scrape_fashion(BASE_URL)
    
    if all_fashion_data:
        try:
            DataFrame = transform_to_DataFrame(all_fashion_data)
            DataFrame = transform_data(DataFrame, 16000)
            
            db_url = 'postgresql+psycopg2://postgres:postgres@localhost:5432/fashiondb'
            
            store_to_csv(DataFrame)
            store_to_postgre(DataFrame, db_url)
            store_to_sheets(DataFrame)

            print()
            print('-' * 20)
            print()

            print(DataFrame.info())

        except Exception as e:
            print(f"Terjadi kesalahan dalam proses: {e}")
    else:
        print("Tidak ada data yang ditemukan.")

if __name__ == '__main__':
    main()