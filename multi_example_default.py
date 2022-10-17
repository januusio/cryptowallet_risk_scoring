from januus_riskreport.client import riskreport_on_entity 

eth_address_1 = "0xbb0ea877a85df253ccc312b80c644da31443abfd"
eth_address_2 = "0x690bfe31f17b22924e7f0037b0b0046dcc63cc44"
eth_addresses=[eth_address_1, eth_address_2]
# Single address example
report = riskreport_on_entity(eth_addresses=eth_addresses)
print("Scoring breakdown for:")
for eth_address in eth_addresses:
    print(eth_address)
print()
print("Combined risk: " + str(report.risk_scores.combined_risk))
print("Fraud risk: " + str(report.risk_scores.fraud_risk))
print("Reputation risk: " + str(report.risk_scores.reputation_risk))
print("Lending risk: " + str(report.risk_scores.lending_risk))

for reason in report.reasons:
    print()
    print(f"The following contributed to the score by: {reason.offsets.combined_risk_offset}")
    print(reason.explanation)
