import pytest
from src.components import *

# File Tests
def test_file_initializer():
    file = File(data="test", content_type="application/pdf")
    assert file.data == "test"
    assert file.content_type == "application/pdf"

def test_file_initializer_fromdict():
    file = File.fromdict({"data":"test", "content_type":"application/pdf"})
    assert file.data == "test"
    assert file.content_type == "application/pdf"

def test_file_invalid_initialize_fromdict():
    error_msg = "File can only accept the values 'data' and 'content_type'"
    with pytest.raises(TypeError) as excinfo:
        File.fromdict({"data":"test", "content_type":"application/pdf", "garbage":"value"})
    assert error_msg in str(excinfo.value)

def test_file_data_validator():
    error_msg = "data must be string-type"
    with pytest.raises(TypeError) as excinfo:
        file = File(data=12, content_type="application/pdf")
    assert error_msg in str(excinfo.value)

def test_file_content_type_validator():
    error_msg = "strawberry/filling is not valid. File.content_type can only be one of the following:"
    with pytest.raises(ValueError) as excinfo:
        file = File(data="test", content_type="strawberry/filling")
    assert error_msg in str(excinfo.value)

def test_file_setters():
    file = File(data="test", content_type="application/pdf")
    file.data = "new test"
    file.content_type = "application/xml"
    assert file.data == "new test"
    assert file.content_type == "application/xml"

# Filter Selector Tests
def test_filter_selector_initializer():
    test_type = "ALLOW"
    test_pattern = "[A-Z]"
    filter_selector = FilterSelector(type=test_type, pattern=test_pattern)
    assert filter_selector.type == test_type
    assert filter_selector.pattern == test_pattern

def test_filter_selector_initialize_fromdict():
    test_type = "ALLOW"
    test_pattern = "[A-Z]"
    test_dict = {"type": test_type, "pattern": test_pattern}
    filter_selector = FilterSelector.fromdict(test_dict)
    assert filter_selector.type == test_type
    assert filter_selector.pattern == test_pattern

def test_filter_selector_invalid_initialize_fromdict():
    with pytest.raises(TypeError) as excinfo:
        FilterSelector.fromdict({"type": "ALLOW", "pattern": "[A-Z]", "fake_key": "fake_value"})
    assert "FilterSelector can only accept the values 'type' and 'pattern'" in str(excinfo.value)

def test_filter_selector_setters():
    test_type = "ALLOW"
    test_pattern = "[A-Z]"
    filter_selector = FilterSelector(type=test_type, pattern=test_pattern)
    filter_selector.type = "BLOCK"
    filter_selector.pattern = "*1"
    
    assert filter_selector.type == "BLOCK"
    assert filter_selector.pattern == "*1"

def test_filter_selector_type_validator():
    test_type = "JUNK"
    test_pattern = "[A-Z]"
    with pytest.raises(ValueError) as excinfo:
        FilterSelector(type=test_type, pattern=test_pattern)
    assert " is not valid. FilterSelector.type can only be one of the following: " in str(excinfo.value)

def test_filter_selector_pattern_validator():
    test_type = "ALLOW"
    test_pattern = 12
    with pytest.raises(TypeError) as excinfo:
        FilterSelector(type=test_type, pattern=test_pattern)
    assert "FilterSelector.pattern must be of type string" in str(excinfo.value)

def test_filter_to_dict():
    test_type = "ALLOW"
    test_pattern = "[A-Z]"
    filter_selector = FilterSelector(type=test_type, pattern=test_pattern)
    filter_dict = filter_selector.to_dict()
    assert filter_dict["type"]== test_type
    assert filter_dict["pattern"] == test_pattern

# Entity Type Selector Tests
def test_entity_type_selector_initializer():
    test_type = "DISABLE"

    entity_type_selector = EntityTypeSelector(type=test_type)
    assert entity_type_selector.type == test_type
    assert entity_type_selector.value == []

def test_entity_type_selector_initialize_fromdict():
    entity_type_obj = EntityTypeSelector.fromdict({"type":"ENABLE", "value":["NAME"]})
    assert entity_type_obj.type == "ENABLE"
    assert entity_type_obj.value == ["NAME"]

