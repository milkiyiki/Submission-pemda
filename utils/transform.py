import pandas as pd
import re

def clean_price(price_str):
    try:
        # Contoh: $12.99
        price_float = float(price_str.replace("$", "").strip())
        return int(price_float * 16000)
    except:
        return None

def clean_rating(rating_str):
    try:
        # Contoh: "4.8 / 5"
        match = re.match(r"(\d+(\.\d+)?)", rating_str)
        return float(match.group(1)) if match else None
    except:
        return None

def clean_colors(colors_str):
    try:
        # Contoh: "3 Colors" → 3
        match = re.match(r"(\d+)", colors_str)
        return int(match.group(1)) if match else None
    except:
        return None

def clean_size(size_str):
    return size_str.replace("Size: ", "").strip()

def clean_gender(gender_str):
    return gender_str.replace("Gender: ", "").strip()

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Bersihkan kolom satu per satu
    df["Price"] = df["Price"].apply(clean_price)
    df["Rating"] = df["Rating"].apply(clean_rating)
    df["Colors"] = df["Colors"].apply(clean_colors)
    df["Size"] = df["Size"].apply(clean_size)
    df["Gender"] = df["Gender"].apply(clean_gender)

    # Drop data yang invalid
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    df = df[df["Title"].str.lower() != "unknown product"]

    # Pastikan tipe data
    df = df.astype({
        "Title": str,
        "Price": int,
        "Rating": float,
        "Colors": int,
        "Size": str,
        "Gender": str,
        "Timestamp": str
    })

    return df
