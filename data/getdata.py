import os
import requests

from logger.log import LogActivities

def LoadContent(url):
    response = requests.get(url)
    content ="C:\\ActiveAssist\\data\\content.json"
    if response.status_code == 200:
        with open(content, "w") as file:
            file.write(response.text)
        LogActivities("Content data retrieved \n")
    else:
        LogActivities("Error retrieving JSON data.")
