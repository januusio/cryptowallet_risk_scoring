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
                print(args, kwargs)
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

        if label == "sent-to-bad-actor":
            return SentToBadActor.from_dict(d)
        
        elif label == "funded-by-bad-actor": 
            return FundedByBadActor.from_dict(d) 
        
        elif label == "bad-zero-valued-txs": 
            return BadZeroValuedTxs.from_dict(d)
        
        elif label == "is-bad-actor" or label == "is-threat":
            return IsBadActor.from_dict(d) 
        
        elif label == "date-verification": 
            return VerifiedDates.from_dict(d)        
        
        else: 
            return UnknownElaboration.from_dict(d)


    def __summerize__(self)->Optional[SummerizedInteractions]:
        return None

@dataclass 
class IsBadActor(RiskElaboration):
    risk_details: List[RiskAccountDetails]         
    __as_json__: Dict[str, Any] = field(default_factory=lambda: {}) 

    @staticmethod 
    @raise_as("IsBadActor") 
    def from_dict(d: Dict[str, Any]   )->IsBadActor:
        x = IsBadActor(**d)
        x.__as_json__ = d
        return x

    def as_json(self)->Dict[str, Any]:
        return self.__as_json__ 

    def __summerize__(self)->Optional[SummerizedInteractions]:
        ts = TagSummary(address="", tagged_as=[])
        for d in self.risk_details:
            ts["address"] = d["address"]
            for factor in d["risk_factors"]:
                ts["tagged_as"].append(factor["actor_type"])
        return SummerizedInteractions(percentage_of_category=100.0, bad_nbrs=[ts])
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
class BadNeighborDetails:
    sender: str 
    recipient: str 
    total_usd: float 
    risk_details: RiskAccountDetails 
    __as_json__: Dict[str, Any] = field(default_factory=lambda: {}) 
    
    @staticmethod 
    @raise_as("BadNeighborDetails")
    def from_dict(d: Dict[str, Any]   )->BadNeighborDetails:
        x = BadNeighborDetails(**d)
        x.__as_json__ = d
        return x

    def as_json(self)->Dict[str, Any]:
        return self.__as_json__ 

class TagSummary(TypedDict):
    address: str
    tagged_as: List[str]

class SummerizedInteractions(TypedDict):
    percentage_of_category: float
    bad_nbrs: List[TagSummary]


@dataclass 
class SentToBadActor(RiskElaboration):
    how_many_recipients: int
    how_many_bad_recipients: int
    bad_recipient_details: List[BadNeighborDetails]
    __as_json__: Dict[str, Any] = field(default_factory=lambda: {}) 

    @staticmethod
    @raise_as("SentToBadActor")
    def from_dict(d: Dict[str, Any]   )->SentToBadActor:
        return SentToBadActor(
            how_many_recipients = int(d["how_many_recipients"]),
            how_many_bad_recipients = int(d["how_many_bad_recipients"]),
            bad_recipient_details = [BadNeighborDetails.from_dict(dd) for dd in d["bad_recipient_details"]],
            __as_json__=d
        )

    def as_json(self)->Dict[str, Any]:
        return self.__as_json__ 


    def __summerize__(self)->Optional[SummerizedInteractions]:
        bad_nbrs = []
        for nbr in self.bad_recipient_details:
            details = nbr.risk_details
            bad_nbrs.append(TagSummary(address = nbr.recipient,
                                       tagged_as = [x["actor_type"] for x in details["risk_factors"]]))
        return SummerizedInteractions(percentage_of_category= 100.0 * self.how_many_bad_recipients / self.how_many_recipients,
                                      bad_nbrs=bad_nbrs)


@dataclass 
class FundedByBadActor(RiskElaboration):
    how_many_funders: int 
    how_many_bad_funders: int 
    bad_funder_details: List[BadNeighborDetails] 
    __as_json__: Dict[str, Any] = field(default_factory=lambda: {}) 
    
    @staticmethod
    @raise_as("FundedByBadActor")
    def from_dict(d: Dict[str, Any]   )->FundedByBadActor: 
        x = FundedByBadActor(**d)
        x.how_many_bad_funders = int(x.how_many_bad_funders)
        x.how_many_funders = int(x.how_many_funders)
        x.__as_json__ = d
        return x 

    def as_json(self)->Dict[str, Any]:
        return self.__as_json__ 

    def __summerize__(self)->Optional[SummerizedInteractions]:
        bad_nbrs = []
        for nbr in self.bad_funder_details:
            assert isinstance(nbr, Dict)
            details = nbr["risk_details"]
            bad_nbrs.append(TagSummary(address = details["address"],
                                       tagged_as = [x["actor_type"] for x in details["risk_factors"]]))
        return SummerizedInteractions(percentage_of_category= 100.0 * self.how_many_bad_funders / self.how_many_funders,
                                      bad_nbrs=bad_nbrs)


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
        x.weight = float(x.weight)
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
       for date_info in d["verified_dates"]:
           date_info.setdefault("weight", 0.0)
       x = VerifiedDates(verified_dates=[VerifiedDate.from_dict(dd) for dd in d["verified_dates"]])
       x.__as_json__ = d
       return x 

    def as_json(self)->Dict[str, Any]:
        return self.__as_json__ 

@dataclass 
class UnknownElaboration(RiskElaboration):
    __as_json__: Dict[str, Any] = field(default_factory=lambda: {}) 

    @staticmethod 
    @raise_as("UnknownElaboration")
    def from_dict(d:Dict[str,Any])->RiskElaboration:
       x = UnknownElaboration()
       x.__as_json__ = d
       return x 

    def as_json(self)->Dict[str, Any]:
        return self.__as_json__ 

@dataclass 
class BadZeroValuedTxs(RiskElaboration):
    how_many_neighbors: int 
    how_many_bad_neighbors: int 
    bad_neighbor_details: List[Dict[str,Any]]
    __as_json__: Dict[str, Any] = field(default_factory=lambda: {}) 
    @staticmethod
    @raise_as("BadZeroValuedTxs")
    def from_dict(d: Dict[str, Any]   )->BadZeroValuedTxs:
        x = BadZeroValuedTxs(**d)
        x.__as_json__ = d
        x.how_many_neighbors = int(x.how_many_neighbors)
        x.how_many_bad_neighbors = int(x.how_many_bad_neighbors)
        return x 

    def as_json(self)->Dict[str, Any]:
        return self.__as_json__ 


    def __summerize__(self)->Optional[SummerizedInteractions]:
        bad_nbrs = []
        for nbr in self.bad_neighbor_details:
            assert isinstance(nbr, Dict)
            details = nbr["risk_details"]
            bad_nbrs.append(TagSummary(address = details["address"],
                                       tagged_as = [x["actor_type"] for x in details["risk_factors"]]))
        return SummerizedInteractions(percentage_of_category= 100.0 * self.how_many_bad_neighbors / self.how_many_neighbors,
                                      bad_nbrs=bad_nbrs)


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

    def summerize_risky_interactions(self)->Dict[str, SummerizedInteractions]:
        ret = {}
        for reason in self.reasons:
            sww = reason.risk_elaboration.__summerize__()
            if sww is not None:
               ret[reason.label] = sww
        return ret
