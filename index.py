import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import os
import sys
import asyncio
import datetime
import json
from getConfig import loadContent
from payloadModel import DataToPost, DataToPostEncoder, PingResult, ServerData, ServerDataEncoder
from ping import asyncping
from post2server import send_json_to_endpoint
from winmonitor import GetCpuUsage, get_computer_name, get_physical_memory, getAvailableRAM, getPCSpace


class MonitorService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'MonitorService'
    _svc_display_name_ = 'Monitor Service'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    async def main(self):
        while self.is_running:
            try:
                content_path = 'content.json'
                with open('config.json') as json_file:
                    data = json.load(json_file)
                getUrl = data["getUrl"]
                postUrl = data["postUrl"]
                proxyHost = data["proxyHost"]
                proxyPort = data["proxyPort"]

                if os.path.exists(content_path):
                    print("loading file")
                else:
                    loadContent(getUrl)

                with open('content.json') as content_file:
                    data = json.load(content_file)

                # Extract information from the JSON
                license_key = data["licenceKey"]
                org_id = data["orgID"]
                entries = data["data"]

                ping_results = []
                tasks = [asyncping(entry["svr_ip_ip_address"])
                         for entry in entries]
                results = await asyncio.gather(*tasks)

                for result in results:
                    ping_results.append(result)

                ping_results_dict = [
                    ping_result.__dict__ for ping_result in ping_results]
                server_data = ServerData(get_computer_name(), get_physical_memory(
                )+"MB", getPCSpace(), GetCpuUsage() + "%", getAvailableRAM() + "MB")
                server_data_dict = server_data.__dict__
                data_to_post = DataToPost(
                    license_key, org_id, server_data_dict, ping_results_dict)

                json_string = json.dumps(data_to_post, cls=DataToPostEncoder)

                send_json_to_endpoint(
                    postUrl, json_string, proxyHost, proxyPort, 'monitor.log')
                with open('log.json', 'w') as file:
                    file.write(json_string)

                await asyncio.sleep(60)  # Sleep for 60 seconds

            except Exception as e:
                servicemanager.LogErrorMsg(str(e))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MonitorService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MonitorService)
