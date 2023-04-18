# pai-thin-client

A client for communicating with the private-ai deidentication api

### Quick Links
1. [Installation](#installation)

### Installation <a name=installation></a>

```
pip install paiclient
```

### Sample Usage <a name=sample-usage></a>

```python

from paiclient import PAIClient
from paiclient import request_objects

schema = "http"
host = "localhost"
port = "8080"

client = PAIClient(schema=schema, host=host, port=port)

text_request = request_objects.process_text(text=["My sample name is John Smith"])
text_request.text

response = client.process_text(text_request)
response.processed_text


```
Output:
```
["My sample name is John Smith"]
['My sample name is [NAME_1]']
```