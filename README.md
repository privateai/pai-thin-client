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
sample_text = "This is John Smith's sample dictionary request"
text_dict_request = {"text": sample_text}

response = client.process_text(text_dict_request)
response.processed_text
```
Output:
```
["This is [NAME_1]'s sample dictionary request"]
```

or using built-in request objects:

```python
from paiclient import request_objects

sample_text = "This is John Smith's sample process text object request"
text_request_object =  request_objects.process_text_obj(text=[sample_text])

response = client.process_text(text_request_object)
response.processed_text
```
Output:
```
["This is [NAME_1]'s sample process text object request"]
```


### Request Objects <a name=request-objects></a>
Request objects are a simple way of creating request bodies without the tediousness of writing dictionaries. Every post request (as listed in the [Private-Ai documentation][1]) has its own request own request object. 
```python
from paiclient import request_objects

sample_obj = request_objects.file_url_obj(uri='path/to/file.jpg')
sample_obj.uri
```
Output:
```
'path/to/file.jpg'
```

Additionally there are request objects for each nested dictionary of a request:
```python 
from paiclient import request_objects

sample_text = "This is John Smith's sample process text object request where names won't be removed"

# sub-dictionary of entity_detection
sample_entity_type_selector = request_objects.entity_type_selector_obj(type="DISABLE", value=['NAME', 'NAME_GIVEN', 'NAME_FAMILY'])

# sub-dictionary of a process text request
sample_entity_detection = request_objects.entity_detection_obj(entity_types=[sample_entity_type_selector])

# request object created using the sub-dictionaries
sample_request = request_objects.process_text_obj(text=[sample_text], entity_detection=sample_entity_detection)
response = client.process_text(sample_request)
print(response.processed_text)
```
Output:
```
["This is John Smith's sample process text object request where names won't be removed"]
```

#### Building Request Objects
Request objects can initialized by passing in all the required values needed for the request as arguments or from a dictionary:
```python
# Passing arguments 
sample_data = "JVBERi0xLjQKJdPr6eEKMSAwIG9iago8PC9UaXRsZSAoc2FtcGxlKQovUHJvZHVj..."
sample_content_type = "application/pdf"

sample_file_obj = request_objects.file_obj(data=sample_data, content_type=sample_content_type)

# Passing a dictionary
sample_dict = {"data": "JVBERi0xLjQKJdPr6eEKMSAwIG9iago8PC9UaXRsZSAoc2FtcGxlKQovUHJvZHVj...",
               "content_type": "application/pdf"}

sample_file_obj2 = request_objects.file_obj.fromdict(sample_dict)
```

Request objects can be formatted as dictionaries:
```python
from paiclient import request_objects

sample_text = "Sample text."
# Create the nested request objects
sample_entity_type_selector = request_objects.entity_type_selector_obj(type="DISABLE", value=['HIPAA'])
sample_entity_detection = request_objects.entity_detection_obj(entity_types=[sample_entity_type_selector])
# Create the request object
sample_request = request_objects.process_text_obj(text=[sample_text], entity_detection=sample_entity_detection)

# All nested objects are also formatted
print(sample_request.to_dict())
```
Output:
```
{
    'text': ['Sample text.'], 
    'link_batch': False, 
    'entity_detection': {'accuracy': 'high', 
                        'entity_types': [{
                                            'type': 'DISABLE', 
                                            'value': ['HIPAA']
                                        }
                        ], 
                        'filter': [], 
                        'return_entity': True
    }, 
    'processed_text': {'type': 'MARKER', 
                      'pattern': '[UNIQUE_NUMBERED_ENTITY_TYPE]'
    }
}
```


[1]:https://docs.private-ai.com/reference/latest/operation/process_text_v3_process_text_post/