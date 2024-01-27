import csv
import psycopg2
import re
import sys
# Database connection parameters
db_params = {
    'database': 'mountains',
    'user': 'filefish',
    'password': 'filefish',
    'host': 'localhost',
    'port': '5432'
}

# Define the CSV file path
csv_file_path = 'routes.csv'

def parse_2d_array(array_string):
    # Convert string representation of 2D array to actual list of lists (2D array)
    # Replace this with a safer parsing method than eval in production
    return eval(array_string)


def parse_route_profile(profile_string):
    profile_string, "this is the route_profile"
    profile_string = profile_string.replace('Â', '')
    #print(profile_string)
    # Regular expression pattern to match distances in km and m, respectively
    pattern = r'(\d+(\.\d+)?)\s*km'
    matches = re.findall(pattern,profile_string)
    pattern1 = r'ascent\d+'
    pattern2 = r'miles\)\d+'
    ascent_max_h = re.findall(pattern2,profile_string)
    match_max_h = re.findall(pattern1,profile_string)
    distance_km = float(matches[0][0])  # First match, km
    for x in profile_string:
        if 'ascent' in x:
            break 
        else:
            pass
    return distance_km, (ascent_max_h[0][6:]),(match_max_h[0][6:])

def extract_and_format_path_name(url):
    # Find the start of the path_name parameter
    start = url.find("path_name=") + len("path_name=")
    if start == -1:
        return None

    # Extract the substring after path_name
    extracted_string = url[start:]

    # Replace '+' with spaces
    formatted_string = extracted_string.replace('+', ' ')

    return formatted_string

def extract_and_format_path_name(url):
    # Find the start of the path_name parameter
    start = url.find("path_name=") + len("path_name=")
    if start == -1:
        return None

    # Extract the substring after path_name
    extracted_string = url[start:]

    # Replace '+' with spaces
    formatted_string = extracted_string.replace('+', ' ')

    return formatted_string

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)
# Create a cursor object
cur = conn.cursor()


# Increase the maximum field size limit
max_int_size = 2**31 - 1
csv.field_size_limit(max_int_size)


# Read the CSV file and insert data into the database
with open(csv_file_path, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Parse the data
        route_mappings = parse_2d_array(row['Route Mappings'])
        if (len(row['Route Profile']) == 0):
            print('failed to add')
            continue
        
        distance, ascent, max_height = parse_route_profile(row['Route Profile'])
        name = extract_and_format_path_name(row['Route Name'])

        # Create SQL insert statement
        insert_query = '''
            INSERT INTO routes (route_mappings, distance, ascent, max_height, name)
            VALUES (%s, %s, %s, %s, %s);
        '''

        # Execute the insert statement
        cur.execute(insert_query, (route_mappings, distance, ascent, max_height, name))
        print(cur.statusmessage)
        conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
