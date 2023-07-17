# Private AI Python Client

A Python client library for communicating with the Private AI API. This document provides information about how to best use the client. For more information, see Private AI's [API Documentation.][1]

### Quick Links

1. [Installation](#installation)
1. [Quick Start](#quick-start)
1. [Running the tests](#testing)
1. [Working with the Client](#client)
1. [Request Objects](#request-objects)
1. [Sample Use](#sample-use)

### Installation <a name=installation></a>

```
pip install privateai_client
```

### Quick Start <a name=quick-start></a>

```python

from privateai_client import PAIClient
from privateai_client import request_objects

url="http://localhost:8080"

client = PAIClient(url="http://localhost:8080")
text_request = request_objects.process_text_obj(text=["My sample name is John Smith"])
response = client.process_text(text_request)

print(text_request.text)
print(response.processed_text)


```

Output:

```
['My sample name is John Smith']
['My sample name is [NAME_1]']
```

### Running the tests <a name=testing></a>

We use [pytest](https://docs.pytest.org/) to run our tests in the tests folder.

To run from command line, ensure you have pytest installed, and then run `pytest` from the main project folder.

```shell
pip install -U pytest -y
pytest
```

Alternatively, you can run automatically run all tests from the Testing window in Visual Studio Code.

### Working With The Client <a name=client></a>

#### Initializing the Client

The PAI client requires a scheme, host, and optional port to initialize. 
Alternatively, a full url can be used.
Once created, the connection can be tested with the client's `ping` function

```python
scheme = 'http'
host = 'localhost'
port= '8080'
client = PAIClient(scheme, host, port)

client.ping()


url = "http://localhost:8080"
client = PAIClient(url=url)

client.ping()
```

Output:

```
True
True
```

#### Adding Authorization to the Client

```python
from privateai_client import PAIClient
# On initialization
client = PAIClient(url="http://localhost:8080", api_key='testkey')

# After initialization
client = PAIClient(url="http://localhost:8080")
client.ping()
client.add_api_key("testkey")
client.ping()
```
Output:

```
The request returned with a 401 Unauthorized
True
```


#### Making Requests

Once initialized the client can be used to make any request listed in the [Private-AI documentation][1]

Available requests:

| Client Function          | Endpoint                   |
| ------------------------ | -------------------------- |
| `get_version()`          | `/`                        |
| `ping()`                 | `/healthz`                 |
| `get_metrics()`          | `/metrics`                 |
| `get_diagnostics()`      | `/diagnostics`             |
| `process_text()`         | `/v3/process/text`         |
| `process_files_uri()`    | `/v3/process/files/uri`    |
| `process_files_base64()` | `/v3/process/files/base64` |
| `bleep()`                | `/v3/bleep`                |

Requests can be made using dictionaries:

```python
sample_text = ["This is John Smith's sample dictionary request"]
text_dict_request = {"text": sample_text}

response = client.process_text(text_dict_request)
print(response.processed_text)
```

Output:

```
["This is [NAME_1]'s sample dictionary request"]
```

or using built-in request objects:

```python
from privateai_client import request_objects

sample_text = "This is John Smith's sample process text object request"
text_request_object =  request_objects.process_text_obj(text=[sample_text])

response = client.process_text(text_request_object)
print(response.processed_text)
```

Output:

```
["This is [NAME_1]'s sample process text object request"]
```

### Request Objects <a name=request-objects></a>

Request objects are a simple way of creating request bodies without the tediousness of writing dictionaries. Every post request (as listed in the [Private-AI documentation][1]) has its own request own request object.

```python
from privateai_client import request_objects

sample_obj = request_objects.file_url_obj(uri='path/to/file.jpg')
sample_obj.uri
```

Output:

```
'path/to/file.jpg'
```

Additionally there are request objects for each nested dictionary of a request:

```python
from privateai_client import request_objects

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

Request objects can initialized by passing in all the required values needed for the request as arguments or from a dictionary, using the object's `fromdict` function. Any object can be created as per the [Private AI documentation][1].

```python
# Passing arguments
sample_data = "JVBERi0xLjQKJdPr6eEKMSAwIG9iago8PC9UaXRsZSAoc2FtcGxlKQovUHJvZHVj..."
sample_content_type = "application/pdf"

sample_file_obj = request_objects.file_obj(data=sample_data, content_type=sample_content_type)

# Passing a dictionary using .fromdict()
sample_dict = {"data": "JVBERi0xLjQKJdPr6eEKMSAwIG9iago8PC9UaXRsZSAoc2FtcGxlKQovUHJvZHVj...",
               "content_type": "application/pdf"}

sample_file_obj2 = request_objects.file_obj.fromdict(sample_dict)
```

Request objects also can be formatted as dictionaries, using the request object's `to_dict()` function:

```python
from privateai_client import request_objects

sample_text = "Sample text."
sample_accuracy = "standard"

# Create the nested request objects
sample_entity_type_selector = request_objects.entity_type_selector_obj(type="DISABLE", value=['HIPAA'])
sample_entity_detection = request_objects.entity_detection_obj(
    entity_types=[sample_entity_type_selector],
    accuracy=sample_accuracy
)

# Create the request object
sample_request = request_objects.process_text_obj(text=[sample_text], entity_detection=sample_entity_detection)

# All nested request objects are also formatted
print(sample_request.to_dict())
```

Output:

```
{
 'text': ['Sample text.'],
 'link_batch': False,
 'entity_detection': {'accuracy': 'standard', 'entity_types': [{'type': 'DISABLE', 'value': ['HIPAA']}], 'filter': [], 'return_entity': True},
 'processed_text': {'type': 'MARKER', 'pattern': '[UNIQUE_NUMBERED_ENTITY_TYPE]'}
}
```

### Sample Use <a name=sample-use></a>

#### Processing a directory of files

```python
from privateai_client import PAIClient
from privateai_client.objects import request_objects
import os
import logging

file_dir = "/path/to/file/directory"
client = PAIClient(url="http://localhost:8080")
for file_name in os.listdir(file_dir):
    filepath = os.path.join(file_dir, file_name)
    if not os.path.isfile(filepath):
        continue
    req_obj = request_objects.file_url_obj(uri=filepath)
    # NOTE this method of file processing requires the container to have an the input and output directories mounted
    resp = client.process_files_uri(req_obj)
```

#### Processing a Base64 file

```python
from privateai_client import PAIClient
from privateai_client.objects import request_objects
import base64
import os
import logging

file_dir = "/path/to/your/file"
file_name = 'sample_file.pdf'
filepath = os.path.join(file_dir,file_name)
file_type= "type/of_file" #eg. application/pdf
client = PAIClient(url="http://localhost:8080")

# Read from file
with open(filepath, "rb") as b64_file:
    file_data = base64.b64encode(b64_file.read())
    file_data = file_data.decode("ascii")

# Make the request
file_obj = request_objects.file_obj(data=file_data, content_type=file_type)
request_obj = request_objects.file_base64_obj(file=file_obj)
resp = client.process_files_base64(request_object=request_obj)

# Write to file
with open(os.path.join(file_dir,f"redacted-{file_name}"), 'wb') as redacted_file:
    processed_file = resp.processed_file.encode("ascii")
    processed_file = base64.b64decode(processed_file, validate=True)
    redacted_file.write(processed_file)
```

#### Bleep an audio file

```python
from privateai_client import PAIClient
from privateai_client.objects import request_objects
import base64
import os
import logging

file_dir = "/path/to/your/file"
file_name = 'sample_file.pdf'
filepath = os.path.join(file_dir,file_name)
file_type= "type/of_file" #eg. audio/mp3 or audio/wav
client = PAIClient(url="http://localhost:8080")


file_dir = "/home/adam/workstation/file_processing/test_audio"
file_name = "test_audio.mp3"
filepath = os.path.join(file_dir,file_name)
file_type = "audio/mp3"
with open(filepath, "rb") as b64_file:
    file_data = base64.b64encode(b64_file.read())
    file_data = file_data.decode("ascii")

file_obj = request_objects.file_obj(data=file_data, content_type=file_type)
timestamp = request_objects.timestamp_obj(start=1.12, end=2.14)
request_obj = request_objects.bleep_obj(file=file_obj, timestamps=[timestamp])

resp = client.bleep(request_object=request_obj)
with open(os.path.join(file_dir,f"redacted-{file_name}"), 'wb') as redacted_file:
    processed_file = resp.bleeped_file.encode("ascii")
    processed_file = base64.b64decode(processed_file, validate=True)
    redacted_file.write(processed_file)
```

#### Working with structured data

Redacting a data frame column by column

##### NOTE: When de-identifying smaller strings of structured data, more accurate results can be achieved by passing in the whole column as a string (including the header) and a delimiter. For example, making a request row by row for a column named SSN will return data identified as PHONE_NUMBER, even when the header is included

```python
# Working with data frames
import pandas as pd
from privateai_client import PAIClient
from privateai_client.objects import request_objects

client = PAIClient(url="http://localhost:8080")
data_frame = pd.DataFrame(
    {
        "Name": [
            "Braund, Mr. Owen Harris",
            "Allen, Mr. William Henry",
            "Bonnell, Miss. Elizabeth",
        ],
        "Age": [22, 35, 58],
        "Sex": ["male", "male", "female"],
    }
)
print(data_frame)
text_req = request_objects.process_text_obj(text=[])
for column in data_frame.columns:
    text_req.text.append(f"{column}:{' | '.join([str(row) for row in data_frame[column]])}")

resp = client.process_text(text_req)
redacted_data = dict()
for row in resp.processed_text:
    data = row.split(':',1)
    redacted_data[data[0]] = data[1].split(' | ')
redacted_data_frame = pd.DataFrame(redacted_data)
print(redacted_data_frame)
```

Redacting cell by cell for columns with large text content

```python
# Working with data frames
import pandas as pd
from privateai_client import PAIClient
from privateai_client.objects import request_objects

client = PAIClient(url="http://localhost:8080")
data_frame = pd.DataFrame(
    {
        "Book": [
            "Treasure Island",
            "Moby Dick",
        ],
        "chapter": [1,1],
        "paragraph": [1,1],
        "text": ["The Old Sea-dog at the Admiral Benbow\nSquire Trelawney, Dr. Livesey, and the rest of...",
                 "Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse..."
                 ]
    }
)
obj = request_objects.process_text_obj
func = client.process_text
data_frame['text'] = [(lambda x: func(obj(text=[x])).processed_text[0])(row) for row in data_frame['text']]
```

Reidentifying Text
```python
from privateai_client import PAIClient
from privateai_client import request_objects

client = PAIClient(url="http://localhost:8080")

# Deidentify the text
initial_text = 'My name is John. I work for Private AI'
request_obj = request_objects.process_text_obj(text=[initial_text])
response_obj = client.process_text(request_obj)

# Build reidentify request object from the deidentified response
new_request_obj = response_obj.get_reidentify_request()
# Call the reidentify Route
new_response_obj = client.reidentify_text(new_request_obj)
print(new_response_obj.body)
```

[1]: https://docs.private-ai.com/reference/latest/operation/process_text_v3_process_text_post/
