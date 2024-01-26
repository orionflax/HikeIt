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