def test_entity_type_selector_invalid_initialize_fromdict():
    error_msg = "EntityTypeSelector can only accept the values 'type' and 'value'"
    with pytest.raises(TypeError) as excinfo:
        EntityTypeSelector.fromdict({"type":"ENABLE", "value":["NAME"], "garbage":"value"})
    assert error_msg in str(excinfo.value)

def test_entity_type_selector_setters():
    entity_type_obj = EntityTypeSelector(type="ENABLE", value=['LOCATION'])
    entity_type_obj.type = "DISABLE"
    assert entity_type_obj.type == "DISABLE"

def test_entity_type_selector_type_validator():
    error_msg = "'JUNK' is not valid. EntityTypeSelector.type can only be one of the following: " 
    entity_type_obj = EntityTypeSelector(type="ENABLE", value=['LOCATION'])
    with pytest.raises(ValueError) as excinfo:
        entity_type_obj.type = 'JUNK'
    assert error_msg in str(excinfo.value)

def test_entity_type_selector_value_validator():
    error_msg = "EntityTypeSelector.value must be of type list"
    with pytest.raises(TypeError) as excinfo:
        EntityTypeSelector(type="ENABLE", value={})
    assert error_msg in str(excinfo.value)

def test_entity_type_selector_to_dict():
    entity_type_obj = EntityTypeSelector.fromdict({"type":"ENABLE", "value":["NAME"]}).to_dict()
    assert entity_type_obj["type"] == "ENABLE"
    assert entity_type_obj["value"] == ["NAME"]

# Entity Detection Tests
def test_entity_detection_default_initializer():
    entity_detection = EntityDetection()
    assert entity_detection.accuracy == "high"
    assert entity_detection.entity_types == []
    assert entity_detection.filter == []
    assert entity_detection.return_entity == True

def test_entity_detection_initializer():
    entity_detection_obj = EntityDetection(accuracy="high",
                                           entity_types=[EntityTypeSelector(type="ENABLE")],
                                           filter=[FilterSelector(type="ALLOW", pattern="hey")],
                                           return_entity=False
    )
    assert entity_detection_obj.accuracy == "high"
    assert type(entity_detection_obj.entity_types[0]) is EntityTypeSelector
    assert type(entity_detection_obj.filter[0]) is FilterSelector
    assert entity_detection_obj.return_entity is False


def test_entity_detection_initialize_fromdict():
    entity_detection = EntityDetection.fromdict({"accuracy":"high", 
                                                 "entity_types":[EntityTypeSelector(type="ENABLE").to_dict()],
                                                 "filter": [FilterSelector(type="ALLOW", pattern="hey").to_dict()],
                                                 "return_entity": False
                        })
    assert entity_detection.accuracy == "high"
    assert type(entity_detection.entity_types[0]) is EntityTypeSelector
    assert type(entity_detection.filter[0]) is FilterSelector
    assert entity_detection.return_entity is False

def test_entity_detection_invalid_initialize_fromdict():
    error_msg = "EntityDetection can only accept the values 'accuracy', 'entity_types', 'filter' and 'return_entity'"
    with pytest.raises(TypeError) as excinfo:
        EntityDetection.fromdict({"accuracy":"high", 
                                  "entity_types":[EntityTypeSelector(type="ENABLE").to_dict()],
                                  "filter": [FilterSelector(type="ALLOW", pattern="hey").to_dict()],
                                  "return_entity": False,
                                  "garbage": "value"
        })
    assert error_msg in str(excinfo.value)

def test_entity_detection_setters():
    entity_detection_obj = EntityDetection.fromdict({"accuracy":"high", 
                                                 "entity_types":[EntityTypeSelector(type="ENABLE").to_dict()],
                                                 "filter": [FilterSelector(type="ALLOW", pattern="hey").to_dict()],
                                                 "return_entity": False
    })
    entity_detection_obj.accuracy = 'standard'
    entity_detection_obj.return_entity = True
    assert entity_detection_obj.accuracy == 'standard'
    assert entity_detection_obj.return_entity == True

