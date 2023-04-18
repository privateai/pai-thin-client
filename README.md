# pai-thin-client

A client for communicating with the private-ai deidentication api. This document provides information about how to best use the client, for information on private-ai's api, follow [this link][1]

### Quick Links
1. [Installation](#installation)
2. [Usage](#usage)
3. [Working with the Client](#client)
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

#### Initializing the Client

the PAI client requires a scheme, host and optional port to initialize.
Once created, the connection can be tested with the client's `ping` function

```python
from paiclient import PAIClient
scheme = 'http'
host = 'localhost'
port= '8080'
client = PAIClient(scheme, host, port)
 
client.ping()
```
Output:
```
True
```

#### Making Requests

Once initialized the client can be used to make any request listed in the [Private-Ai documentation][1]

Available requests:

| Client Function        | Endpoint                   |
| ---------------        | --------                   |
| `get_version`          | `/`                        |
| `get_metrics`          | `/metrics`                 |
| `process_text`         | `/v3/process/text`         |
| `process_files_url`    | `/v3/process/files/uri`    |
| `process_files_base64` | `/v3/process/files/base64` |
| `bleep`                | `/v3/bleep`                |

Requests can be made using dictionaries:
```python
text_dict_request = {"text": ["This is John Smith's sample request"]}

response = client.process_text(text_dict_request)
response.processed_text
```
Output:
```
["This is [NAME_1]'s sample request"]
```

or using built-in request objects:

```python
from paiclient import request_objects

sample_text = "This is John Smith's sample request"
text_request_object =  request_objects.process_text_obj(text=[sample_text])

response = client.process_text(text_request_object)
response.processed_text
```
Output:
```
["This is [NAME_1]'s sample request"]
```


[1]:https://docs.private-ai.com/reference/latest/operation/process_text_v3_process_text_post/