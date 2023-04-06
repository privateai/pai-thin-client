import logging 
from typing import Dict, List, str, bool 
from components import PAIGetRequests, PAIPostRequests, PAIURIs

logger = logging.getLogger(__name__)




class PAIClient:
    """
    Client used to connect to private-ai's deidentication service   
    """
    def __init__(self, pai_url, api_key=None):
        # Add source url
        self.uris = PAIURIs(pai_url)
        self.get = PAIGetRequests(self.uris)
        self.post = PAIPostRequests(api_key, self.uris)
        # Hit the health endpoint to verifya
        self.ping()

    def ping(self):
        """
        Makes a call to the Private-AI service's health endpoint. 
        Can be used as a validator to ensure the service is running.
        """
        response = self.get.health()
        if response.status_code != 200:
            logger.warning(f"The Private AI server cannot be reached")
            return False
        logger.info(f"Connected to {self.uris.pai_uri}")
        return True

    def get_metrics(self):
        """
        Returns information about the Private-AI's server
        """
        response = self.get.metrics
        return response.text
    
    def process_text_request(self, text: List, link_batch, ):
        """
        Used to deidentify text 
        """
        self.uri

    








