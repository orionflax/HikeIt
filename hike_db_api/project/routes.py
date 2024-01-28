from flask import Blueprint, jsonify, request,make_response
from project.models import Routes
from project.util import *
from flask import jsonify
import math
from pyproj import CRS, Transformer
from .util import calculate_overall_hiking_difficulty,weather_difficulty,convert_object_to_JSON

def convert_osgb36_to_wgs84(easting, northing):
    # Define the projection for OSGB36 using the new CRS class
    crs_osgb36 = CRS("EPSG:27700")

    # Define the projection for WGS84
    crs_wgs84 = CRS("EPSG:4326")

    # Create a transformer object for converting between OSGB36 and WGS84
    transformer = Transformer.from_crs(crs_osgb36, crs_wgs84)

    # Perform the transformation
    lon, lat = transformer.transform(easting, northing)
    return lon, lat


bp = Blueprint('routes', __name__)

@bp.route('/home', methods=['GET'])
def send_csrf_token():
    return (jsonify(success=True))

def haversine_distance(coord1, coord2):
    print(coord1,coord2)
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [coord1[1], coord1[0], coord2[1], coord2[0]])

    # Haversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) 
    radius_earth = 6371  # Radius of Earth in kilometers.
    distance = radius_earth * c
    return distance

@bp.route('/submitForm',methods=['POST'])
def process_form():
    if request.json is None:
        return jsonify({"msg": "Missing JSON in request"}), 400
    print(request.json)
    valid_routes = []
    diffs = []
    weather_datas = []
    route_distances = []
    route_ascents = []
    all_routes = Routes.query.all()
    for route in all_routes:
        distance =  haversine_distance([route.average_location[0],route.average_location[1]],[request.json.get('location')['latitude'],request.json.get('location')['longitude']]) 
        print(distance, f"from here to {route.name} ")
        if distance > 5:
            pass
        else:
            valid_routes.append(convert_object_to_JSON(route))
            weather_diff,weather_data = weather_difficulty(route.average_location[0],route.average_location[1])
            diff = calculate_overall_hiking_difficulty(route.distance,route.ascent,weather_diff)
            diffs.append(diff)
            route_distances.append(route.distance)
            route_ascents.append(route.ascent)
            weather_datas.append(weather_data)
    return(jsonify({"routes":valid_routes,"diff":diffs,"weather":weather_datas}))

