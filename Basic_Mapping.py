import folium
from folium.plugins import AntPath
from geopy.geocoders import Nominatim
import webbrowser
import os
from datetime  import timedelta ,datetime
import random

def generate_random_time():
    base_date = datetime(2024, 10, 29)
    random_seconds = random.randint(0, 86400)
    random_time = base_date + timedelta(seconds=random_seconds)
    return random_time.strftime("%Y-%m-%d %H:%M:%S")

locations = ["adyar", "thiruvanmiyur", "santhome"]

map_center = [13.5, 78.5]
mymap = folium.Map(location=map_center, zoom_start=7)

geolocator = Nominatim(user_agent="location_mapper")
s=list()
for location_name in locations:
   
    location = geolocator.geocode(location_name)
    a=(location.latitude, location.longitude)
    s.append(a)
    if location:
        folium.Marker(
            [location.latitude, location.longitude],
            popup=folium.Popup(f'{location_name} '+" "+generate_random_time(),max_width=500),
            icon=folium.Icon(icon='person',icon_color='white',prefix='fa',color='red'),
            tooltip=location_name +" "+generate_random_time()            
        ).add_to(mymap)
        
        
folium.PolyLine(locations=s,weight=2,color='red').add_to(mymap)
path=s
AntPath(path,delay=400,weight=3,color='red',dash_array=[20,15],pulse_array='orange').add_to(mymap)
file_path = "locationsmap.html"
mymap.save(file_path)

print(s)


webbrowser.open('file://' + os.path.realpath(file_path))
