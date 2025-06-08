import pandas as pd
from datetime import datetime

def transform_to_DataFrame(data):
    try:
        df = pd.DataFrame(data)
        return df
    
    except Exception as e:
        print(f"Error creating DataFrame: {e}")
        return pd.DataFrame()

def transform_data(data, exchange_rate):
    try:
        # Tambahkan timestamp ekstraksi
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['Extraction Timestamp'] = timestamp
        
        # Hapus baris dengan Title "Unknown Product"
        data = data[~data['Title'].str.contains("Unknown Product", na=False)]
        
        # Hapus baris dengan Rating "Invalid Rating"
        data = data[~data['Rating'].astype(str).str.contains("Invalid Rating", na=False)]

        # Hapus baris dengan Price "Invalid Price"
        data = data[~data['Price'].astype(str).str.contains("Price Unavailable", na=False)]
        
        # Menghapus baris yang nilainya dupliklat
        data = data.drop_duplicates()
        
        # Menghapus baris yang nilainya null
        data = data.dropna()
        
        # Tranformasi Price (menghapus simbol '$', dan konversi ke float)
        data['Price'] = data['Price'].replace('\\$', '', regex=True).astype(float) * exchange_rate
        
        # Tranformasi Rating (menghapus '/' dan spasi)
        data['Rating'] = data['Rating'].str.extract(r'(\d+\.\d+)').astype(float)
        
        # Tranformasi Colors (menghapus kata 'Colors' dan spasi)
        data['Colors'] = data['Colors'].replace('Colors', '', regex=True).str.strip()
        data['Colors'] = data['Colors'].astype('int64')
        
        # Tranformasi Size (menghapus kata 'Size:' dan spasi)
        data['Size'] = data['Size'].replace('Size:', '', regex=True).str.strip()
        
        # Tranformasi Gender (menghapus kata 'Gender:' dan spasi)
        data['Gender'] = data['Gender'].replace('Gender:', '', regex=True).str.strip()
        
        # Transformasi Tipe Data
        data['Title'] = data['Title'].astype('object') 
        data['Price'] = data['Price'].astype('float64') 
        data['Rating'] = data['Rating'].astype('float64') 
        data['Colors'] = data['Colors'].astype('int64') 
        data['Size'] = data['Size'].astype('object') 
        data['Gender'] = data['Gender'].astype('object') 
        
        return data

    except KeyError as e:
        print(f"Column error: {e}")
        
    except ValueError as e:
        print(f"Value conversion error: {e}")
        
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return pd.DataFrame()