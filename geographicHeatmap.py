# CREATING GEOGRAPHIC HEATMAP OF GOFUNDME FUNDRAISERS

from geopy.geocoders import Nominatim
import pandas as pd
import folium
from folium.plugins import HeatMap
import time

df = pd.read_csv('GoFundMe-Data.csv')

geolocator = Nominatim(user_agent="gofundme")

locations = df['Location'].tolist()
coordinates = []

for l in locations:
    location = geolocator.geocode(l)
    if location != None:
        coordinates.append((location.latitude, location.longitude))

df = pd.DataFrame(coordinates, columns=['Lat', 'Lon'])

df.to_csv('GoFundMe-Coordinates.csv', index=False)

time.sleep(5)

df = pd.read_csv('GoFundMe-Coordinates.csv')
lat = df['Lat'].tolist()
lon = df['Lon'].tolist()
coordinates = []

for i in range(len(lat)):
    coordinates.append((lat[i], lon[i]))

m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

HeatMap(coordinates).add_to(m)

m.save('GoFundMe-Heatmap.html')