from GPSPhoto import gpsphoto
import pandas as pd
from math import radians, cos, sin, asin, sqrt
import folium
import warnings
import os
warnings.filterwarnings("ignore")

def geodistance(lng1, lat1, lng2, lat2):
    # lng1,lat1,lng2,lat2 = (120.12802999999997,30.28708,115.86572000000001,28.7427)
    lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)])
    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    distance = 2 * asin(sqrt(a)) * 6371 * 1000
    return distance


def extractGPSFromImage(filename):
    data = gpsphoto.getGPSData(filename)
    latitude = data['Latitude']
    longitude = data['Longitude']
    return (latitude, longitude)


image_name = input("Please input the filename of image:")
image_name = "../photo_img/"+image_name
if not os.path.exists(image_name):
    print("The image file does not exist.")
    exit(-1)

amenity_recode_dict = {'parking_entrance': 'parking',
                       'pub': 'bar',
                       'childcare': 'kindergarten',
                       'nightclub': 'bar',
                       'gambling': 'casino',
                       'motorcycle_parking': 'parking',
                       'drinking_water': 'fountain',
                       'doctors': 'hospital',
                       'storage': 'storage_rental',
                       'internet_cafe': 'cafe',
                       'chiropractor': 'hospital',
                       'post_depot': 'post_office',
                       'Pharmacy': 'pharmacy',
                       'ferry_terminal': 'bus_station',
                       'car_rental': 'traffic',
                       'car_sharing': 'traffic',
                       'bicycle_rental': 'traffic',
                       'taxi': 'traffic',
                       'boat_rental': 'traffic',
                       'food_court': 'restaurant',
                       'motorcycle_rental': 'traffic'}
amenity_group_dict = {'cafe': 'food',
                      'restaurant': 'food',
                      'fast_food': 'food',
                      'traffic': 'transportation',
                      'parking': 'transportation',
                      'bus_station': 'transportation',
                      'pub': 'entertainment',
                      'cinema': 'entertainment',
                      'bar': 'entertainment',
                      'atm': 'shop',
                      'bank': 'shop',
                      'marketplace': 'shop'}
raw_amen_data = pd.read_json('amenities-vancouver.json.gz', lines=True, compression='gzip')
processed_data = raw_amen_data
processed_data['amenity_new'] = processed_data['amenity'].replace(amenity_recode_dict)
processed_data['amenity_group'] = processed_data['amenity_new'].replace(amenity_group_dict)

image_lat, image_lon = extractGPSFromImage(image_name)
van_map = folium.Map(location=[image_lat, image_lon], zoom_start=12)
folium.Marker(
    location=[image_lat, image_lon],
    popup="My position",
    icon=folium.Icon(color="red", icon="info-sign"),
).add_to(van_map)

for index, row in processed_data.iterrows():
    if row["amenity"] in amenity_group_dict:
        group_name = amenity_group_dict[row["amenity"]]
        group_color = ""
        if group_name == "food":
            group_color = "red"
        elif group_name == "transportation":
            group_color = "blue"
        elif group_name == "entertainment":
            group_color = "yellow"
        elif group_name == "shop":
            group_color = "green"
        folium.Circle(
            radius=6,
            location=[row['lat'], row['lon']],
            color=group_color,
        ).add_to(van_map)

all_businesses = pd.read_csv("ODBus_v1.csv")
all_hotels =all_businesses.loc[all_businesses.city=="Vancouver",:]
all_hotels=all_hotels.loc[all_hotels.business_sector=="Hotel",:]


for index, row in all_hotels.iterrows():
    if row["latitude"]==".." or row["longitude"]=="..":
        continue
    hotel_lat = float(row["latitude"])
    hotel_lon = float(row["longitude"])
    dist = geodistance(image_lon,image_lat,hotel_lon,hotel_lat)
    if dist < 500:
        folium.Marker([row["latitude"], row["longitude"]], popup=row["business_name"]).add_to(van_map)


van_map.save(outfile="../result/amenity_near_hotel.html")
