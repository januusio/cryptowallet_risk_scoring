from januus_riskreport.client import riskreport_on_entity 

eth_address_1 = "0xbb0ea877a85df253ccc312b80c644da31443abfd"

# Single address example
report = riskreport_on_entity(eth_addresses=[eth_address_1])
print("Scoring breakdown for " + eth_address_1)
print("Combined risk: " + str(report.risk_scores.combined_risk))
print("Fraud risk: " + str(report.risk_scores.fraud_risk))
print("Reputation risk: " + str(report.risk_scores.reputation_risk))
print("Lending risk: " + str(report.risk_scores.lending_risk))

