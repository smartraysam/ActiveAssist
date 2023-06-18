import os
import requests


def LoadContent(url):
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        with open(os.path.join("data", "content.json"), "w") as file:
            file.write(response.text)
        print("JSON data saved to content.json")
    else:
        print("Error retrieving JSON data. Status code:", response.status_code)
