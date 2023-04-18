# pai-thin-client

A client for communicating with the private-ai deidentication api. This document provides information about how to best use the client, for information on private-ai's api, follow [this link][1]

### Quick Links
1. [Installation](#installation)
2. [Usage](#usage)
3. Working with the Client(#client)
3. [Request Objects](#request-objects)

### Installation <a name=installation></a>

```
pip install paiclient
```

### Usage <a name=usage></a>

#### Simple Example
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

### Working with the Client <a name=client></a>



[https://docs.private-ai.com/reference/latest/operation/process_text_v3_process_text_post/]