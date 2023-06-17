import asyncio
import datetime
import os
import json
from getConfig import loadContent
from log import logactivities
from payloadModel import DataToPost, DataToPostEncoder, PingResult, ServerData, ServerDataEncoder
from ping import asyncping
from post2server import send_json_to_endpoint
from winmonitor import GetCpuUsage, get_computer_name, get_physical_memory, getAvailableRAM, getPCSpace

async def main():
    while True:
        print("Session Start")
        logactivities("Monitoring: New session started...\n")
        content_path = 'content.json'
        with open('config.json') as json_file:
            data = json.load(json_file)
        getUrl = data["getUrl"]
        postUrl = data["postUrl"]
        proxyHost = data["proxyHost"]
        proxyPort = data["proxyPort"]

        if os.path.exists(content_path):
            logactivities("Read local file...\n")
        else:
            logactivities("Getting remote server...\n")
            loadContent(getUrl)

        with open('content.json') as content_file:
            data = json.load(content_file)

        # Extract information from the JSON
        license_key = data["licenceKey"]
        org_id = data["orgID"]
        entries = data["data"]

        ping_results = []
        logactivities("Pinging server ips...\n")
        tasks = [asyncping(entry["svr_ip_ip_address"]) for entry in entries]
        results = await asyncio.gather(*tasks)

        for result in results:
            ping_results.append(result)

        ping_results_dict = [ping_result.__dict__ for ping_result in ping_results]
        server_data = ServerData(get_computer_name(), get_physical_memory()+"MB", getPCSpace(), GetCpuUsage() + "%", getAvailableRAM() + "MB")
        server_data_dict = server_data.__dict__
        data_to_post = DataToPost(license_key, org_id, server_data_dict, ping_results_dict)

        json_string = json.dumps(data_to_post, cls=DataToPostEncoder)

        logactivities("Send to cloud...\n")
        send_json_to_endpoint(postUrl, json_string, proxyHost, proxyPort)
        # Wait for 10 sec before the next iteration
        await asyncio.sleep(10)
        logactivities("Monitoring: Session ended...\n")
        print("Session Ended")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
