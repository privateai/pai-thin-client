

class PAIURIs:

    def __init__(self, pai_uri):
        self._pai_uri = pai_uri

    @property
    def pai_uri(self):
        return self._pai_uri
    
    @property
    def api_version(self):
        return "v3"

    @property
    def bleep(self):
        return self._create_uri(self.pai_uri, self.api_version, "bleep")

    @property
    def health(self):
        return self._create_uri(self.pai_uri, "healthz")
    
    @property
    def metrics(self):
        return self._create_uri(self.pai_uri, "metrics")
    
    @property
    def process_text(self):
        return self._create_uri(self.pai_uri, self.api_version, "process", "text")
    
    @property
    def process_files_uri(self):
        return self._create_uri(self.pai_uri, self.api_version, "process" "files", "uri")
    
    @property
    def process_files_base64(self):
        return self._create_uri(self.pai_uri, self.api_version, "process" "files", "base64")

    @property
    def version(self):
        return self._create_uri(self.pai_uri, "")

    def _create_uri(self, *args):
        return "/".join([x.strip("/") for x in args])