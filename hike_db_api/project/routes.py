from flask import Blueprint, jsonify, request,make_response
from project.models import Routes
from project.util import *
from flask import jsonify
import math
from pyproj import CRS, Transformer

def convert_osgb36_to_wgs84(easting, northing):
    # Define the projection for OSGB36 using the new CRS class
    crs_osgb36 = CRS("EPSG:27700")

    # Define the projection for WGS84
    crs_wgs84 = CRS("EPSG:4326")

    # Create a transformer object for converting between OSGB36 and WGS84
    transformer = Transformer.from_crs(crs_osgb36, crs_wgs84)

    # Perform the transformation
    lon, lat = transformer.transform(easting, northing)
    return lat, lon


bp = Blueprint('routes', __name__)

@bp.route('/home', methods=['GET'])
def send_csrf_token():
    return (jsonify(success=True))

def haversine_distance(coord1, coord2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians


    # Haversine formula
    dlon = coord1[1] - coord2[1] 
    dlat = coord1[0] - coord2[0] 
    a = math.sin(dlat/2)**2 + math.cos(coord1[0]) * math.cos(coord2[0]) * math.sin(dlon/2)**2
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
    all_routes = Routes.query.all()
    for route in all_routes:
        if haversine_distance(convert_osgb36_to_wgs84(route.average_location[0],route.average_location[1]),[request.json.get('latitude'),request.json.get('longitude')]) > request.json.get('radius'):
            pass
            print(0,route.name)
        else:
            print(1,route.name)
            valid_routes.append(route)
    print(valid_routes)


    return(jsonify(success=True))