def test_entity_detection_accuracy_validator():
    error_msg = "junk is not valid. EntityDetection.accuracy can only be one of the following: "
    entity_detection_obj = EntityDetection.fromdict({"accuracy":"high", 
                                                 "entity_types":[EntityTypeSelector(type="ENABLE").to_dict()],
                                                 "filter": [FilterSelector(type="ALLOW", pattern="hey").to_dict()],
                                                 "return_entity": False
    })
    with pytest.raises(ValueError) as excinfo:
        entity_detection_obj.accuracy = "junk"
    assert error_msg in str(excinfo.value)

def test_entity_detection_entity_types_validator():
    error_msg = "EntityDetection.entity_types can only contain EntityTypeSelector objects"
    with pytest.raises(ValueError) as excinfo:
        EntityDetection(accuracy="high",
            entity_types=["junk"],
            filter=[FilterSelector(type="ALLOW", pattern="hey")],
            return_entity=False
        )
    assert error_msg in str(excinfo.value)

def test_entity_detection_entity_types_validator():
    error_msg = "EntityDetection.filter can only contain FilterSelector objects"
    with pytest.raises(ValueError) as excinfo:
        EntityDetection(accuracy="high",
            entity_types=[EntityTypeSelector(type="ENABLE")],
            filter=["junk"],
            return_entity=False
        )
    assert error_msg in str(excinfo.value)

def test_entity_detection_return_entity_validator():
    error_msg = "EntityDetection.return_entity must be of type bool"
    entity_detection_obj = EntityDetection.fromdict({"accuracy":"high", 
                                                 "entity_types":[EntityTypeSelector(type="ENABLE").to_dict()],
                                                 "filter": [FilterSelector(type="ALLOW", pattern="hey").to_dict()],
                                                 "return_entity": False
    })
    with pytest.raises(ValueError) as excinfo:
        entity_detection_obj.return_entity = "junk"
    assert error_msg in str(excinfo.value)

def test_entity_detection_to_dict():
    entity_detection_obj = EntityDetection(accuracy="high",
                                           entity_types=[EntityTypeSelector(type="ENABLE")],
                                           filter=[FilterSelector(type="ALLOW", pattern="hey")],
                                           return_entity=False
    ).to_dict()
    assert entity_detection_obj["accuracy"] == "high"
    assert type(entity_detection_obj["entity_types"][0]) is dict
    assert type(entity_detection_obj["filter"][0]) is dict
    assert entity_detection_obj["return_entity"] is False

# Processed Text Tests
def test_processed_text_default_initializer():
    processed_text = ProcessedText()
    assert processed_text.type == "MARKER"
    assert processed_text.pattern == "[UNIQUE_NUMBERED_ENTITY_TYPE]"

def test_processed_text_initializer():
    processed_text = ProcessedText(type="MASK", pattern= "*ALL_ENTITY_TYPES*")
    assert processed_text.type == "MASK"
    assert processed_text.pattern == "*ALL_ENTITY_TYPES*"

def test_processed_text_initialize_fromdict():
    processed_text = ProcessedText.fromdict({"type":"MARKER","pattern":"[UNIQUE_NUMBERED_ENTITY_TYPE]"})
    assert processed_text.type == "MARKER"
    assert processed_text.pattern == "[UNIQUE_NUMBERED_ENTITY_TYPE]"

def test_processed_text_invalid_initialize_fromdict():
    error_msg = "ProcessedText can only accept the values 'type' and 'pattern'"
    with pytest.raises(TypeError) as excinfo:
        ProcessedText.fromdict({"type":"MARKER","pattern":"[UNIQUE_NUMBERED_ENTITY_TYPE]", "junk":"value"})
    assert error_msg in str(excinfo.value)

def test_processed_text_setters():
    processed_text = ProcessedText()
    processed_text.type = "MASK"
    processed_text.pattern = "*ALL_ENTITY_TYPES*"
    assert processed_text.type == "MASK"
    assert processed_text.pattern == "*ALL_ENTITY_TYPES*"

def test_processed_text_type_validator():
    error_msg = "junk is not valid. ProcessedText.type can only be one of the following: "
    with pytest.raises(ValueError) as excinfo:
        ProcessedText.fromdict({"type":"junk","pattern":"[UNIQUE_NUMBERED_ENTITY_TYPE]"})
    assert error_msg in str(excinfo.value)

