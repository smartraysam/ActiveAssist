import asyncio
import datetime
import socket
import aioping
from data.datamodel import PingResult



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