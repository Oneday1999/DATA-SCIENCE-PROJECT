# DATA-SCIENCE-PROJECT 353

# Firstly, the file ODbus_v1.csv must be decompressed in the src folder before the program runs! Since the file is >25MB, we had to compress it to facilitate uploading.

# Extra packages requirement (assuming you are running with Anaconda)
1) pip install gpsphoto
2) pip install exifread
3) pip install piexif
4) pip install geojson
5) pip install folium

# Running main application
1) open terminal with path to the "src" folder
2) Method 1
run: py choose_hotel.py imagename
Sample code:
python choose_hotel.py img1.jpg
# Viewing the result
in the result folder, can open the result file amenity_near_hotel.html in chrome.
3) Method 2
run: py chain_nonchain_density.py
# Viewing the result 
in the result folder, can open the result file all_restaurant_heatmap.html,all_chains_restaurant_heatmap.html and restaurant_density.jpg  in chrome.


# Datasource
The ODBus_v1.csv file is downloading from https://www150.statcan.gc.ca/n1/pub/21-26-0003/212600032023001-eng.htm