def test_processed_text_pattern_validator():
    error_msg = "junk is not valid. ProcessedText.pattern can only be one of the following: "
    with pytest.raises(ValueError) as excinfo:
        ProcessedText.fromdict({"type":"MASK","pattern":"junk"})
    assert error_msg in str(excinfo.value)

def test_processed_text_to_dict():
    processed_text = ProcessedText(type="MASK", pattern= "*ALL_ENTITY_TYPES*").to_dict()
    assert processed_text["type"] == "MASK"
    assert processed_text["pattern"] == "*ALL_ENTITY_TYPES*"

# PDF Options Tests
def test_pdf_options_default_initializer():
    pdf_options = PDFOptions()
    assert pdf_options.density == 150

def test_pdf_options_initializer():
    pdf_options = PDFOptions(density=300)
    assert pdf_options.density == 300

def test_pdf_options_initialize_fromdict():
    pdf_options = PDFOptions.fromdict({"density": 300})
    assert pdf_options.density == 300

def test_pdf_options_invalid_initialize_fromdict():
    error_msg = "PDFOptions can only accept 'density'"
    with pytest.raises(TypeError) as excinfo:
        PDFOptions.fromdict({"density": 300, "junk": "value"})
    assert error_msg in str(excinfo.value)

def test_pdf_options_setters():
    pdf_options = PDFOptions(density=300)
    pdf_options.density = 10
    assert pdf_options.density == 10

def test_pdf_options_density_validator():
    error_msg = "PDFOptions.density must be of type int"
    pdf_options = PDFOptions()
    with pytest.raises(ValueError) as excinfo:
        pdf_options.density = "junk"
    assert error_msg in str(excinfo.value)

def test_pdf_options_to_dict():
    pdf_options = PDFOptions().to_dict()
    assert pdf_options['density'] == 150

# Audio Options Tests
def test_audio_options_default_initializer():
    audio_options = AudioOptions()
    assert audio_options.bleep_end_padding == 0
    assert audio_options.bleep_start_padding == 0

def test_audio_options_initializer():
    audio_options = AudioOptions(bleep_start_padding=200, bleep_end_padding=300)
    assert audio_options.bleep_end_padding == 300
    assert audio_options.bleep_start_padding == 200

def test_audio_options_initialize_fromdict():
    audio_options = AudioOptions.fromdict({"bleep_start_padding":200, "bleep_end_padding":300})
    assert audio_options.bleep_end_padding == 300
    assert audio_options.bleep_start_padding == 200

def test_audio_options_invalid_initialize_fromdict():
    error_msg = "ProcessedText can only accept the values 'bleep_start_padding' and 'bleep_end_padding'" 
    with pytest.raises(TypeError) as excinfo:
        AudioOptions.fromdict({"bleep_start_padding":200, "bleep_end_padding":300, "junk": "value"})
    assert error_msg in str(excinfo.value)

def test_audio_options_setters():
    audio_options = AudioOptions()
    audio_options.bleep_end_padding = 1
    audio_options.bleep_start_padding = 2

    assert audio_options.bleep_end_padding == 1
    assert audio_options.bleep_start_padding == 2

def test_audio_options_bleep_start_padding_validator():
    error_msg = "AudioOptions.bleep_start_padding must be of type int" 
    with pytest.raises(ValueError) as excinfo:
        AudioOptions().bleep_start_padding = "junk"
    assert error_msg in str(excinfo.value)

def test_audio_options_bleep_end_padding_validator():
    error_msg = "AudioOptions.bleep_end_padding must be of type int" 
    with pytest.raises(ValueError) as excinfo:
        AudioOptions().bleep_end_padding = "junk"
    assert error_msg in str(excinfo.value)

def test_audio_options_to_dict():
    audio_options = AudioOptions().to_dict()
    assert audio_options["bleep_end_padding"] == 0
    assert audio_options["bleep_start_padding"] == 0

# Timestamp Tests
def test_timestamp_initializer():
    timestamp = Timestamp(start=2.0, end=3.0)
    assert timestamp.start == 2.0
    assert timestamp.end == 3.0

def test_timestamp_initialize_fromdict():
    timestamp = Timestamp.fromdict({"start":2.0, "end":3.0})
    assert timestamp.start == 2.0
    assert timestamp.end == 3.0    

