import requests
import os
import json

def create_shortcode():
    url = input("Enter a URL: ")
    short_code = input("Enter a short code: ")
    description = input("Enter a description(optional): ")
    
    data = {
        "url": url,
        "short_code": short_code,
        "description": description if description else ""
    }
    
    function_url = os.environ.get("CREATE_FUNCTION_URL")
    
    response = requests.post(function_url, json=data)
    # Debugging
    #print(f"Status Code: {response.status_code}")
    #print(f"Function URL: {function_url}")
    try:
        response_data = response.json()
        print(f"Short URL: {response_data.get('short_url', 'No short URL found')}")
    except json.JSONDecodeError:
        print("Error creating short URL")

def list_shortcodes():
    function_url = os.environ.get("LIST_FUNCTION_URL")
    response = requests.get(function_url)
    try:
        response_data = response.json()
        for item in response_data:
            print(f"Shortened URL: {item.get('Shortened URL')}, Long URL: {item.get('Long URL')}, Description: {item.get('Description')}")
    except json.JSONDecodeError:
        print("Error listing short URLs")

def main():
    while True:
        print("1. Create a short URL")
        print("2. List all short URLs")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            create_shortcode()
        elif choice == "2":
            list_shortcodes()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please input 1, 2, or 3")

if __name__ == "__main__":
    main()
    