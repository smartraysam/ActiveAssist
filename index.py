import asyncio
import datetime
import os
import json
from data.datamodel import DataToPost, DataToPostEncoder, ServerData
from data.getdata import LoadContent
from logger.log import LogActivities
from utils.ping import AsyncPing
from utils.postdata import PostRequest
from utils.winmonitor import get_available_ram, get_cpu_usage, get_pc_space, get_computer_name, get_physical_memory



def initialize():
    base_path = "C:\\ActiveAssist\\data"
    content_path = base_path + "\\content.json"
    config_path = base_path + "\\config.json"
    log_path = "C:\\ActiveAssist\\logger\\log.json"
    with open(config_path) as json_file:
        data = json.load(json_file)
    getUrl = data["getUrl"]
    postUrl = data["postUrl"]
    proxyHost = data["proxyHost"]
    proxyPort = data["proxyPort"]

    return content_path, getUrl, postUrl, proxyHost, proxyPort, log_path

async def main():
    print("start session monitoring")
    LogActivities("Monitoring: New session started...\n")
    
    if os.path.exists(content_path):
        LogActivities("Read local file...\n")
    else:
        LogActivities("Getting remote server...\n")
        LoadContent(getUrl)

    with open(content_path) as content_file:
        data = json.load(content_file)

    # Extract information from the JSON
    license_key = data["licenceKey"]
    org_id = data["orgID"]
    entries = data["data"]

    ping_results = []
    LogActivities("Pinging server ips...\n")
    tasks = [AsyncPing(entry["svr_ip_ip_address"]) for entry in entries]
    results = await asyncio.gather(*tasks)

    for result in results:
        ping_results.append(result)

    ping_results_dict = [ping_result.__dict__ for ping_result in ping_results]
    server_data = ServerData(get_computer_name(), get_physical_memory()+"MB", get_pc_space(), get_cpu_usage() + "%", get_available_ram() + "MB")
    server_data_dict = server_data.__dict__
    data_to_post = DataToPost(license_key, org_id, server_data_dict, ping_results_dict)

    json_string = json.dumps(data_to_post, cls=DataToPostEncoder)

    LogActivities("Send to cloud...\n")
    PostRequest(postUrl, json_string, proxyHost, proxyPort)
    with open(log_path, 'w') as file:
        file.write(json_string)
    # Wait for 10 sec before the next iteration
    await asyncio.sleep(10)
    LogActivities("Monitoring: Session ended...\n")
    print("End session monitorong")


if __name__ == '__main__':
    content_path, getUrl, postUrl, proxyHost, proxyPort, log_path = initialize()
    while True:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(main())
        except KeyboardInterrupt:
            pass