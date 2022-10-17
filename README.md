# Cryptowallet Risk Scoring by Januus

A free cryptowallet risk assessment tool, it helps assess if a cryptowallet has transacted with a threat actor, if it belongs to a scammer, or if the wallet address is generally safe. It generates a report on the fraudulent activity of any ethereum or bitcoin address based on the corresponding identity data and transaction analysis and displays the audit trail for this report in clean json.

## Setup

```
git clone https://github.com/januusio/cryptowallet_risk_scoring
cd cryptowallet_risk_scoring
python3 setup.py install
pip3 install -r requirements.txt
python3 example_default.py
```

## Usage

The example files `example_default.py`, `example_json.py`, `example_reasons.py` easily articulate the usage options. 

### Example Output

```json
{
    "reasons": [
        {
            "explanation": "The following addresses of this entity were found to likely be perpetrators of fraud: 0xbb0ea877a85df253ccc312b80c644da31443abfd",
            "label": "is-scammer",
            "offsets": {
                "combined_risk_offset": 52.31019,
                "fraud_risk_offset": 69.04503,
                "lending_risk_offset": 20.537472,
                "reputation_risk_offset": 50.95931
            },
            "risk_elaboration": {
                "scam_history": [
                    {
                        "address": "0xbb0ea877a85df253ccc312b80c644da31443abfd",
                        "blockchain": "ethereum",
                        "number_of_transactions": 98,
                        "risk_factors": [
                            {
                                "actor_type": "honeypot",
                                "involved_risk_activity": {
                                    "category_name": "honeypot",
                                    "description": "The scammer has involved in the creating smart contract for honeypot ",
                                    "rating": "high",
                                    "sub_category": "maliciousSmartContractCreation"
                                },
                                "media_platform_used": "Unknown"
                            }
                        ]
                    },
                    {
                        "address": "0xbb0ea877a85df253ccc312b80c644da31443abfd",
                        "blockchain": "ethereum",
                        "number_of_transactions": 98,
                        "risk_factors": [
                            {
                                "actor_type": "honeypot",
                                "involved_risk_activity": {
                                    "category_name": "honeypot",
                                    "description": "The scammer has involved in the creating smart contract for honeypot ",
                                    "rating": "high",
                                    "sub_category": "maliciousSmartContractCreation"
                                },
                                "media_platform_used": "Unknown"
                            }
                        ]
                    }
                ]
            }
        },
        {
            "explanation": "The entity has been associated with multiple dates between 2017-09-10 and 2021-03-19",
            "label": "date-verification",
            "offsets": {
                "combined_risk_offset": -1.6213226,
                "fraud_risk_offset": -2.9186554,
                "lending_risk_offset": 0,
                "reputation_risk_offset": -3.5666428
            },
            "risk_elaboration": {
                "verified_dates": [
                    {
                        "date": "2017-09-10",
                        "source": "The day '0xbb0ea877a85df253ccc312b80c644da31443abfd' was first seen on the blockchain.",
                        "weight": 1.86
                    },
                    {
                        "date": "2021-03-19",
                        "source": "The day '0xbb0ea877a85df253ccc312b80c644da31443abfd' was last seen on the blockchain.",
                        "weight": 0.574
                    }
                ]
            }
        },
        {
            "explanation": "The entity has had blockchain transactions with a known scammer. However, the total value sent/received was $0 so it may be part of a automatically executed contract.",
            "label": "risky-zero-valued-txs",
            "offsets": {
                "combined_risk_offset": 1.7818756,
                "fraud_risk_offset": 2.6735687,
                "lending_risk_offset": 2.9770813,
                "reputation_risk_offset": 1.4767227
            },
            "risk_elaboration": {
                "how_many_neighbors": "17",
                "how_many_scammy_neighbors": "1",
                "scammy_neighbor_details": [
                    {
                        "neighbor": "0xc94a6e7776bade5da316cf6fd8c751fb0d5c3c5e",
                        "scammer_details": {
                            "address": "0xc94a6e7776bade5da316cf6fd8c751fb0d5c3c5e",
                            "blockchain": "ethereum",
                            "number_of_transactions": 9,
                            "risk_factors": [
                                {
                                    "actor_type": "scammer",
                                    "involved_risk_activity": {
                                        "category_name": "phishing",
                                        "description": "Tricks the victim into paying a certain amount of money to the actor.",
                                        "rating": "moderate",
                                        "sub_category": "scam"
                                    },
                                    "media_platform_used": "Unknown"
                                },
                                {
                                    "actor_type": "scammer",
                                    "involved_risk_activity": {
                                        "category_name": "phishing",
                                        "description": "Tricks the victim into paying a certain amount of money to the actor.",
                                        "rating": "moderate",
                                        "sub_category": "scam"
                                    },
                                    "media_platform_used": "Unknown"
                                }
                            ]
                        }
                    }
                ]
            }
        }
    ],
    "risk_scores": {
        "combined_risk": 83.111786,
        "fraud_risk": 95.67439,
        "lending_risk": 58.691364,
        "reputation_risk": 78.08139
    }
}
```

