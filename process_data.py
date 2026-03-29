import pandas as pd

def load_and_filter_data(csv_path):
    print("Loading the massive SFpark dataset... (This might take a minute)")
    
    # Load the data
    df = pd.read_csv(csv_path)
    
    print(f"Original dataset rows: {len(df)}")
    
    # Filter out empty rows or corrupted sensor data
    df = df.dropna(subset=['OCCUPIED_SPACES', 'TOTAL_SPACES'])
    
    # Calculate the availability percentage (Heuristic for ACO)
    df['AVAILABILITY_RATE'] = (df['TOTAL_SPACES'] - df['OCCUPIED_SPACES']) / df['TOTAL_SPACES']
    
    # Let's filter to a specific street from our micro-map as a test
    # (e.g., 'BUSH ST' which runs right through our map area)
    micro_map_data = df[df['STREET_NAME'].str.contains('BUSH ST', na=False)]
    
    print(f"Filtered micro-map rows: {len(micro_map_data)}")
    print("\n--- Sample Data ---")
    print(micro_map_data[['STREET_NAME', 'DATE', 'TIME', 'AVAILABILITY_RATE']].head())
    
    return micro_map_data

if __name__ == "__main__":
    filtered_df = load_and_filter_data('synthetic_sfpark_data.csv')
