import requests

def fetch_weather(api_key, latitude, longitude):
    """
    Fetch weather data from OpenWeatherMap API for given coordinates.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

def calculate_hiking_difficulty(weather_data):
    """
    Calculate hiking difficulty based on weather conditions.
    """
    temperature = weather_data['main']['temp']
    wind_speed = weather_data['wind']['speed']
    precipitation = 0 if 'rain' not in weather_data else weather_data['rain'].get('1h', 0)

    difficulty = 0

    # Add difficulty points based on various weather conditions
    if temperature < 5 or temperature > 25:
        difficulty += 0.75
    if wind_speed > 30:
        difficulty += 2
    if precipitation > 1:
        difficulty += 1.5

    return difficulty

def weather_difficulty( latitude, longitude):
    """
    Determine the hiking difficulty based on current weather.
    """
    weather_data = fetch_weather(api_key, latitude, longitude)
    difficulty = calculate_hiking_difficulty(weather_data)
    return difficulty,weather_data

def calculate_overall_hiking_difficulty(distance_km, ascent_meters, weather_difficulty):
    """
    Calculate the overall difficulty of a hike based on distance, ascent, and weather difficulty.
    The output is normalized to be a score between 0 and 5.
    """
    # Normalize the distance: Assume a 20km hike is medium difficulty (2.5)
 # Calculate the average gradient in percentage
    gradient = (ascent_meters / (distance_km * 1000)) * 100  # Convert distance to meters

    # Normalize the gradient: for simplicity, we can use the same 0-5 scale
    # Assuming a gradient of 20% is very difficult (5), and 0% is very easy (0)
    gradient_difficulty = min(gradient / 5, 5)  # This is an example normalization
    print(gradient_difficulty)
    print(weather_difficulty)
    # Calculate average difficulty
    total_difficulty = (gradient_difficulty + 5**((0.70*weather_difficulty)-3))

    # Ensure the difficulty is within 0-5 range
    return max(0, min(total_difficulty, 5))

# Example usage
api_key = "e16203e84ba4c25bb50815d97367c8a2"

def convert_object_to_JSON(object):
    print(object.route_mappings,"this is it over here")
    return ({
        "distance":object.distance,
        "ascent":object.ascent,
        "route_mappings":object.route_mappings,
        "name": object.name,
        "average_location":object.average_location,
        "max_height":object.max_height
    })
