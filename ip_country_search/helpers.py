import requests
import csv
import math
from ipaddress import ip_address, IPv4Address
import bisect
import os
import sys

from .constants import *

def download_data(rir_entry):
    rir = rir_entry[0]
    link = rir_entry[1]
    data = requests.get(link)
    if data.status_code == 200:
        file_name = rir + ".csv"
        with open(file_name, mode='wb') as file:
            file.write(data.content)

def size_to_cidr_mask(c):
    """ c = 2^(32-m), m being the CIDR mask """
    return int(-math.log2(c) + 32)

def parse_rir_file(filename):
    for path in sys.path:
        try:
            path = path + "/ip_country_search/static/csv/"
            if os.path.isdir(path):
                break
        except:
            continue

    with open(path + filename) as f:
        rows = csv.reader(f, delimiter='|')
        for r in rows:
            try:
                rir, country_code, ip_version, ip, mask, *_ = r
            except ValueError:
                continue
            if ip == '*':
                continue
            if ip_version == 'ipv4':
                length = int(mask)
                addr = ip_address(ip)
                yield {
                    'ip_low': addr,
                    'ip_high': addr + length - 1,
                    'rir': rir,
                    'country': country_code,
                    'range': ip+'/'+str(size_to_cidr_mask(length)),
                }

def get_ip_data(keys, data, ip):
    ip = ip_address(ip)
    if not ip.is_global or ip.is_multicast:
        return None
    i = bisect.bisect_right(keys, ip)
    entry = data[i-1]
    assert(entry['ip_low'] <= ip <= entry['ip_high'])
    return entry

def validate_ip(ip):
    try:
        ip_address(ip)
        return True
    except ValueError:
        return False

def parse_ip_data(ip_data):
    return COUNTRY_MAPPING.get(ip_data.get('country'), "Unknown country code")
