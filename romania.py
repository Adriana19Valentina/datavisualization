import numpy as np

def calculate_grid_points_for_romania(lat_start=43.6, lat_end=48.0, lon_start=20.0, lon_end=29.7, lat_step=0.18, lon_step=0.12):
    """
    Generate grid points within the bounding box of Romania.
    Adjust lat_step and lon_step according to the radius used in the Places API search.
    """
    lat_points = np.arange(lat_start, lat_end, lat_step)
    lon_points = np.arange(lon_start, lon_end, lon_step)
    grid_points = [(lat, lon) for lat in lat_points for lon in lon_points]
    return grid_points

# Example usage
grid_points = calculate_grid_points_for_romania()
print(f"Generated {len(grid_points)} grid points.")
print(len(grid_points))