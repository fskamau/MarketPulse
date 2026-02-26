# 🏙️ MarketPulse: Real Estate Market Tracker

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://python.org)
[![Pandas](https://img.shields.io/badge/pandas-data%20analysis-150458.svg)](https://pandas.pydata.org/)
[![Folium](https://img.shields.io/badge/folium-geospatial%20mapping-77B829.svg)](https://python-visualization.github.io/folium/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**MarketPulse** is a Python-based geospatial analytics tool designed to scrape real estate rental/sale listings, calculate property valuations, and visualize market momentum. Instead of relying on static charts, this tool utilizes **Folium** to plot coordinates on an interactive HTML map, highlighting neighborhoods experiencing the highest price-per-square-foot growth over a 30-day rolling window.



---

## 🚀 The "Level Up"

Standard web scraping projects often dump data into a CSV or a basic Matplotlib bar chart. **MarketPulse** takes it a step further by introducing **Geospatial Data Visualization**. By mapping pandas coordinates into interactive HTML layers, users can visually pinpoint where market inflation or deflation is occurring at a granular, neighborhood level.

## 🛠️ Tech Stack & Features

| Tool | Role in Project | Description |
| :--- | :--- | :--- |
| **BeautifulSoup4** | Data Extraction | Parses target real estate sites to extract pricing, square footage, and location tags. |
| **Pandas** | Data Engineering | Cleans unstructured data, calculates Price-Per-SqFt, and computes 30-day percentage growth. |
| **Folium** | Geospatial UI | Translates latitude/longitude coordinates into interactive markers and heatmaps. |

* **Metric Engine:** Automatically standardizes property prices by calculating `$ / sq. ft.`
* **Time-Series Analysis:** Compares current listing batches against 30-day historical data.
* **Smart Mapping:** Color-codes map markers dynamically based on growth percentages (e.g., green for high appreciation).

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/fskamau/MarketPulse.git
   cd MarketPulse
   pip install -r requirements.txt
   python main.py
   ```