The request to Januus' risk scoring service is a single function:

```python

from januus_riskreport.client import riskreport_on_entity

report = riskreport_on_entity( eth_addresses = [...], btc_addresses = [...] )

```
 
`eth_addresses` and `btc_addresses` are lists of strings. Note, this is a report on a single entity, not a batch request.
If an entity has multiple addresses, all may be queried at the same time by passing lists of length > 1. The query must not be empty.


## **Risk Scoring Package Maintenance**

We're committed to supporting this package *indefinitely*. Fresh risk data, newly identified threat actors and fraudulent wallets are added to the database daily. 

## **What kind of risk?**
 
Risk is not one-dimensional. A terrorist organization may pay their bills on time and be very credit worthy; but that doesn’t mean that they should be engaged with. A person who tends to naively fall for phishing scams isn’t necessarily likely to defraud others; but he probably shouldn’t be lent to. This API scores entities along 3 dimensions of risk:

### **Cryptowallet Reputation Risk**

- What risk does this entity pose to my reputation? Would it cause bad PR to enter a contractual relationship with them?
- Where to find it:
  - For the overall reputation risk: `report.risk_scores.reputation_risk`
  - For each reason in `report.reasons`: `reason.offsets.reputation_risk_offset`
 
### **Cryptowallet Fraud Risk**

- Has this person defrauded others before? Is there a long history of online presence to indicate it’s not a fake (or scam) account? Have they been funded by known scammers?
- Where to find it:
  - For the overall reputation risk: `report.risk_scores.fraud_risk`
  - For each reason in `report.reasons`: `reason.offsets.fraud_risk_offset`
 
### **Cryptowallet Lending Risk**

- Does this entity have concrete signs of credit-worthiness? Do they appear financially responsible? Do they have a record of falling victim to scams in the past?
- Where to find it:
  - For the overall reputation risk: `report.risk_scores.lending_risk`
  - For each reason in `report.reasons`: `reason.offsets.lending_risk_offset`
 
## I don’t care about categories of risk. Give me a number.

  - Use `report.risk_scores.combined_risk`.
  
All of the above dimensions are aggregated to produce a combined risk score. This is probably the most important single score. The only guarantee it makes as to certain failure is the following: If the `report.risk_scores.combined_risk` is failing (>= 60), then one or more of the above dimensions must also have had a failing score. Each reason also has a `combined_risk_offset`. In the rare circumstance that an entity has multiple reasons for certain failure, the combined risk offsets may not be evenly distributed. 

# Core Concepts

## Januus' Risk Scale
 
The risk score that’s returned does not represent a probability; it’s a carefully calculated grade with nuanced ranges of meaning. It’s bounded between 0 and 100; where 0 is impossibly low risk (zero) and 100 is impossibly high risk. The neutral score is 30 and 60 is failing. You can think of it like an `A+/A-/B+/B/B-/C+/C/C-/D+/D/D-/F` grade from primary school (except from-low-to-high, because low risk equates to a good grade.)
 
Here’s a brief summary:

| | |
| -- | --------|
|**Score**| **Description** |
| > 25 | Good |
| 30 | Neutral |
| > 40 | A troublingly high score |
| >= 60 | A failing score |
 
A more detailed breakdown:

