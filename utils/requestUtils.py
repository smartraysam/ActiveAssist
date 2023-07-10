import requests

from logger.log import LogActivities

def PostRequest(url, json_string, proxy_host="", proxy_port=""):
    headers = {
        "Content-Type": "application/json"
    }
    log = ""

    try:
        if proxy_host and proxy_port:
            proxy_url = f"{proxy_host}:{proxy_port}"
            proxies = {
                "http": proxy_url,
                "https": proxy_url
            }
            response = requests.post(
                url, data=json_string, headers=headers, proxies=proxies)
        else:
            response = requests.post(url, data=json_string, headers=headers)
        LogActivities(response.text)

        if response.status_code == 200:
            log = "JSON string sent successfully!\n"
        else:
            log = f"Failed to send JSON string. Status code: {response.status_code}\n"
    except requests.Timeout:
        log = "Failed to send JSON string. Timeout\n"
    except requests.RequestException as e:
        log = f"An error occurred: {str(e)}\n"
    # Append the log to the log file
    LogActivities(log)


def GetContent(url):
    log = ""
    status = False
    try:
        response = requests.get(url)
        content ="C:\\ActiveAssist\\data\\content.json"
        if response.status_code == 200:
            with open(content, "w") as file:
                file.write(response.text)
            log = "Content data retrieved \n"
            status = True
        else:
            log = "Error retrieving JSON data."
    except requests.Timeout:
        log = "Failed to send JSON string. Timeout\n"
    except requests.RequestException as e:
        log = f"An error occurred: {str(e)}\n"
    
    LogActivities(log)
    return status


