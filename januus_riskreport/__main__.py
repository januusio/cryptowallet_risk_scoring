from .client import *
from .types import *
import sys 
import json 


# python3 -m januus_riskcheck '{"eth_addresses": ["0xbb0ea877a85df253ccc312b80c644da31443abfd"]}'

report = riskreport_on_entity(**json.loads(sys.argv[1]))

print(json.dumps(report.as_json()))
