import re

# Example string
route_profile = "1.9 km (1.2 miles)86 m (282 ft) ascent814 m (2,671 ft) maximum height"

def parse_route_profile(profile_string):
    # Regular expression pattern to match distances in km and m, respectively
    pattern = re.compile(r'(\d+(\.\d+)?)\s*km|\((\d+(\.\d+)?)\s*miles\)|(\d+)\s*m\s*\((\d+)\s*ft\)')
    matches = pattern.findall(profile_string)
    pattern1 = r'ascent\d+'
    match_max_h = re.findall(pattern1,profile_string)
    # Extract the distance and ascent, which are the first and third groups in the pattern
    # We'll also extract the maximum height, which are the fifth and sixth groups in the pattern
    distance_km = float(matches[0][0])  # First match, km
    ascent_m = int(matches[2][4])   # Third match, m
    for x in route_profile:
        if 'ascent' in x:
            print( 'ascent',x[5:])
            break 
        else:
            pass
    return distance_km, ascent_m,(match_max_h[0][6:])

# Parse the route profile
distance_km, ascent_m ,max_height= parse_route_profile(route_profile)

# Output the results
print(f"Distance: {distance_km} km")
print(f"Ascent: {ascent_m} m")
print(f"Maximum Height: {max_height} m")
