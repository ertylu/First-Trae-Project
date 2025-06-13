import base64
import requests
import glob # Import the glob module to find files matching a pattern
import os   # Import the os module for path manipulation

# --- Configuration ---
# ---> CHANGE THIS to the path of the folder containing your images.
#      Use '.' for the current directory.
#      Examples:
#      - Windows: 'C:\Users\YourName\Pictures\TestImages'
#      - macOS/Linux: '/home/YourName/Pictures/TestImages'
IMAGE_FOLDER_PATH = r'C:\Users\ertyl\OneDrive\Documents\Trae Projects\First Trae projects\Webscraping exercise'

# You can change this prompt to ask a different question about the images.
PROMPT = "Describe this image in detail. What objects do you see? What is happening?"

# NOTE: You do not need to provide your own API key if running this in the
# provided learning environment. However, if you run this on your own
# machine, you will need to get a key from Google AI Studio and place it here.
API_KEY = "AIzaSyCVLaUtypYU0kopm_IaAcyD5ZutFON4c2Q" # Leave blank if in the learning environment.


def analyze_image(image_path):
    """
    Encodes a single image, sends it to the Gemini API with a prompt, and prints the result.
    
    Args:
        image_path (str): The path to the image file to be analyzed.
    """
    print(f"\n--- Starting Analysis for: {image_path} ---")

    # --- Step 1: Encode the image file into Base64 ---
    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')
        print(f"Successfully encoded '{image_path}'.")
    except FileNotFoundError:
        print(f"ERROR: The file '{image_path}' was not found.")
        return # Skip to the next file
    except Exception as e:
        print(f"An error occurred during file encoding for {image_path}: {e}")
        return # Skip to the next file


    # --- Step 2: Construct the API Request Payload ---
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": PROMPT
                    },
                    {
                        "inlineData": {
                            "mimeType": "image/jpeg",
                            "data": base64_image
                        }
                    }
                ]
            }
        ]
    }

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }

    # --- Step 3: Make the POST request to the API ---
    print("Sending request to the Gemini API...")
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the API request for {image_path}: {e}")
        return # Skip to the next file

    # --- Step 4: Extract and Print the Response ---
    print("Request successful. Processing response...")
    try:
        response_json = response.json()
        
        if (response_json.get('candidates') and 
            response_json['candidates'][0].get('content') and
            response_json['candidates'][0]['content'].get('parts')):
            
            generated_text = response_json['candidates'][0]['content']['parts'][0]['text']
            
            print("\n--- AI Analysis Result ---")
            print(generated_text)
            print("--------------------------")
        else:
            print(f"Could not find generated text in the API response for {image_path}. Full response:")
            print(response_json)

    except (ValueError, KeyError, IndexError) as e:
        print(f"Error parsing the API response for {image_path}: {e}")
        print("Full response content:")
        print(response.text)


# This is the standard entry point for a Python script.
if __name__ == "__main__":
    # Check if the specified folder path exists
    if not os.path.isdir(IMAGE_FOLDER_PATH):
        print(f"Error: The specified folder path does not exist: '{IMAGE_FOLDER_PATH}'")
        print("Please update the IMAGE_FOLDER_PATH variable in the script.")
    else:
        # Define the patterns to search for inside the specified folder
        patterns_to_check = ['*.jpg', '*.JPG', '*.jpeg', '*.JPEG', '*.png', '*.PNG']
        image_files = []
        for pattern in patterns_to_check:
            # os.path.join correctly combines the folder path and the pattern
            search_path = os.path.join(IMAGE_FOLDER_PATH, pattern)
            image_files.extend(glob.glob(search_path))
        
        unique_image_files = list(set(image_files))

        if not unique_image_files:
            print(f"No image files (.jpg, .jpeg, .png) found in the folder: '{IMAGE_FOLDER_PATH}'")
        else:
            print(f"Found {len(unique_image_files)} image files in '{IMAGE_FOLDER_PATH}' to analyze.")
            for file_path in unique_image_files:
                analyze_image(file_path)
        
        print("\nBatch analysis complete.")
