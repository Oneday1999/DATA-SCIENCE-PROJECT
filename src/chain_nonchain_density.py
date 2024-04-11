import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import math
import numpy as np
from folium.plugins import HeatMap
import folium
import pandas as pd
from folium import plugins
import matplotlib.pyplot as plt
from math import *


def get_all_restaurant_chains():
    restaurant_chains_list = []
    canadian_restaurant_chains_url = 'https://en.wikipedia.org/wiki/List_of_Canadian_restaurant_chains'
    chains_html = urllib.request.urlopen(canadian_restaurant_chains_url).read().decode('utf-8')
    chains_html_soup = BeautifulSoup(chains_html, 'html.parser')
    answers = chains_html_soup.find_all('span', class_='mw-headline')
    for restaurant in answers:
        text = restaurant.get_text()
        if text == "See also" or text == "References":
            continue
        restaurant_chains_list.append(text)
    return restaurant_chains_list


all_restaurant_chains = get_all_restaurant_chains()
raw_amen_data = pd.read_json('amenities-vancouver.json.gz', lines=True, compression='gzip')
all_restaurant_df = raw_amen_data.loc[raw_amen_data.amenity == "restaurant", :]
data_map = folium.Map(location=[49.284808779798745, -123.12244539679432], zoom_start=10)
chain_data_map = folium.Map(location=[49.284808779798745, -123.12244539679432], zoom_start=10)
location = []
chain_location = []
for index, row in all_restaurant_df.iterrows():
    location.append([row['lat'], row['lon']])
    if row["name"] in all_restaurant_chains:
        chain_location.append([row['lat'], row['lon']])
data_map.add_child(plugins.HeatMap(location, blur=28))
data_map.save(outfile="../result/all_restaurant_heatmap.html")
chain_data_map.add_child(plugins.HeatMap(chain_location, blur=28))
chain_data_map.save(outfile="../result/all_chains_restaurant_heatmap.html")


def in_chain_restaurants(item):
    if item in all_restaurant_chains:
        return True
    else:
        return False


chain_df = all_restaurant_df[all_restaurant_df['name'].apply(in_chain_restaurants)]
nonchain_df = all_restaurant_df[~all_restaurant_df['name'].apply(in_chain_restaurants)]

plt.xlabel('longitude')
plt.ylabel('latitude')
plt.title('Distribution of Restaurants in Vancouver')
plt.scatter(nonchain_df['lon'], nonchain_df['lat'], c="orange", s=10)
plt.scatter(chain_df['lon'], chain_df['lat'], c="purple", s=10)
plt.legend(['non-chain', 'chain'])
strFile = "../result/restaurant_density.jpg"
plt.savefig(strFile)
plt.close()
