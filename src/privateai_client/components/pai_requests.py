from typing import Union

import requests

from .pai_uris import PAIURIs


class PAIRequests:
    def __init__(self, uris: PAIURIs):
        self._uris = uris
        self.headers = self.base_header

    @property
    def uris(self):
        return self._uris

    @property
    def base_header(self):
        return {"Accept": "application/json"}

    def make_request(
        self,
        request_type: Union[requests.get, requests.post],
        uri: str,
        payload: dict = None,
    ):
        response = request_type(uri, json=payload, headers=self.headers)
        return response


class PAIGetRequests(PAIRequests):
    def __init__(self, uris: PAIURIs):
        """
        A class of get requests used by the client
        """
        self.request_type = requests.get
        super(PAIGetRequests, self).__init__(uris)

    def health(self):
        return self.make_request(self.request_type, self.uris.health)

    def metrics(self):
        return self.make_request(self.request_type, self.uris.metrics)

    def version(self):
        return self.make_request(self.request_type, self.uris.version)

    def diagnostics(self):
        return self.make_request(self.request_type, self.uris.diagnostics)


class PAIPostRequests(PAIRequests):
    def __init__(self, uris: PAIURIs):
        self.request_type = requests.post
        super(PAIPostRequests, self).__init__(uris)

    def process_text(self, request_object):
        return self.make_request(
            self.request_type, self.uris.process_text, request_object
        )

    def process_files_uri(self, request_object):
        return self.make_request(
            self.request_type, self.uris.process_files_uri, request_object
        )

    def process_files_base64(self, request_object):
        return self.make_request(
            self.request_type, self.uris.process_files_base64, request_object
        )

    def bleep(self, request_object):
        return self.make_request(self.request_type, self.uris.bleep, request_object)

    def reidentify_text(self, request_object):
        return self.make_request(
            self.request_type, self.uris.reidentify_text, request_object
        )