def test_timestamp_invalid_initialize_fromdict():
    error_msg = "Timestamp can only accept the values 'start' and 'end'" 
    with pytest.raises(TypeError) as excinfo:
        Timestamp.fromdict({"start":2.0, "end":3.0, "junk": "value"})
    assert error_msg in str(excinfo.value)

def test_timestamp_setters():
    timestamp = Timestamp(start=2.0, end=3.0)
    timestamp.start = 0.0
    timestamp.end = 5.0
    assert timestamp.start == 0.0
    assert timestamp.end == 5.0

def test_timestamp_start_validator():
    error_msg = "Timestamp.start must be of type float" 
    with pytest.raises(ValueError) as excinfo:
        Timestamp.fromdict({"start":"test", "end":3.0})
    assert error_msg in str(excinfo.value)

def test_timestamp_end_validator():
    error_msg = "Timestamp.end must be of type float"
    with pytest.raises(ValueError) as excinfo:
        Timestamp.fromdict({"start":2.0, "end":"test"})
    assert error_msg in str(excinfo.value)

def test_timestamp_to_dict():
    timestamp = Timestamp(start=2.0, end=3.0).to_dict()
    assert timestamp['start'] == 2.0
    assert timestamp['end'] == 3.0

# Process Text Request Tests
def test_process_text_request_default_initializer():
    process_text_request = ProcessTextRequest(text = ['hey'])
    assert process_text_request.text == ['hey']
    assert process_text_request.link_batch == False
    assert type(process_text_request.entity_detection) == EntityDetection
    assert type(process_text_request.processed_text) == ProcessedText

def test_process_text_request_initializer():
    text = ['hey!']
    link_batch = True
    entity_type = EntityTypeSelector(type="ENABLE", value=['NAME'])
    filter = FilterSelector(type='ALLOW', pattern='hey')
    entity_detection = EntityDetection(accuracy='standard', entity_types=[entity_type], filter=[filter], return_entity=False)
    processed_text = ProcessedText(type='MARKER', pattern='BEST_ENTITY_TYPE')
    
    process_text_request = ProcessTextRequest(text=text, link_batch=link_batch, entity_detection=entity_detection, processed_text=processed_text)

    assert process_text_request.text == text
    assert process_text_request.link_batch == link_batch
    assert process_text_request.entity_detection.accuracy == entity_detection.accuracy
    assert process_text_request.entity_detection.entity_types[0].type == entity_type.type
    assert process_text_request.entity_detection.entity_types[0].value == entity_type.value
    assert process_text_request.entity_detection.filter[0].type == filter.type
    assert process_text_request.entity_detection.filter[0].pattern == filter.pattern
    assert process_text_request.processed_text.type == processed_text.type
    assert process_text_request.processed_text.pattern == processed_text.pattern

def test_process_text_request_initialize_fromdict():
    request_obj = {
        "text": ["hey!"],
        "link_batch": False,
        "entity_detection": {"accuracy":"standard",
                             "entity_types": [{"type": "DISABLE", "value":["LOCATION"]}],
                             "filter": [{"type": "BLOCK", "pattern": "Roger"}],
                             "return_entity": False
        },
        "processed_text": {
            "type": "MARKER",
            "pattern": "ALL_ENTITY_TYPES"
        }
    }
    process_text_request = ProcessTextRequest.fromdict(request_obj)
    assert process_text_request.text == request_obj["text"]
    assert process_text_request.link_batch == request_obj["link_batch"]
    assert process_text_request.entity_detection.accuracy == request_obj["entity_detection"]["accuracy"]
    assert process_text_request.entity_detection.entity_types[0].type == request_obj["entity_detection"]["entity_types"][0]["type"]
    assert process_text_request.entity_detection.entity_types[0].value == request_obj["entity_detection"]["entity_types"][0]["value"]
    assert process_text_request.entity_detection.filter[0].type == request_obj["entity_detection"]["filter"][0]["type"]
    assert process_text_request.entity_detection.filter[0].pattern == request_obj["entity_detection"]["filter"][0]["pattern"]
    assert process_text_request.processed_text.type == request_obj["processed_text"]["type"]
    assert process_text_request.processed_text.pattern == request_obj["processed_text"]["pattern"]

