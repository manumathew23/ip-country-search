import concurrent.futures
import csv
import math
from ipaddress import ip_address, IPv4Address
import bisect
from urllib.parse import urlencode, quote_plus
import itertools

from .constants import *
from .helpers import *


def update_rir_files():
    with concurrent.futures.ProcessPoolExecutor(max_workers=len(RIR_URL_MAPPING)) as executor:
        executor.map(download_data, RIR_URL_MAPPING.items())


rir_file = [rir + ".csv" for rir in list(RIR_URL_MAPPING.keys())]

# Parse RIR file data
data = list(itertools.chain(
    parse_rir_file(rir_file[0]),
    parse_rir_file(rir_file[1]),
    parse_rir_file(rir_file[2]),
    parse_rir_file(rir_file[3]),
    parse_rir_file(rir_file[4])
))

data.sort(key=lambda r: r['ip_low'])
keys = [r['ip_low'] for r in data]

def get_country_name(ip_address=None):
    if not ip_address:
        return {"status_code": 400, "message": "empty IP"}
    print('bb')
    if validate_ip(ip_address):
        return {
            "status_code": 200,
            "message": parse_ip_data(get_ip_data(keys, data, ip_address))
        }
    return {"status_code": 400, "message": "Incorrect IP"}
