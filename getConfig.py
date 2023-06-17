import requests
def loadContent(url):
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        with open("content.json", "w") as file:
            file.write(response.text)
        print("JSON data saved to content.json")
    else:
        print("Error retrieving JSON data. Status code:", response.status_code)
