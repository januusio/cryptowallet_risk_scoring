from __future__ import annotations 
from typing import *
from dataclasses import dataclass, field  
from .__camelsnake__ import snake_case_dict 
from .exceptions import UnknownLabelException, DeserializationException, RiskReportException 

Fn = Callable 
RiskAccountDetails = Any

def raise_as(msg: str):
    def inner(f):
        def super_inner(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except RiskReportException as e:
                raise e
            except Exception as e:
                raise DeserializationException(msg)
        return super_inner 
    return inner


@dataclass 
class RiskScores:
    combined_risk: float 
    fraud_risk: float 
    reputation_risk: float 
    lending_risk: float 
   
    __as_json__: Dict[str, Any] = field(default_factory=lambda: {}) 
    @staticmethod 
    @raise_as("RiskScores") 
    def from_dict(d: Dict[str, Any]   )->RiskScores:
        x = RiskScores(**d)
        x.__as_json__ = d
        return x

    def as_json(self)->Dict[str, Any]:
        return self.__as_json__ 


@dataclass 
class RiskOffsets:
    combined_risk_offset: float 
    fraud_risk_offset: float 
    lending_risk_offset: float 
    reputation_risk_offset: float 
    __as_json__: Dict[str, Any] = field(default_factory=lambda: {}) 

    @staticmethod 
    @raise_as("RiskOffsets") 
    def from_dict(d: Dict[str, Any]   )->RiskOffsets:
        x = RiskOffsets(**d)     
        x.__as_json__ = d
        return x 

    def as_json(self)->Dict[str, Any]:
        return self.__as_json__ 

@dataclass 
class RiskElaboration:  
    @staticmethod 
    @raise_as("RiskElaboration") 
    def from_dict_label(d: Dict[str, Any], label: str)->RiskElaboration:

        if label == "sent-to-scammer":
            return SentToScammer.from_dict(d)
        
        elif label == "funded-by-scammer": 
            return FundedByScammer.from_dict(d) 
        
        elif label == "risky-zero-valued-txs": 
            return RiskyZeroValuedTxs.from_dict(d)
        
        elif label == "is-scammer":
            return IsScammer.from_dict(d) 
        
        elif label == "date-verification": 
            return VerifiedDates.from_dict(d)        
        
        else: 
            raise AttributeError(f"Unknown label: {label}")


@dataclass 
class IsScammer(RiskElaboration):
    scam_history: List[RiskAccountDetails]         
    __as_json__: Dict[str, Any] = field(default_factory=lambda: {}) 

    @staticmethod 
    @raise_as("IsScammer") 
    def from_dict(d: Dict[str, Any]   )->IsScammer:
        x = IsScammer(**d)
        x.__as_json__ = d
        return x

    def as_json(self)->Dict[str, Any]:
        return self.__as_json__ 

@dataclass 
class RiskReason:
    explanation: str 
    risk_elaboration: RiskElaboration 
    label: str 
    offsets: RiskOffsets 
    
    __as_json__: Dict[str, Any] = field(default_factory=lambda: {}) 
    @staticmethod 
    @raise_as("RiskReason")
    def from_dict(d: Dict[str, Any])-> RiskReason: 
        return RiskReason(
                      explanation = d["explanation"],
                      risk_elaboration = RiskElaboration.from_dict_label(d["risk_elaboration"], d["label"]),
                      label = d["label"],
                      offsets = RiskOffsets.from_dict(d["offsets"]),
                      __as_json__= d          
        )

    def as_json(self)->Dict[str, Any]:
        return self.__as_json__ 

@dataclass 
class ScammyNeighborDetails:
    sender: str 
    recipient: str 
    total_usd: float 
    scammer_details: RiskAccountDetails 
    __as_json__: Dict[str, Any] = field(default_factory=lambda: {}) 
    
    @staticmethod 
    @raise_as("ScammyNeighborDetails")
    def from_dict(d: Dict[str, Any]   )->ScammyNeighborDetails:
        x = ScammyNeighborDetails(**d)
        x.__as_json__ = d
        return x

    def as_json(self)->Dict[str, Any]:
        return self.__as_json__ 

@dataclass 
class SentToScammer(RiskElaboration):
    how_many_recipients: int
    how_many_scammy_recipients: int
    scammy_recipient_details: List[ScammyNeighborDetails]
    __as_json__: Dict[str, Any] = field(default_factory=lambda: {}) 

    @staticmethod
    @raise_as("SentToScammer")
    def from_dict(d: Dict[str, Any]   )->SentToScammer:
        return SentToScammer(
            how_many_recipients = d["how_many_recipients"],
            how_many_scammy_recipients = d["how_many_scammy_recipients"],
            scammy_recipient_details = [ScammyNeighborDetails.from_dict(dd) for dd in d["scammy_recipient_details"]],
            __as_json__=d
        )

    def as_json(self)->Dict[str, Any]:
        return self.__as_json__ 

@dataclass 
class FundedByScammer(RiskElaboration):
    how_many_funders: int 
    how_many_scammy_funders: int 
    scammy_funder_details: List[ScammyNeighborDetails] 
    __as_json__: Dict[str, Any] = field(default_factory=lambda: {}) 
    
    @staticmethod
    @raise_as("FundedByScammer")
    def from_dict(d: Dict[str, Any]   )->FundedByScammer: 
        x = FundedByScammer(**d)
        x.__as_json__ = d
        return x 

    def as_json(self)->Dict[str, Any]:
        return self.__as_json__ 

@dataclass 
class VerifiedDate:
    date: str 
    source: str 
    weight: float 
    __as_json__: Dict[str, Any] = field(default_factory=lambda: {}) 
    
    @staticmethod
    @raise_as("VerifiedDate")
    def from_dict(d: Dict[str, Any]   )->VerifiedDate:
        x = VerifiedDate(**d)
        x.__as_json__ = d
        return x 

    def as_json(self)->Dict[str, Any]:
        return self.__as_json__ 

@dataclass 
class VerifiedDates(RiskElaboration):
    verified_dates: List[VerifiedDate] 
    __as_json__: Dict[str, Any] = field(default_factory=lambda: {}) 

    @staticmethod 
    @raise_as("VerifiedDates")
    def from_dict(d:Dict[str,Any])->RiskElaboration:
       x = VerifiedDates(verified_dates=[VerifiedDate.from_dict(dd) for dd in d["verified_dates"]])
       x.__as_json__ = d
       return x 

    def as_json(self)->Dict[str, Any]:
        return self.__as_json__ 

@dataclass 
class RiskyZeroValuedTxs(RiskElaboration):
    how_many_neighbors: int 
    how_many_scammy_neighbors: int 
    scammy_neighbor_details: List[Dict[str,str]]
    __as_json__: Dict[str, Any] = field(default_factory=lambda: {}) 
    @staticmethod
    @raise_as("RiskyZeroValuedTxs")
    def from_dict(d: Dict[str, Any]   )->RiskyZeroValuedTxs:
        x = RiskyZeroValuedTxs(**d)
        x.__as_json__ = d
        return x 

    def as_json(self)->Dict[str, Any]:
        return self.__as_json__ 



@dataclass 
class RiskReport:
    risk_scores: RiskScores 
    reasons: List[RiskReason]    
    __as_json__: Dict[str, Any] = field(default_factory=lambda: {}) 
    @staticmethod
    @raise_as("RiskReport")
    def from_dict(d: Dict[str, Any]   )->RiskReport:
        d = snake_case_dict(d) 
        
        return RiskReport(
            risk_scores=RiskScores.from_dict(d["risk_scores"]),
            reasons = [RiskReason.from_dict(dd) for dd in d["reasons"]],
            __as_json__= d
        )
    
    def as_json(self)->Dict[str, Any]:
        return self.__as_json__ 
