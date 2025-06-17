from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def store_to_csv(df):
    try:
        df.to_csv('products.csv', index=False)
        print("[CSV] Data berhasil disimpan ke file: products.csv")
    except Exception as error:
        print(f"[CSV] Gagal menyimpan data: {error}")

def store_to_postgre(df, db_connection_url):
    try:
        engine = create_engine(db_connection_url)
        print("[PostgreSQL] Kolom DataFrame:", df.columns.tolist())

        with engine.begin() as conn:
            df.to_sql('fashiontoscrape', con=conn, if_exists='append', index=False)

        print("[PostgreSQL] Data berhasil ditambahkan ke tabel fashiontoscrape")
    except Exception as error:
        print(f"[PostgreSQL] Gagal menyimpan data: {error}")

def store_to_sheets(df):
    SERVICE_ACCOUNT_PATH = './google-sheets-api.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SHEET_ID = '1VnhY63XXDprPOX5g6m5VM7TFso1GLlavUmk-tqXdDOo'
    TARGET_RANGE = 'Sheet1!A2'  # Pastikan header sudah ada di A1

    try:
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_PATH, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        sheet_api = service.spreadsheets()

        values = df.values.tolist()
        print("[Google Sheets] Jumlah baris yang akan diunggah:", len(values))
        print("[Google Sheets] Data pertama:", values[0] if values else "Tidak ada data")

        body = {'values': values}

        result = sheet_api.values().update(
            spreadsheetId=SHEET_ID,
            range=TARGET_RANGE,
            valueInputOption='RAW',
            body=body
        ).execute()

        print(f"[Google Sheets] {result.get('updatedRows', 0)} baris diperbarui.")
        print(f"[Google Sheets] Data berhasil diunggah! https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
    
    except Exception as error:
        print(f"[Google Sheets] Gagal menyimpan data: {error}")