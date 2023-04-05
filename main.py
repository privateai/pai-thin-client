import requests
import logging 
from typing import Union
logger = logging.getLogger(__name__)






class PAIClient:
    """
    Client used to connect to private-ai's deidentication service   
    """
    def __init__(self, pai_url, api_key):
        # Add source url
        self.endpoints = PAIEndpoints(pai_url)
        self.get = PAIGetRequests(self.endpoints)
        self.post = PAIPostRequests(api_key, self.endpoints)
        # Hit the health endpoint to verify
        self.ping()

    def ping(self):
        """
        Makes a call to the Private-AI service's health endpoint. 
        Can be used as a validator to ensure the service is running.
        """
        response = self.get.health
        if response.status_code != 200:
            logger.warning(f"The Private AI server cannot be reached")
            return False
        logger.info(f"Connected to {self.endpoints.pai_url}")
        return True

    def get_metrics(self):
        """
        Returns information about the Private-AI's server
        """
        response = self.get.metrics
        return response.text
    



class PAIEndpoints:

    def __init__(self, pai_url):
        self._pai_url = pai_url

    @property
    def pai_url(self):
        return self._pai_url
    
    @property
    def version(self):
        return "v3"

    @property
    def bleep(self):
        return self._create_endpoint(self.pai_url, self.version, "bleep")

    @property
    def health(self):
        return self._create_endpoint(self.pai_url, "healthz")
    
    @property
    def metrics(self):
        return self._create_endpoint(self.pai_url, "metrics")
    
    @property
    def process_text(self):
        return self._create_endpoint(self.pai_url, self.version, "process", "text")
    
    @property
    def process_files_uri(self):
        return self._create_endpoint(self.pai_url, self.version, "process" "files", "uri")
    
    @property
    def process_files_base64(self):
        return self._create_endpoint(self.pai_url, self.version, "process" "files", "base64")

    @property
    def version(self):
        return self._create_endpoint(self.pai_url, "")

    def _create_endpoint(self, *args):
        return "/".join([x.strip("/") for x in args])

class PAIRequests:
    
    def __init__(self, endpoints:PAIEndpoints):

        self._endpoints = endpoints

    @property
    def endpoints(self):
        return self._endpoints
    
    def make_request(self, request_type: Union[requests.get, requests.post], endpoint:str, payload: dict=None):
        return requests.request_type



class PAIGetRequests(PAIRequests):

    def __init__(self, endpoints:PAIEndpoints):
        """
        A class of get requests used by the client
        """
        super(PAIGetRequests, self).__init__(endpoints)
    
    @property
    def health(self):
        return requests.get(self.endpoints.health)
    
    @property
    def metrics(self):
        return requests.get(self.endpoints.metrics)
    
    @property
    def version(self):
        return requests.get(self.endpoints.version)
    
class PAIPostRequests(PAIRequests):

    def __init__(self, api_key:str, endpoints:PAIEndpoints):
        self._api_key = api_key
        self.request_type = requests.post
        super(PAIGetRequests, self).__init__(endpoints)



    def process_text(self, request_object):
        return self.make_request(self.request_type, self.endpoints.process_text, request_object)






