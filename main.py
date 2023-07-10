import asyncio
import json
import multiprocessing
import os
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
from data.datamodel import DataToPost, DataToPostEncoder, ServerData
from logger.log import LogActivities
from utils.ping import ping_ip_address
from utils.requestUtils import GetContent, PostRequest
from utils.winmonitor import get_available_ram, get_computer_name, get_cpu_usage, get_pc_space, get_physical_memory


class AssistService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'ActiveAssist'
    _svc_display_name_ = 'Active Assist Service'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_running = True
        self.base_path = "C:\\ActiveAssist\\data"
        self.content_path = self.base_path + "\\content.json"
        self.config_path = self.base_path + "\\config.json"
        self.log_path = "C:\\ActiveAssist\\logger\\log.json"
        self.settings_path = "C:\\ActiveAssist\\settings\\settings.json"
      

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
           
        while self.is_running:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main(self))
 
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False


async def main(self):
    with open(self.config_path) as json_file:
        self.data = json.load(json_file)
    self.getUrl = self.data["getUrl"]
    self.postUrl = self.data["postUrl"]
    self.server_id = self.data["serverID"]

    with open(self.settings_path) as json_file:
        self.data = json.load(json_file)
    self.proxyHost = self.data["proxyHost"]
    self.proxyPort = self.data["proxyPort"]
    self.licenseKey = self.data["licenseKey"]
    self.scan_rate = self.data["scanRate"]
    LogActivities("Monitoring: New session started...\n")

    status = GetContent(self.getUrl)

    if status is False:
        self.is_running = False
        return

    with open(self.content_path) as content_file:
        data = json.load(content_file)

    # Extract information from the JSON
    license_key = data["licenceKey"]

    if license_key != self.licenseKey:
        LogActivities("Invalid License Key, Update the key from the setting\n")
        self.is_running = False
        return
    org_id = data["orgID"]
    entries = data["data"]

    ping_results = []
    LogActivities("Pinging server ips...\n")

    with multiprocessing.Pool(processes=50) as pool:
            results = pool.map(ping_ip_address, [entry["svr_ip_ip_address"] for entry in entries])
            
    for result in results:
        ping_results.append(result)

    ping_results_dict = [ping_result.__dict__ for ping_result in ping_results]
    server_data = ServerData(get_computer_name(), get_physical_memory(
    )+"MB", get_pc_space(), get_cpu_usage() + "%", get_available_ram() + "MB")
    server_data_dict = server_data.__dict__
    data_to_post = DataToPost(
        license_key, org_id, self.server_id, server_data_dict, ping_results_dict)

    json_string = json.dumps(data_to_post, cls=DataToPostEncoder)

    LogActivities("Send to cloud...\n")
    PostRequest(self.postUrl, json_string, self.proxyHost, self.proxyPort)
    with open(self.log_path, 'w') as file:
        file.write(json_string)
    LogActivities("Monitoring: Session ended...\n")
    # Wait for 10 sec before the next iteration
    await asyncio.sleep(self.scan_rate)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(AssistService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(AssistService)
