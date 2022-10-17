import json 
from .types import RiskReport 
from .exceptions import RequestedNullReport, EndPointException 
from typing import *
import urllib3 
from urllib3.exceptions import ProtocolError 
import os 

url = "http://34.229.17.199:8080" 

__http__ = urllib3.PoolManager()


def riskreport_on_entity(eth_addresses: Sequence[str] = (), 
                         btc_addresses: Sequence[str] = ())->RiskReport:
    "Perform a risk report on a single entity. The entity may own multiple ETH or BTC addresses."

    payload = {"ethAddresses": eth_addresses,
               "btcAddresses": btc_addresses }
   
    if 0 == sum(map(len, payload.values())):
        raise RequestedNullReport() 

    try: 
        r = __http__.request('POST', url,
                     headers={'Content-Type': 'application/json'},
                     body=json.dumps(payload).encode("utf-8"))
        
        json_response = json.loads(r.data.decode('utf-8'))

        return RiskReport.from_dict(json_response)
    except ProtocolError:
        raise EndPointException()
