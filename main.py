import requests
import os
import json

def main():
    url = input("Enter a URL: ")
    short_code = input("Enter a short code: ")
    description = input("Enter a description(optional): ")
    
    data = {
        "url": url,
        "short_code": short_code,
        "description": description if description else ""
    }
    
    function_url = os.environ.get("FUNCTION_URL")
    
    response = requests.post(function_url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Function URL: {function_url}")
    try:
        response_data = response.json()
        print(f"Short URL: {response_data.get('short_url', 'No short URL found')}")
    except json.JSONDecodeError:
        print("Error creating short URL")

if __name__ == "__main__":
    main()
    