import json
import os
import datetime

class PingResult:
    def __init__(self, svr_ip_ip_address, svr_ip_status, ping_date_time):
        self.SvrIpIpAddress = svr_ip_ip_address
        self.SvrIpStatus = svr_ip_status
        self.PingDateTime = ping_date_time

class ServerData:
    def __init__(self, hostname, ram_total, drive_space, cpu, ram_free):
        self.Hostname = hostname
        self.RamTotal = ram_total
        self.DriveSpace = drive_space
        self.Cpu = cpu
        self.RamFree = ram_free

class DataToPost:
    def __init__(self, license_key, org_id, server_data, ping_result):
        self.licenceKey = license_key
        self.OrgID = org_id
        self.Serverdata = server_data
        self.Pingresult = ping_result


class ServerDataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ServerData):
            return obj.__dict__  # Convert ServerData object to a dictionary
        return super().default(obj)

class DataToPostEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DataToPost):
            return obj.__dict__  # Convert DataToPost object to a dictionary
        return super().default(obj)