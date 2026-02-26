import pandas as pd
import folium
from folium.plugins import HeatMap
from bs4 import BeautifulSoup
import requests
import datetime
import os

# ==========================================
# 1. SCRAPING MODULE (BeautifulSoup)
# ==========================================
def scrape_listings(url):
    """
    Template for scraping real estate listings.
    Note: Most commercial real estate sites require headers or Selenium to bypass bot protection.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # Mocking the scraped data for demonstration purposes
    # In a real scenario, you would parse the HTML using BeautifulSoup:
    # response = requests.get(url, headers=headers)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # listings = soup.find_all('div', class_='listing-card')
    
    print("[*] Scraping data from target URL...")
    
    mock_data = [
        {"id": 1, "neighborhood": "Downtown", "price": 450000, "sqft": 800, "lat": 40.7128, "lon": -74.0060, "date": "2023-10-01"},
        {"id": 2, "neighborhood": "Uptown", "price": 850000, "sqft": 1200, "lat": 40.7306, "lon": -73.9866, "date": "2023-10-01"},
        {"id": 3, "neighborhood": "Midtown", "price": 600000, "sqft": 950, "lat": 40.7549, "lon": -73.9840, "date": "2023-10-01"},
        {"id": 4, "neighborhood": "Downtown", "price": 480000, "sqft": 800, "lat": 40.7130, "lon": -74.0070, "date": "2023-10-31"}, # 30 days later
        {"id": 5, "neighborhood": "Uptown", "price": 840000, "sqft": 1200, "lat": 40.7310, "lon": -73.9870, "date": "2023-10-31"}, # 30 days later
        {"id": 6, "neighborhood": "Midtown", "price": 650000, "sqft": 950, "lat": 40.7550, "lon": -73.9850, "date": "2023-10-31"}  # 30 days later
    ]
    
    return pd.DataFrame(mock_data)

# ==========================================
# 2. ANALYSIS MODULE (Pandas)
# ==========================================
def analyze_market(df):
    """
    Calculates price-per-square-foot and 30-day neighborhood price growth.
    """
    print("[*] Analyzing market data with Pandas...")
    
    # Calculate Price per Square Foot
    df['price_per_sqft'] = df['price'] / df['sqft']
    df['date'] = pd.to_datetime(df['date'])
    
    # Separate into 'historical' (30 days ago) and 'current'
    min_date = df['date'].min()
    max_date = df['date'].max()
    
    historical_df = df[df['date'] == min_date].groupby('neighborhood')['price_per_sqft'].mean().reset_index()
    historical_df.rename(columns={'price_per_sqft': 'old_price_sqft'}, inplace=True)
    
    current_df = df[df['date'] == max_date].groupby('neighborhood')['price_per_sqft'].mean().reset_index()
    current_df.rename(columns={'price_per_sqft': 'new_price_sqft'}, inplace=True)
    
    # Merge and calculate growth percentage
    growth_df = pd.merge(historical_df, current_df, on='neighborhood')
    growth_df['growth_pct'] = ((growth_df['new_price_sqft'] - growth_df['old_price_sqft']) / growth_df['old_price_sqft']) * 100
    
    # Merge growth data back with current coordinates for mapping
    map_data = df[df['date'] == max_date].merge(growth_df[['neighborhood', 'growth_pct']], on='neighborhood')
    
    # Identify top neighborhood
    top_neighborhood = growth_df.loc[growth_df['growth_pct'].idxmax()]
    print(f"\n[!] HOTSPOT DETECTED: {top_neighborhood['neighborhood']} with {top_neighborhood['growth_pct']:.2f}% growth in 30 days!\n")
    
    return map_data

# ==========================================
# 3. GEOSPATIAL VISUALIZATION (Folium)
# ==========================================
def generate_map(df, output_file="map.html"):
    """
    Plots real estate listings on an interactive map.
    Colors indicate price growth (Green = Growth, Red = Decline).
    """
    print("[*] Generating interactive Folium map...")
    
    # Center map on the average coordinates
    center_lat = df['lat'].mean()
    center_lon = df['lon'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles="CartoDB positron")
    
    for _, row in df.iterrows():
        # Determine marker color based on growth
        if row['growth_pct'] > 5:
            color = 'darkgreen'
            icon_type = 'arrow-up'
        elif row['growth_pct'] > 0:
            color = 'lightgreen'
            icon_type = 'arrow-up'
        else:
            color = 'red'
            icon_type = 'arrow-down'
            
        popup_html = f"""
        <b>{row['neighborhood']}</b><br>
        Price: ${row['price']:,.0f}<br>
        Price/SqFt: ${row['price_per_sqft']:,.2f}<br>
        30-Day Growth: {row['growth_pct']:,.2f}%
        """
        
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{row['neighborhood']} Listing",
            icon=folium.Icon(color=color, icon=icon_type, prefix='fa')
        ).add_to(m)

    m.save(output_file)
    print(f"[*] Map successfully saved to {os.path.abspath(output_file)}")

# ==========================================
# EXECUTION
# ==========================================
if __name__ == "__main__":
    TARGET_URL = "https://example-real-estate-site.com/listings"
    
    raw_data = scrape_listings(TARGET_URL)
    analyzed_data = analyze_market(raw_data)
    generate_map(analyzed_data)