| | |
|--------|--|
|**Score**| **Description** |
| 0 | Impossibly low risk (zero) |
| <10 | Very few entities will have a score this outstanding, almost risk-free based on seen datapoints. |
| 10-20 |  An extremely good score. |
| 20-25 | A good score. In this range, the improved score is still very meaningful. |
| 25-27  | Starting to become only slightly better than neutral. Usually in this range, there might not be much data available about an entity other than date verification. |
| 27-33 | Neutral. |
| 33-35 | Slightly worse than neutral. This is the realm where a risk factor starts to become more than just noise. |
| 35-40 | A slightly worrying score. Perhaps this wallet has transacted with bad actors, but at a low enough proportion that a meaningful link cannot be established. |
| 40-50 | A bad score. |
| 50-60 | A very bad score. Because it becomes exponentially more difficult to reach 60 without a reason for certain failure, this range probably signifies the presence of several unrelated risk factors. Especially as the score inches toward toward and past 57ish, then it becomes nearly as meaningful as a failing score in the low 60’s. |
| ==60 | A failing score; do not have dealings with this entity. This is the exact point where risk becomes so extreme that an irredeemably failing score is given. Only a hand-full of concrete reasons in our rule system will allow the score to hit this threshold. Once at 60, no number of safe datapoints can ever push the score below this mark. It’s guaranteed. |
| 70-80 | This score signifies an entity that one should divert considerable resources to avoid. Although, it’s possible that it was even higher, but some datapoints (or ‘reasons’) had a negative offset, pushing it closer toward 60. |
| >80 | A supremely high risk. In this range, usually the wallet has been directly and credibly marked as malicious or has an overwhelming number of direct neighbors of whom this is true. |
| ==100 | An impossibly high risk score. |
 
 
### What makes the risk score explainable?
In the response, we provide an array of reasons ( in `report.reasons` ) that explain our score for a given entity. Each reason given provides an offset for a very approximate estimate of how much it impacted the overall score. A risk factor will have a positive offset and a datapoint that gives credibility will have a negative offset. 

# The Report
 
The generated report will be an instance of the `RiskReport` class:


```python

class RiskReport:
    risk_scores: RiskScores
    reasons: List[RiskReason]
```

## RiskScores

What is a `RiskScores` object? It contains the three fundamental scores of risk, as well as a combined score. These are all explained above in the 'Concepts' section. 

```python
class RiskScores:
    combined_risk: float
    fraud_risk: float
    reputation_risk: float
    lending_risk: float
```

## White-box Reasoning

What about the `reasons: List[RiskReason]` of our risk report? Each `Reason` is a manifestation of a single component that contributed to the score. 

```python 
class RiskReason:

    # An English explanation of the reason
    explanation: str
    
    # A RiskElaboration gives machine-readable details about this Reason, or component of the score
    risk_elaboration: RiskElaboration
    
    # This is json data giving details of the reason.
    # There are a finite number of labels, and each label has it's own corresponding RiskElaboration
    label: str
    
    # A RiskOffsets object is an approximation of how much this Reason contributed to each dimension of the top-level RiskScore
    offsets: RiskOffsets 

class RiskOffsets:
    combined_risk_offset: float
    fraud_risk_offset: float
    lending_risk_offset: float
    reputation_risk_offset: float
    
```    

The ideas of `RiskOffsets` are, again, covered above in the 'Concepts' section.
    
 
### Labels & subclasses of RiskElaboration

Each reason will have a label. For each reason, the subclass of `reason.risk_elaboration` can be known by its label. If you would like a new label added, please contact us and we’d love to look into its feasibility and usefulness. Here are the current labels:

```
"sent-to-scammer"
"funded-by-scammer"
"risky-zero-valued-txs"
"is-scammer"
"date-verification"
```

And here are the corresponding classes

```python 
class RiskElaboration:
  pass
  
class IsScammer(RiskElaboration):
    """
    The queried entity is a known scammer. 
    The layout of `RiskAccountDetails` will be publicly expanded in the future, but for now it's JSON. 
    """
    scam_history: List[RiskAccountDetails]

class ScammyNeighborDetails:
    sender: str
    recipient: str
    total_usd: float
    scammer_details: RiskAccountDetails

class SentToScammer(RiskElaboration):
    """
    The entity sent money to a scammer.
    The 'recipient' is a wallet that has received funds from the queried entity.
    """
    how_many_recipients: int
    how_many_scammy_recipients: int
    scammy_recipient_details: List[ScammyNeighborDetails]

class FundedByScammer(RiskElaboration):
    """
    The entity has received funds from a scammer.
    A wallet that has sent money to the queried entity is a 'funder'
    """
    how_many_funders: int
    how_many_scammy_funders: int
    scammy_funder_details: List[ScammyNeighborDetails]


class RiskyZeroValuedTxs(RiskElaboration):
    "This class shows that the queried entity has had one or more zero-valued transactions with a scammer."
    how_many_neighbors: int
    how_many_scammy_neighbors: int
    scammy_neighbor_details: List[Dict[str,str]]

```

Date verification is also important, as newly created entities tend to not have as much known about them or credit history.


```python

class VerifiedDates(RiskElaboration):
    verified_dates: List[VerifiedDate]
    
class VerifiedDate:
    date: str
    source: str
    weight: float

```

## Rate Limits

We ask that you generally not generate more than 30 queries per minute.
 
