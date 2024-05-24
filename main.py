import requests
import pandas as pd
import numpy as np
import time


def calculate_grid_points_for_romania(lat_start=43.6, lat_end=48.0, lon_start=20.0, lon_end=29.7, step=0.1):
    lat_points = np.arange(lat_start, lat_end, step)
    lon_points = np.arange(lon_start, lon_end, step)
    return [(lat, lon) for lat in lat_points for lon in lon_points]


def is_in_romania(location_info):
    return "Romania" in location_info

def filter_results(results):
    return [result for result in results if is_in_romania(result.get('vicinity', ''))]

def filter_by_country(results, country='Romania'):
    filtered = [result for result in results if any(
        component for component in result['address_components'] if component['long_name'] == country)]
    return filtered

def fetch_and_save_atms(api_key, lat, lng, output_file):
    """
    Fetch ATMs near a given latitude and longitude and save results incrementally to a CSV file.
    """
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f'{lat},{lng}',
        'radius': 10000,
        'type': 'atm',
        'region': 'ro',
        'language': 'ro',
        'key': api_key
    }

    while True:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data['status'] != 'OK':
            print(f"Error fetching data: {data['status']}")
            break

        results = []

        for item in data.get('results', []):
            result = {
                'name': item.get('name', 'N/A'),
                'vicinity': item.get('vicinity', 'N/A'),
                'latitude': item.get('geometry', {}).get('location', {}).get('lat', 'N/A'),
                'longitude': item.get('geometry', {}).get('location', {}).get('lng', 'N/A')
            }
            results.append(result)

        df = pd.DataFrame(results)
        if not df.empty:
            df.to_csv(output_file, mode='a', header=not pd.read_csv(output_file).empty, index=False, encoding='utf-8')
            print(f"Saved {len(results)} ATMs to {output_file} from location ({lat}, {lng})")

        page_token = data.get('next_page_token')
        if page_token:
            print("next page")
            params['pagetoken'] = page_token
            time.sleep(10)
        else:
            break

def main():
    api_key = ''
    output_file = 'atms_romania.csv'
    grid_points = calculate_grid_points_for_romania()

    for lat, lng in grid_points:
        print(f"Starting extraction near ({lat}, {lng})")
        fetch_and_save_atms(api_key, lat, lng, output_file)

if __name__ == "__main__":
    main()