def test_process_text_request_invalid_initialize_fromdict():
    error_msg = "ProcessTextRequest can only accept the values 'text', 'link_batch', 'entity_detection' and 'process_text'"
    request_obj = {
        "text": ["hey!"],
        "link_batch": False,
        "entity_detection": {"accuracy":"standard",
                             "entity_types": [{"type": "DISABLE", "value":["LOCATION"]}],
                             "filter": [{"type": "BLOCK", "pattern": "Roger"}],
                             "return_entity": False
        },
        "processed_text": {
            "type": "MARKER",
            "pattern": "ALL_ENTITY_TYPES"
        },
        "junk": "value"
    }
    with pytest.raises(TypeError) as excinfo:
        ProcessTextRequest.fromdict(request_obj)
    assert error_msg in str(excinfo.value)

def test_process_text_request_to_dict():
    text = ['hey!']
    link_batch = True
    entity_type = EntityTypeSelector(type="ENABLE", value=['NAME'])
    filter = FilterSelector(type='ALLOW', pattern='hey')
    entity_detection = EntityDetection(accuracy='standard', entity_types=[entity_type], filter=[filter], return_entity=False)
    processed_text = ProcessedText(type='MARKER', pattern='BEST_ENTITY_TYPE')
    
    process_text_request = ProcessTextRequest(text=text, link_batch=link_batch, entity_detection=entity_detection, processed_text=processed_text).to_dict()
    print(process_text_request)
    assert process_text_request["text"] == text
    assert process_text_request["link_batch"] == link_batch
    assert process_text_request["entity_detection"]["accuracy"] == entity_detection.accuracy
    assert process_text_request["entity_detection"]["entity_types"][0]["type"] == entity_type.type
    assert process_text_request["entity_detection"]["entity_types"][0]["value"] == entity_type.value
    assert process_text_request["entity_detection"]["filter"][0]["type"] == filter.type
    assert process_text_request["entity_detection"]["filter"][0]["pattern"] == filter.pattern
    assert process_text_request["processed_text"]["type"] == processed_text.type
    assert process_text_request["processed_text"]["pattern"] == processed_text.pattern

# Process File URI Request Tests
def test_process_file_uri_request_default_initializer():
    process_file_uri_obj = ProcessFileUriRequest(uri="this/location/right/here.png")
    assert process_file_uri_obj.uri == "this/location/right/here.png"
    assert type(process_file_uri_obj.entity_detection) is EntityDetection
    assert type(process_file_uri_obj.pdf_options) is PDFOptions
    assert type(process_file_uri_obj.audio_options) is AudioOptions

def test_process_file_uri_request_initializer():
    entity_type = EntityTypeSelector(type="ENABLE", value=['NAME'])
    filter = FilterSelector(type='ALLOW', pattern='hey')
    entity_detection = EntityDetection(accuracy='standard', entity_types=[entity_type], filter=[filter], return_entity=False)
    pdf_options = PDFOptions(density=100)
    audio_options = AudioOptions(bleep_start_padding=1, bleep_end_padding=2)
    process_file_uri_obj = ProcessFileUriRequest(uri="this/location/right/here.png", entity_detection=entity_detection, pdf_options=pdf_options, audio_options=audio_options)
    assert process_file_uri_obj.uri == "this/location/right/here.png"
    assert process_file_uri_obj.entity_detection.accuracy == 'standard'
    assert process_file_uri_obj.pdf_options.density == 100
    assert process_file_uri_obj.audio_options.bleep_end_padding == 2

def test_process_file_uri_request_initialize_fromdict():
    entity_type = EntityTypeSelector(type="ENABLE", value=['NAME'])
    filter = FilterSelector(type='ALLOW', pattern='hey')
    entity_detection = EntityDetection(accuracy='standard', entity_types=[entity_type], filter=[filter], return_entity=False)
    pdf_options = PDFOptions(density=100)
    audio_options = AudioOptions(bleep_start_padding=1, bleep_end_padding=2)
    process_file_uri_obj = ProcessFileUriRequest.fromdict({"uri":"this/location/right/here.png", "entity_detection":entity_detection.to_dict(), "pdf_options":pdf_options.to_dict(), "audio_options":audio_options.to_dict()})
    assert process_file_uri_obj.uri == "this/location/right/here.png"
    assert process_file_uri_obj.entity_detection.accuracy == 'standard'
    assert process_file_uri_obj.pdf_options.density == 100
    assert process_file_uri_obj.audio_options.bleep_end_padding == 2

