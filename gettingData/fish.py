import requests
import pandas as pd
import io
import concurrent.futures
from bs4 import BeautifulSoup

def dms_to_decimal(dms_str):
    """Convert a string like '21 0 37 N' to decimal degrees."""
    try:
        parts = dms_str.strip().split()
        if len(parts) < 4:
            return None
        
        degrees = float(parts[0])
        minutes = float(parts[1])
        seconds = float(parts[2])
        direction = parts[3].upper()
        
        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
        if direction in ['S', 'W']:
            decimal *= -1
        return round(decimal, 4)
    except Exception:
        return None

def get_coast_weather(lat_dms, lon_dms):
    """
    Get current weather and wind conditions for a given coast using its latitude and longitude (in DMS format).
    Uses the free Open-Meteo API.
    """
    lat_dec = dms_to_decimal(lat_dms)
    lon_dec = dms_to_decimal(lon_dms)
    
    if lat_dec is None or lon_dec is None:
        return {"error": "Invalid latitude or longitude format"}
        
    url_weather = f"https://api.open-meteo.com/v1/forecast?latitude={lat_dec}&longitude={lon_dec}&current=temperature_2m,wind_speed_10m,wind_direction_10m,weather_code"
    url_marine = f"https://marine-api.open-meteo.com/v1/marine?latitude={lat_dec}&longitude={lon_dec}&current=wave_height"
    
    try:
        weather_res = requests.get(url_weather, timeout=10)
        marine_res = requests.get(url_marine, timeout=10)
        
        if weather_res.status_code == 200 and marine_res.status_code == 200:
            weather_data = weather_res.json()
            marine_data = marine_res.json()
            
            w_current = weather_data.get("current", {})
            m_current = marine_data.get("current", {})
            
            return {
                "temperature_celsius": w_current.get("temperature_2m"),
                "wind_speed_kmh": w_current.get("wind_speed_10m"),
                "wind_direction_deg": w_current.get("wind_direction_10m"),
                "weather_code": w_current.get("weather_code"),
                "wave_height_m": m_current.get("wave_height")
            }
        else:
            return {"error": f"Failed to fetch. Weather: {weather_res.status_code}, Marine: {marine_res.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def fetch_incois_data_automated():
    # The main text data page that displays the table
    url = "https://incois.gov.in/MarineFisheries/TextData?secid=SEC011"
    
    # Standard browser headers to avoid getting blocked
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-GPC": "1",
    }
    
    # Initialize a persistent session
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        # 1. First request: Hit the homepage/root portal to trigger the server 
        # to send back a fresh 'Set-Cookie: JSESSIONID=...' header.
        portal_home = "https://incois.gov.in/MarineFisheries/TextDataHome?mfid=1&request_locale=en"
        session.get(portal_home, timeout=10)
        
        # 2. Second request: Hit the actual data page. 
        # The session object automatically attaches the fresh JSESSIONID cookie acquired in Step 1.
        response = session.get(url, timeout=10)
        
        with open("incois_output.html", "w", encoding="utf-8") as f:
            f.write(response.text)
            
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            forecast_div = soup.find('div', id='forecastdata')
            if forecast_div:
                table = forecast_div.find('table')
            else:
                table = None
                
            if table:
                # Instantly parse the HTML grid table into a list of dictionaries
                df = pd.read_html(io.StringIO(str(table)))[0]
                
                # Define a helper function to process one row
                def process_row(row):
                    lat = row.get("Latitude (dms)")
                    lon = row.get("Longitude (dms)")
                    return get_coast_weather(lat, lon)
                
                # Use ThreadPoolExecutor to fetch weather for all locations concurrently
                with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
                    # Convert df.iterrows() to a list of rows
                    rows = [row for _, row in df.iterrows()]
                    # Map process_row to all rows in parallel
                    weather_results = list(executor.map(process_row, rows))
                
                temps, winds, dirs, codes, waves = [], [], [], [], []
                for weather in weather_results:
                    if weather and "error" not in weather:
                        temps.append(weather.get("temperature_celsius"))
                        winds.append(weather.get("wind_speed_kmh"))
                        dirs.append(weather.get("wind_direction_deg"))
                        codes.append(weather.get("weather_code"))
                        waves.append(weather.get("wave_height_m"))
                    else:
                        temps.append(None)
                        winds.append(None)
                        dirs.append(None)
                        codes.append(None)
                        waves.append(None)
                
                df["Temperature (C)"] = temps
                df["Wind Speed (km/h)"] = winds
                df["Wind Direction (deg)"] = dirs
                df["Weather Code"] = codes
                df["Wave Height (m)"] = waves
                
                df.to_csv("fish.csv", index=False)
                return df
            else:
                # If it's June/July, the table won't exist because of the monsoon ban text message
                if "Ban" in response.text or "ban" in response.text:
                    return {
                        "status": "Monsoon Ban Active",
                        "message": "INCOIS data feed suspended due to government fishing ban."
                    }
                return {"error": "HTML table structure not found on the page."}
        else:
            return {"error": f"Server rejected request. Status code: {response.status_code}"}
            
    except Exception as e:
        return {"error": f"Automated scraping failed: {str(e)}"}


# Test execution
if __name__ == "__main__":
    data = fetch_incois_data_automated()
    print(data)
