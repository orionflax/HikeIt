import csv
import psycopg2
import re

# Database connection parameters
db_params = {
    'database': 'mountain',
    'user': 'filefish',
    'password': 'filefish',
    'host': 'mountains',
    'port': '5432'
}

# Define the CSV file path
csv_file_path = 'your_csv_file.csv'

def parse_2d_array(array_string):
    # Convert string representation of 2D array to actual list of lists (2D array)
    # Replace this with a safer parsing method than eval in production
    return eval(array_string)


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
    return int(distance_km), int(ascent_m),int(match_max_h[0][6:])

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

# Example usage
url = "https://ldwa.org.uk/ldp/members/show_path.php?path_name=Nunwell+Trail"
path_name = extract_and_format_path_name(url)
print(path_name)


# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)
# Create a cursor object
cur = conn.cursor()

# Read the CSV file and insert data into the database
with open(csv_file_path, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Parse the data
        route_mappings = parse_2d_array(row['Route Mappings'])
        distance, ascent, max_height = parse_route_profile(row['Route Profile'])
        name = row['Route Name']

        # Create SQL insert statement
        insert_query = '''
            INSERT INTO routes (route_mappings, distance, ascent, max_height, name)
            VALUES (%s, %s, %s, %s, %s);
        '''

        # Execute the insert statement
        cur.execute(insert_query, (route_mappings, distance, ascent, max_height, name))

# Commit the changes
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
