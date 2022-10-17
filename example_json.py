from januus_riskreport.client import riskreport_on_entity 
import json

# Single address example with json output
report = riskreport_on_entity(eth_addresses=["0xbb0ea877a85df253ccc312b80c644da31443abfd"])
# Full report json
print(json.dumps(report.as_json(), indent=4))
# Risk scores json
# print(json.dumps(report.risk_scores.__as_json__, indent=4))
