import datetime
import socket
from data.datamodel import PingResult
import ping3
import aioping

async def AsyncPing(ip_address):
    try:
        delay = await aioping.ping(ip_address)
        if delay is not None:
            return PingResult(ip_address, "Success", datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        else:
            return PingResult(ip_address, "Fail", datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
    except (OSError, socket.gaierror):
        return PingResult(ip_address, "Fail", datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        socket.close()


def ping_ip_address(ip_address):
    try:
        response_time = ping3.ping(ip_address, timeout=8)
        if response_time is not None:
            return PingResult(ip_address, "Success", datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        else:
             return PingResult(ip_address, "Fail", datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
    except OSError:
         return PingResult(ip_address, "Fail", datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))