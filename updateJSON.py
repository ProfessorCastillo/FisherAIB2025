import json

# Define the name of your JSON file
filename = 'AIB_presentation_list.json'

# The new key-value pairs you want to add to each entry
# In Python, the equivalent of JSON's 'null' is 'None'
keys_to_add = {
    "best_phd_finalist": None,
    "best_junior_faculty_finalist": None
}

try:
    # --- Step 1: Read the existing JSON data from the file ---
    # We open the file in read mode ('r') with UTF-8 encoding for compatibility.
    # The 'with' statement ensures the file is closed automatically.
    with open(filename, 'r', encoding='utf-8') as f:
        # json.load() parses the JSON file into a Python list of dictionaries
        data = json.load(f)

    # --- Step 2: Modify the data in memory ---
    # We loop through each presentation (which is a dictionary) in our list
    for presentation in data:
        # The .update() method is a clean way to add or update multiple keys
        presentation.update(keys_to_add)

    # --- Step 3: Write the modified data back to the same file ---
    # We open the file in write mode ('w'), which will overwrite the original content.
    with open(filename, 'w', encoding='utf-8') as f:
        # json.dump() writes the Python object back to the file as a JSON string.
        # The 'indent=2' argument makes the output JSON file human-readable.
        json.dump(data, f, indent=2)

    print(f"Success! The file '{filename}' has been updated with the new keys.")

except FileNotFoundError:
    print(f"Error: The file '{filename}' was not found.")
    print("Please make sure the script and the JSON file are in the same directory.")
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from the file '{filename}'. Please check if it's a valid JSON file.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
