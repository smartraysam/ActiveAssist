import datetime
import ping3
import aioping
from data.datamodel import PingResult



async def AsyncPing(ip_address):
    try:
        delay = await aioping.ping(ip_address)
        print(delay)
        if delay is not None:
            return PingResult(ip_address, "Success", datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        else:
            return PingResult(ip_address, "Fail", datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
    except TimeoutError:
        return PingResult(ip_address, "Fail", datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