def test_process_file_uri_request_invalid_initialize_fromdict():
    error_msg = "ProcessFileUriRequest can only accept the values 'uri', 'entity_detection', 'pdf_options and 'audio_options'"
    entity_type = EntityTypeSelector(type="ENABLE", value=['NAME'])
    filter = FilterSelector(type='ALLOW', pattern='hey')
    entity_detection = EntityDetection(accuracy='standard', entity_types=[entity_type], filter=[filter], return_entity=False)
    pdf_options = PDFOptions(density=100)
    audio_options = AudioOptions(bleep_start_padding=1, bleep_end_padding=2)
    with pytest.raises(TypeError) as excinfo:
        ProcessFileUriRequest.fromdict({"uri":"this/location/right/here.png", "entity_detection":entity_detection.to_dict(), "pdf_options":pdf_options.to_dict(), "audio_options":audio_options.to_dict(), "junk": "value"})
    assert error_msg in str(excinfo.value)


def test_process_file_uri_request_to_dict():
    entity_type = EntityTypeSelector(type="ENABLE", value=['NAME'])
    filter = FilterSelector(type='ALLOW', pattern='hey')
    entity_detection = EntityDetection(accuracy='standard', entity_types=[entity_type], filter=[filter], return_entity=False)
    pdf_options = PDFOptions(density=100)
    audio_options = AudioOptions(bleep_start_padding=1, bleep_end_padding=2)
    process_file_uri_obj = ProcessFileUriRequest(uri="this/location/right/here.png", entity_detection=entity_detection, pdf_options=pdf_options, audio_options=audio_options).to_dict()
    assert process_file_uri_obj["uri"] == "this/location/right/here.png"
    assert process_file_uri_obj["entity_detection"]["accuracy"] == 'standard'
    assert process_file_uri_obj["pdf_options"]["density"] == 100
    assert process_file_uri_obj["audio_options"]["bleep_end_padding"] == 2

# Process File Base64 Request Tests
def test_process_file_base64_request_default_initializer():
    process_file_base64_request_obj = ProcessFileBase64Request(file="sfsfxe234jkjsdlkfnDATA!!!!!!")
    assert process_file_base64_request_obj.file == "sfsfxe234jkjsdlkfnDATA!!!!!!"
    assert type(process_file_base64_request_obj.entity_detection) is EntityDetection
    assert type(process_file_base64_request_obj.pdf_options) is PDFOptions
    assert type(process_file_base64_request_obj.audio_options) is AudioOptions

def test_process_file_base64_request_initializer():
    entity_type = EntityTypeSelector(type="ENABLE", value=['NAME'])
    filter = FilterSelector(type='ALLOW', pattern='hey')
    entity_detection = EntityDetection(accuracy='standard', entity_types=[entity_type], filter=[filter], return_entity=False)
    pdf_options = PDFOptions(density=100)
    audio_options = AudioOptions(bleep_start_padding=1, bleep_end_padding=2)
    process_file_base64_request_obj = ProcessFileBase64Request(file="sfsfxe234jkjsdlkfnDATA", entity_detection=entity_detection, pdf_options=pdf_options, audio_options=audio_options)
    assert process_file_base64_request_obj.file == "sfsfxe234jkjsdlkfnDATA"
    assert process_file_base64_request_obj.entity_detection.accuracy == 'standard'
    assert process_file_base64_request_obj.pdf_options.density == 100
    assert process_file_base64_request_obj.audio_options.bleep_end_padding == 2

def test_process_file_base64_request_initialize_fromdict():
    file = File(data="sfsfxe234jkjsdlkfnDATA", content_type="application/pdf")
    entity_type = EntityTypeSelector(type="ENABLE", value=['NAME'])
    filter = FilterSelector(type='ALLOW', pattern='hey')
    entity_detection = EntityDetection(accuracy='standard', entity_types=[entity_type], filter=[filter], return_entity=False)
    pdf_options = PDFOptions(density=100)
    audio_options = AudioOptions(bleep_start_padding=1, bleep_end_padding=2)
    process_file_base64_request_obj = ProcessFileBase64Request.fromdict({"file":file.to_dict(), "entity_detection":entity_detection.to_dict(), "pdf_options":pdf_options.to_dict(), "audio_options":audio_options.to_dict()})
    assert process_file_base64_request_obj.file.data == "sfsfxe234jkjsdlkfnDATA"
    assert process_file_base64_request_obj.entity_detection.accuracy == 'standard'
    assert process_file_base64_request_obj.pdf_options.density == 100
    assert process_file_base64_request_obj.audio_options.bleep_end_padding == 2

