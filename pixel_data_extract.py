import rasterio
import pandas as pd

# Function to extract pixel values from a GeoTIFF file
def extract_pixel_values(geotiff_file):
    with rasterio.open(geotiff_file) as src:
        data = src.read(1)  # Assuming a single-band raster, change index if necessary
    return data

# Paths to your GeoTIFF files
svi_filepath = 'tifs\\med_res_svi_2020_wgs84_nopop.tif'
pd_filepath = 'tifs\\med_res_usa_pd_2020.tif'

# Extract pixel values from both GeoTIFF files
svi_values = extract_pixel_values(svi_filepath)
pd_values = extract_pixel_values(pd_filepath)

# Initialize an empty pandas DataFrame to store pixel values
df = pd.DataFrame(columns=['Pixel_i', 'Pixel_j', 'SVI', 'PD'])

# Iterate through each pixel and store its values in the DataFrame
for i in range(0, svi_values.shape[0] - 1, 5):
    for j in range(0, svi_values.shape[1] - 1, 5):
        value1 = svi_values[i, j]
        value2 = pd_values[i, j]
        if value1 == float(-3.3999999521443642e+38):
            value1 = 0
        if value2 == -99999:
            value2 = 0
        if value1 != 0 and value2 != 0:
            df = df._append({'Pixel_i': i, 'Pixel_j': j, 'SVI': value1, 'PD': value2}, ignore_index=True)

# Save the DataFrame as a CSV file
df.to_csv('pixel_values.csv', index=False)
