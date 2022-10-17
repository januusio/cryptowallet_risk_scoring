
class RiskReportException(Exception):
    def __init__(self, msg: str):
        self.message = msg 
        super().__init__(self.message)

class DeserializationException(RiskReportException):

    def __init__(self, msg: str):
        self.message = f"\nCould not deserialize the following class: {msg}\nPlease PLEASE contact januus to file a bug" 
        super().__init__(self.message)

class UnknownLabelException(RiskReportException):
    def __init__(self, msg: str):
        self.message = f"Unknown label: {msg}\nPlease PLEASE contact januus to file a bug" 
        super().__init__(self.message)


class EndPointException(RiskReportException):
    def __init__(self):
        self.message = f"Unable to connect to endpoint. Please make sure you are connected to the internet and that 'januus_riskreport' is updated to the most recent version." 
        super().__init__(self.message)

class RequestedNullReport(RiskReportException):
    def __init__(self):
        self.message = "You asked for a risk report but didn't provide any data about the entity. Try adding 'eth_addresses' or 'btc_addresses'" 
        super().__init__(self.message)