def test_process_file_base64_request_invalid_initialize_fromdict():
    error_msg = "ProcessFileBase64Request can only accept the values 'file', 'entity_detection', 'pdf_options and 'audio_options'"
    file = File(data="sfsfxe234jkjsdlkfnDATA", content_type="application/pdf")
    entity_type = EntityTypeSelector(type="ENABLE", value=['NAME'])
    filter = FilterSelector(type='ALLOW', pattern='hey')
    entity_detection = EntityDetection(accuracy='standard', entity_types=[entity_type], filter=[filter], return_entity=False)
    pdf_options = PDFOptions(density=100)
    audio_options = AudioOptions(bleep_start_padding=1, bleep_end_padding=2)
    with pytest.raises(TypeError) as excinfo:
        ProcessFileBase64Request.fromdict({"file":file.to_dict(), "entity_detection":entity_detection.to_dict(), "pdf_options":pdf_options.to_dict(), "audio_options":audio_options.to_dict(), "junk":"value"})    
    assert error_msg in str(excinfo.value)


def test_process_file_base64_request_to_dict():
    entity_type = EntityTypeSelector(type="ENABLE", value=['NAME'])
    filter = FilterSelector(type='ALLOW', pattern='hey')
    entity_detection = EntityDetection(accuracy='standard', entity_types=[entity_type], filter=[filter], return_entity=False)
    pdf_options = PDFOptions(density=100)
    audio_options = AudioOptions(bleep_start_padding=1, bleep_end_padding=2)
    process_file_base64_request_obj = ProcessFileBase64Request(file="sfsfxe234jkjsdlkfnDATA", entity_detection=entity_detection, pdf_options=pdf_options, audio_options=audio_options).to_dict()
    assert process_file_base64_request_obj["file"] == "sfsfxe234jkjsdlkfnDATA"
    assert process_file_base64_request_obj["entity_detection"]["accuracy"] == 'standard'
    assert process_file_base64_request_obj["pdf_options"]["density"] == 100
    assert process_file_base64_request_obj["audio_options"]["bleep_end_padding"] == 2

# Bleep Request Tests
def test_bleep_request_initializer():
    file=File(data="test", content_type="image/jpg")
    timestamps=[Timestamp(start=0.0, end=1.0)]
    bleep_request = BleepRequest(file=file, timestamps=timestamps)
    assert bleep_request.file.data == 'test'
    assert bleep_request.timestamps[0].start == 0

def test_bleep_request_initialize_fromdict():
    file=File(data="test", content_type="image/jpg")
    timestamps=[Timestamp(start=0.0, end=1.0)]
    bleep_request = BleepRequest.fromdict({"file":file.to_dict(), "timestamps":[row.to_dict() for row in timestamps]})
    assert bleep_request.file.data == 'test'
    assert bleep_request.timestamps[0].start == 0

def test_bleep_request_invalid_initialize_fromdict():
    error_msg = "BleepRequest can only accept the values 'file'and 'timestamps'"
    file=File(data="test", content_type="image/jpg")
    timestamps=[Timestamp(start=0.0, end=1.0)]
    with pytest.raises(TypeError) as excinfo:
        BleepRequest.fromdict({"file":file.to_dict(), "timestamps":[row.to_dict() for row in timestamps], "junk": "value"})
    assert error_msg in str(excinfo.value)

def test_bleep_request_to_dict():
    file=File(data="test", content_type="image/jpg")
    timestamps=[Timestamp(start=0.0, end=1.0)]
    bleep_request = BleepRequest(file=file, timestamps=timestamps).to_dict()
    assert bleep_request["file"]["data"] == 'test'
    assert bleep_request["timestamps"][0]["start"] == 0
    
