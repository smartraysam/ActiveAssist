import json
import os
import datetime

class PingResult:
    def __init__(self, svr_ip_ip_address, svr_ip_status, ping_date_time):
        self.svr_ip_ip_address = svr_ip_ip_address
        self.svr_ip_status = svr_ip_status
        self.ping_date_time = ping_date_time

class ServerData:
    def __init__(self, hostname, ram_total, drive_space, cpu, ram_free):
        self.hostname = hostname
        self.ram_total = ram_total
        self.drive_space = drive_space
        self.cpu = cpu
        self.ram_free = ram_free

class DataToPost:
    def __init__(self, license_key, org_id, server_data, ping_result):
        self.license_key = license_key
        self.org_id = org_id
        self.server_data = server_data
        self.ping_result = ping_result


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