import pytest
from components import *

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
    test_type = "ALLOW"
    test_pattern = "[A-Z]"
    test_dict = {"type": test_type, "pattern": test_pattern, "fake_key": "fake_value"}
    with pytest.raises(TypeError) as excinfo:
        FilterSelector.fromdict(test_dict)
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
    with pytest.raises(ValueError) as excinfo:
        FilterSelector(type=test_type, pattern=test_pattern)
    assert " is not valid. FilterSelector.pattern can only be a string" in str(excinfo.value)

def test_filter_to_dict():
    pass


def test_entity_type_selector():
    test_type = "DISABLE"

    entity_type_selector = EntityTypeSelector(type=test_type)
    assert entity_type_selector.type == test_type
    assert entity_type_selector.value == []

def test_entity_detection():
    entity_detection = EntityDetection()
    assert entity_detection.accuracy == "high"
    assert entity_detection.entity_types == []
    assert entity_detection.filter == []
    assert entity_detection.return_entity == True

def test_process_text():
    process_text = ProcessedText()
    assert process_text.type == "MARKER"
    assert process_text.pattern == "[UNIQUE_NUMBERED_ENTITY_TYPE]"

def test_process_text_request_defaults():
    process_text_request = ProcessTextRequest(text = ['hey'])
    assert process_text_request.text == ['hey']
    assert process_text_request.link_batch == False
    assert type(process_text_request.entity_detection) == EntityDetection
    assert type(process_text_request.processed_text) == ProcessedText

def test_process_text_request_full():
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

def test_process_text_request_full_from_dict():
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

