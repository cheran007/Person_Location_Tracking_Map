import folium
from folium.plugins import AntPath
from geopy.geocoders import Nominatim
from datetime import timedelta, datetime
import random
import webbrowser ,os

def generate_random_time():
    base_date = datetime(2024, 10, 29)
    random_seconds = random.randint(0, 86400)
    random_time = base_date + timedelta(seconds=random_seconds)
    return random_time.strftime("%Y-%m-%d %H:%M:%S")

def map(locations, map_center):
    list_of_coordinates = []
    value = []
    mymap = folium.Map(location=map_center, zoom_start=7)
    geolocator = Nominatim(user_agent="location_mapper")
    
    for location_name in locations:
        location = geolocator.geocode(location_name)
        if location:
            coordinates = (location.latitude, location.longitude)
            list_of_coordinates.append(coordinates)
            times = generate_random_time()
            
            folium.Marker(
                coordinates,
                popup=folium.Popup(f'{location_name} {times}', max_width=500),
                icon=folium.Icon(icon='person', icon_color='white', prefix='fa', color='red'),
                tooltip=location_name + " " + times
            ).add_to(mymap)
            
            dict1 = {
                'Location': location_name,
                'Lat_and_Lon': coordinates,
                'time': times
            }
            value.append(dict1)
    
   
    current_time = datetime.now()
    sorted_locations = sorted(
        value,
        key=lambda x: abs(current_time - datetime.strptime(x['time'], "%Y-%m-%d %H:%M:%S")),
        reverse=True 
    )
    
    ordered_coordinates = [location['Lat_and_Lon'] for location in sorted_locations]
    print("Ordered Coordinates (Farthest to Nearest):", ordered_coordinates)
    
    # Add polyline and animated path
    folium.PolyLine(locations=ordered_coordinates, weight=2, color='red').add_to(mymap)
    AntPath(ordered_coordinates, delay=400, weight=3, color='red', dash_array=[20, 15], pulse_color='white').add_to(mymap)
    folium.Marker(location=ordered_coordinates[-1],
                  icon=folium.Icon(icon='person', icon_color='white', prefix='fa', color='green'),).add_to(mymap)
    
    file_path = "locationsmap.html"
    mymap.save(file_path)
    return file_path

if __name__ == '__main__':
    locations = ["adyar", "thiruvanmiyur", "santhome"]
    map_center = [13.5, 78.5]
    file_name = map(locations, map_center)
    webbrowser.open('file://' + os.path.realpath(file_name))
