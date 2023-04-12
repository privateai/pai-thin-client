

class PAIURIs:

    def __init__(self, schema, pai_host, port=None):
        self.valid_schemas = ['http', 'https']
        schema = schema.split('://')[0]
        if schema not in self.valid_schemas:
            raise ValueError(f"Schema must be one of the following: {', '.join(self.valid_schemas)}")
        port = f":{port}" if port else ""
        self._pai_uri = f"{schema}://{pai_host}{port}"

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