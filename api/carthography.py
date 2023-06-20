import folium

def map_rectangular_area(
    bbox: list,
    zoom_start: int = 13,
    tileset:str = 'cartodbpositron'
) -> folium.Map:
    '''
    maps a rectangular area using the folium mapper with the leaflet.js backend
    this method accepts the following arguments:
    * bbox: list of coordinates in the form `Latitude1, Longitude1, Latitude2, Longitude2`
    * zoom_start: integer value controlling the starting zoom factor
    * tileset:  "OpenStreetMap", "Mapbox Bright" (Limited levels of zoom for free tiles), "Mapbox Control Room" (Limited levels of zoom for free tiles), "Stamen" (Terrain, Toner, and Watercolor), "Cloudmade" (Must pass API key), "Mapbox" (Must pass API key), "CartoDB" (positron and dark_matter) [taken from Folium.folium.py]

    this method returns a `Folium map object` for further processing
    '''
    location = preprocess_bbox(bbox= bbox)
    map_object = folium.Map(
        location= location,
        tiles= tileset,
        zoom_start= zoom_start
    )
    return map_object

def map_route(
    locations: list,
    map_object: folium.Map
) -> folium.Map:
    '''
    mapping a route based on processed routing coordinates 
    for turning directions and an overloaded map_object
    returns a `Folium map object` with a polyline vector_layer
    '''
    reversed_locations = preprocess_coordinates(
        coordinates= locations
    )
    polyline_obj = folium.PolyLine(
        locations= reversed_locations
    )
    polyline_obj.add_to(
        map_object
    )
    return map_object, polyline_obj

def preprocess_bbox(
    bbox: list
) -> list:
    '''
    accepts a bbox including the following elements as a list of float-values:
    `Latitude1, Longitude1, Latitude2, Longitude2` 
    to return a list of 2 elements including `Longitude1, Latitude2`
    for further processing for mapping a rectangular area
    '''
    return bbox[1:3]
    

def preprocess_coordinates(
    coordinates: list
) -> list:
    '''
    accepts a list of coordinates for turning navigation directions;
    reverses order in latitude and longitude for every element;
    returns a processed reversed list for further processing and mapping
    '''
    reversed_coords = []
    for co_el in coordinates:
        reversed_el = list(reversed(co_el))
        reversed_coords.append(reversed_el)
    return reversed_coords


def add_marker_to_map(
    map_object,
    coordinates,
    text
):
    folium.Marker(
        location=list(reversed(coordinates)), 
        popup=folium.Popup("ID: {}".format(text))
    ).add_to(map_object)
    return map_object