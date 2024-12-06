import pandas as pd
import numpy as np
from datetime import datetime
import re

def clean_vehicle_data(file_path):
    # Load data
    df = pd.read_csv(file_path)
    print(f"Initial data shape: {df.shape}")
    
    # Show actual column names
    print("\nActual columns in file:")
    print(df.columns.tolist())
    
    # Select and rename critical columns - using actual column names from your file
    critical_columns = {
        'Price': 'price',
        'Kilométrage': 'kilometrage',
        'Boite': 'transmission',
        'Année': 'year',
        'Cylindrée': 'engine_size',
        'Marque': 'brand',
        'Modèle': 'model',
        'Puissance fiscale': 'power',
        'Carburant': 'fuel'
    }
    
    # Clean data
    df = df[list(critical_columns.keys())].rename(columns=critical_columns)
    
    # Clean numeric values
    df['price'] = pd.to_numeric(df['price'].astype(str).str.replace(r'[^\d.]', ''), errors='coerce')
    df['kilometrage'] = pd.to_numeric(df['kilometrage'].astype(str).str.replace(r'[^\d.]', ''), errors='coerce')
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    
    # Clean engine size
    df['engine_size'] = df['engine_size'].replace({'>4.0L': '4.0', '<1.0L': '1.0'})
    df['engine_size'] = df['engine_size'].str.extract(r'(\d+\.?\d*)').astype(float)
    
    # Clean power
    df['power'] = pd.to_numeric(df['power'].replace('0000', np.nan), errors='coerce')
    
    # Clean categorical values
    df['transmission'] = df['transmission'].str.lower()
    df['fuel'] = df['fuel'].str.lower()
    df['brand'] = df['brand'].str.strip().str.title()
    df['model'] = df['model'].str.strip().str.title()
    
    # Validation filters
    df = df[
        (df['price'].between(1000, 1000000)) &
        (df['kilometrage'].between(0, 500000)) &
        (df['year'].between(1950, 2024)) &
        (df['engine_size'].between(0.5, 6.0)) &
        (df['power'].between(3, 20)) &
        (df['transmission'].isin(['automatique', 'manuelle'])) &
        (df['fuel'].isin(['essence', 'diesel', 'hybride', 'électrique']))
    ]
    
    # Drop any remaining missing values
    df = df.dropna()
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    print(f"\nFinal data shape: {df.shape}")
    
    # Save cleaned data
    output_path = 'cleaned_vehicle_data.csv'
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to: {output_path}")
    
    return df

if __name__ == "__main__":
    cleaned_df = clean_vehicle_data('vehicle_data.csv')