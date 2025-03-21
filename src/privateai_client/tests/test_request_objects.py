import pytest

from ..components import *


# File Tests
def test_file_initializer():
    file = File(data="test", content_type="application/pdf")
    assert file.data == "test"
    assert file.content_type == "application/pdf"


def test_file_initializer_fromdict():
    file = File.fromdict({"data": "test", "content_type": "application/pdf"})
    assert file.data == "test"
    assert file.content_type == "application/pdf"


def test_file_invalid_initialize_fromdict():
    error_msg = "File can only accept the values 'data' and 'content_type'"
    with pytest.raises(TypeError) as excinfo:
        File.fromdict(
            {"data": "test", "content_type": "application/pdf", "garbage": "value"}
        )
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


def test_filter_selector_initializer2():
    test_type = "BLOCK"
    test_pattern = "[A-Z]"
    test_entity_type = "CHARACTER"
    filter_selector = FilterSelector(
        type=test_type, pattern=test_pattern, entity_type=test_entity_type
    )
    assert filter_selector.type == test_type
    assert filter_selector.pattern == test_pattern
    assert filter_selector.entity_type == "CHARACTER"
    assert filter_selector.threshold == 1


def test_filter_selector_initializer():
    test_type = "ALLOW_TEXT"
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
        FilterSelector.fromdict(
            {"type": "ALLOW", "pattern": "[A-Z]", "fake_key": "fake_value"}
        )
    assert "FilterSelector can only accept the values 'type' and 'pattern'" in str(
        excinfo.value
    )


def test_filter_selector_setters():
    test_type = "ALLOW"
    test_pattern = "[A-Z]"
    filter_selector = FilterSelector(type=test_type, pattern=test_pattern)
    filter_selector.type = "BLOCK"
    filter_selector.pattern = "*1"
    filter_selector.entity_type = "TEST"
    filter_selector.threshold = 0.5

    assert filter_selector.type == "BLOCK"
    assert filter_selector.pattern == "*1"
    assert filter_selector.entity_type == "TEST"
    assert filter_selector.threshold == 0.5


def test_filter_selector_type_validator():
    test_type = "JUNK"
    test_pattern = "[A-Z]"
    with pytest.raises(ValueError) as excinfo:
        FilterSelector(type=test_type, pattern=test_pattern)
    assert (
        " is not valid. FilterSelector.type can only be one of the following: "
        in str(excinfo.value)
    )


def test_filter_selector_pattern_validator():
    test_type = "ALLOW"
    test_pattern = 12
    with pytest.raises(TypeError) as excinfo:
        FilterSelector(type=test_type, pattern=test_pattern)
    assert "FilterSelector.pattern must be of type string" in str(excinfo.value)


def test_filter_selector_entity_type_validator():
    test_type = "BLOCK"
    test_pattern = "[A-Z]"
    test_entity_type = 30
    with pytest.raises(TypeError) as excinfo:
        FilterSelector(
            type=test_type, pattern=test_pattern, entity_type=test_entity_type
        )
    assert "FilterSelector.entity_type must be of type string" in str(excinfo.value)


def test_filter_selector_entity_type_validator():
    test_type = "BLOCK"
    test_pattern = "[A-Z]"
    test_entity_type = "TEST"
    test_threshold = -1
    with pytest.raises(TypeError) as excinfo:
        FilterSelector(
            type=test_type,
            pattern=test_pattern,
            entity_type=test_entity_type,
            threshold=test_threshold,
        )
    assert "FilterSelector.threshold must be greater than 0" in str(excinfo.value)


def test_filter_to_dict():
    test_type = "ALLOW"
    test_pattern = "[A-Z]"
    filter_selector = FilterSelector(type=test_type, pattern=test_pattern)
    filter_dict = filter_selector.to_dict()
    assert filter_dict["type"] == test_type
    assert filter_dict["pattern"] == test_pattern


# Entity Tests
def test_entity_initializer():
    entity = Entity(processed_text="NAME_1", text="this is a test")
    assert entity.processed_text == "NAME_1"
    assert entity.text == "this is a test"


def test_entity_initializer_fromdict():
    entity = Entity.fromdict({"processed_text": "NAME_1", "text": "this is a test"})
    assert entity.processed_text == "NAME_1"
    assert entity.text == "this is a test"


def test_entity_invalid_initialize_fromdict():
    error_msg = "Entity can only accept the values 'processed_text' and 'text'"
    with pytest.raises(TypeError) as excinfo:
        Entity.fromdict(
            {"processed_text": "NAME_1", "text": "this is a test", "garbage": "value"}
        )
    assert error_msg in str(excinfo.value)


def test_entity_processed_text_validator():
    error_msg = "Entity.processed_text must be of type string"
    with pytest.raises(TypeError) as excinfo:
        Entity(processed_text=12, text="ayy")
    assert error_msg in str(excinfo.value)


def test_entity_text_validator():
    error_msg = "Entity.text must be of type string"
    with pytest.raises(TypeError) as excinfo:
        entity = Entity(processed_text="ORGANIZATION_60", text=45.2)
    assert error_msg in str(excinfo.value)


def test_entity_setters():
    entity = Entity(processed_text="NAME_1", text="Jerry Stevens")
    entity.processed_text = "CONDITION_20"
    entity.text = "Broken leg"
    assert entity.processed_text == "CONDITION_20"
    assert entity.text == "Broken leg"


# Entity Type Selector Tests
def test_entity_type_selector_initializer():
    test_type = "DISABLE"

    entity_type_selector = EntityTypeSelector(type=test_type)
    assert entity_type_selector.type == test_type
    assert entity_type_selector.value == []


def test_entity_type_selector_initialize_fromdict():
    entity_type_obj = EntityTypeSelector.fromdict({"type": "ENABLE", "value": ["NAME"]})
    assert entity_type_obj.type == "ENABLE"
    assert entity_type_obj.value == ["NAME"]


def test_entity_type_selector_invalid_initialize_fromdict():
    error_msg = "EntityTypeSelector can only accept the values 'type' and 'value'"
    with pytest.raises(TypeError) as excinfo:
        EntityTypeSelector.fromdict(
            {"type": "ENABLE", "value": ["NAME"], "garbage": "value"}
        )
    assert error_msg in str(excinfo.value)


def test_entity_type_selector_setters():
    entity_type_obj = EntityTypeSelector(type="ENABLE", value=["LOCATION"])
    entity_type_obj.type = "DISABLE"
    assert entity_type_obj.type == "DISABLE"


def test_entity_type_selector_type_validator():
    error_msg = "'JUNK' is not valid. EntityTypeSelector.type can only be one of the following: "
    entity_type_obj = EntityTypeSelector(type="ENABLE", value=["LOCATION"])
    with pytest.raises(ValueError) as excinfo:
        entity_type_obj.type = "JUNK"
    assert error_msg in str(excinfo.value)


def test_entity_type_selector_value_validator():
    error_msg = "EntityTypeSelector.value must be of type list"
    with pytest.raises(TypeError) as excinfo:
        EntityTypeSelector(type="ENABLE", value={})
    assert error_msg in str(excinfo.value)


def test_entity_type_selector_to_dict():
    entity_type_obj = EntityTypeSelector.fromdict(
        {"type": "ENABLE", "value": ["NAME"]}
    ).to_dict()
    assert entity_type_obj["type"] == "ENABLE"
    assert entity_type_obj["value"] == ["NAME"]


# Entity Detection Tests
def test_entity_detection_default_initializer():
    entity_detection = EntityDetection()
    assert entity_detection.accuracy == "high_automatic"
    assert entity_detection.entity_types == []
    assert entity_detection.filter == []
    assert entity_detection.return_entity == True


def test_entity_detection_initializer():
    entity_detection_obj = EntityDetection(
        accuracy="high",
        entity_types=[EntityTypeSelector(type="ENABLE")],
        filter=[FilterSelector(type="ALLOW", pattern="hey")],
        return_entity=False,
    )
    assert entity_detection_obj.accuracy == "high"
    assert type(entity_detection_obj.entity_types[0]) is EntityTypeSelector
    assert type(entity_detection_obj.filter[0]) is FilterSelector
    assert entity_detection_obj.return_entity is False


def test_entity_detection_initialize_fromdict():
    entity_detection = EntityDetection.fromdict(
        {
            "accuracy": "high",
            "entity_types": [EntityTypeSelector(type="ENABLE").to_dict()],
            "filter": [FilterSelector(type="ALLOW", pattern="hey").to_dict()],
            "return_entity": False,
        }
    )
    assert entity_detection.accuracy == "high"
    assert type(entity_detection.entity_types[0]) is EntityTypeSelector
    assert type(entity_detection.filter[0]) is FilterSelector
    assert entity_detection.return_entity is False


def test_entity_detection_invalid_initialize_fromdict():
    error_msg = "EntityDetection can only accept the values 'accuracy', 'entity_types', 'filter' and 'return_entity'"
    with pytest.raises(TypeError) as excinfo:
        EntityDetection.fromdict(
            {
                "accuracy": "high",
                "entity_types": [EntityTypeSelector(type="ENABLE").to_dict()],
                "filter": [FilterSelector(type="ALLOW", pattern="hey").to_dict()],
                "return_entity": False,
                "garbage": "value",
            }
        )
    assert error_msg in str(excinfo.value)


def test_entity_detection_setters():
    entity_detection_obj = EntityDetection.fromdict(
        {
            "accuracy": "high",
            "entity_types": [EntityTypeSelector(type="ENABLE").to_dict()],
            "filter": [FilterSelector(type="ALLOW", pattern="hey").to_dict()],
            "return_entity": False,
        }
    )
    entity_detection_obj.accuracy = "standard"
    entity_detection_obj.return_entity = True
    assert entity_detection_obj.accuracy == "standard"
    assert entity_detection_obj.return_entity == True


def test_entity_detection_accuracy_validator():
    error_msg = (
        "junk is not valid. EntityDetection.accuracy can only be one of the following: "
    )
    entity_detection_obj = EntityDetection.fromdict(
        {
            "accuracy": "high",
            "entity_types": [EntityTypeSelector(type="ENABLE").to_dict()],
            "filter": [FilterSelector(type="ALLOW", pattern="hey").to_dict()],
            "return_entity": False,
        }
    )
    with pytest.raises(ValueError) as excinfo:
        entity_detection_obj.accuracy = "junk"
    assert error_msg in str(excinfo.value)


def test_entity_detection_entity_types_validator():
    error_msg = (
        "EntityDetection.entity_types can only contain EntityTypeSelector objects"
    )
    with pytest.raises(ValueError) as excinfo:
        EntityDetection(
            accuracy="high",
            entity_types=["junk"],
            filter=[FilterSelector(type="ALLOW", pattern="hey")],
            return_entity=False,
        )
    assert error_msg in str(excinfo.value)


def test_entity_detection_entity_types_validator():
    error_msg = "EntityDetection.filter can only contain FilterSelector objects"
    with pytest.raises(ValueError) as excinfo:
        EntityDetection(
            accuracy="high",
            entity_types=[EntityTypeSelector(type="ENABLE")],
            filter=["junk"],
            return_entity=False,
        )
    assert error_msg in str(excinfo.value)


def test_entity_detection_return_entity_validator():
    error_msg = "EntityDetection.return_entity must be of type bool"
    entity_detection_obj = EntityDetection.fromdict(
        {
            "accuracy": "high",
            "entity_types": [EntityTypeSelector(type="ENABLE").to_dict()],
            "filter": [FilterSelector(type="ALLOW", pattern="hey").to_dict()],
            "return_entity": False,
        }
    )
    with pytest.raises(ValueError) as excinfo:
        entity_detection_obj.return_entity = "junk"
    assert error_msg in str(excinfo.value)


def test_entity_detection_to_dict():
    entity_detection_obj = EntityDetection(
        accuracy="high",
        entity_types=[EntityTypeSelector(type="ENABLE")],
        filter=[FilterSelector(type="ALLOW", pattern="hey")],
        return_entity=False,
    ).to_dict()
    assert entity_detection_obj["accuracy"] == "high"
    assert type(entity_detection_obj["entity_types"][0]) is dict
    assert type(entity_detection_obj["filter"][0]) is dict
    assert entity_detection_obj["return_entity"] is False


# Object Entity Type Selector Tests
def test_object_entity_type_selector_initializer():
    test_type = "DISABLE"

    object_entity_type_selector = ObjectEntityTypeSelector(type=test_type)
    assert object_entity_type_selector.type == test_type
    assert object_entity_type_selector.value == []


def test_object_entity_type_selector_initialize_fromdict():
    entity_type_obj = ObjectEntityTypeSelector.fromdict(
        {"type": "ENABLE", "value": ["LOGO"]}
    )
    assert entity_type_obj.type == "ENABLE"
    assert entity_type_obj.value == ["LOGO"]


def test_object_entity_type_selector_invalid_initialize_fromdict():
    error_msg = "ObjectEntityTypeSelector can only accept the values 'type' and 'value'"
    with pytest.raises(TypeError) as excinfo:
        ObjectEntityTypeSelector.fromdict(
            {"type": "ENABLE", "value": ["LOGO"], "garbage": "value"}
        )
    assert error_msg in str(excinfo.value)


def test_object_entity_type_selector_setters():
    entity_type_obj = ObjectEntityTypeSelector(type="ENABLE", value=["FACE"])
    entity_type_obj.type = "DISABLE"
    assert entity_type_obj.type == "DISABLE"


def test_object_entity_type_selector_type_validator():
    error_msg = "'RANDOM' is not valid. ObjectEntityTypeSelector.type can only be one of the following: "
    entity_type_obj = ObjectEntityTypeSelector(type="ENABLE", value=["FACE"])
    with pytest.raises(ValueError) as excinfo:
        entity_type_obj.type = "RANDOM"
    assert error_msg in str(excinfo.value)


def test_object_entity_type_selector_value_validator():
    error_msg = "ObjectEntityTypeSelector.value must be of type list"
    with pytest.raises(TypeError) as excinfo:
        ObjectEntityTypeSelector(type="ENABLE", value={})
    assert error_msg in str(excinfo.value)


def test_object_entity_type_selector_invalid_value_validator():
    error_msg = "ObjectEntityTypeSelector.value can only be one of the following:"
    with pytest.raises(ValueError) as excinfo:
        ObjectEntityTypeSelector(type="ENABLE", value=["RANDOM"])
    assert error_msg in str(excinfo.value)


def test_object_entity_type_selector_to_dict():
    entity_type_obj = ObjectEntityTypeSelector.fromdict(
        {"type": "ENABLE", "value": ["SIGNATURE"]}
    ).to_dict()
    assert entity_type_obj["type"] == "ENABLE"
    assert entity_type_obj["value"] == ["SIGNATURE"]


# Object Entity Detection Tests
def test_object_entity_detection_default_initializer():
    object_entity_detection = ObjectEntityDetection()
    assert object_entity_detection.object_entity_types == []


def test_object_entity_detection_initializer():
    object_entity_detection_obj = ObjectEntityDetection(
        object_entity_types=[ObjectEntityTypeSelector(type="ENABLE")],
    )
    assert (
        type(object_entity_detection_obj.object_entity_types[0])
        is ObjectEntityTypeSelector
    )


def test_object_entity_detection_initialize_fromdict():
    object_entity_detection = ObjectEntityDetection.fromdict(
        {
            "object_entity_types": [ObjectEntityTypeSelector(type="ENABLE").to_dict()],
        }
    )
    assert (
        type(object_entity_detection.object_entity_types[0]) is ObjectEntityTypeSelector
    )


def test_object_entity_detection_invalid_initialize_fromdict():
    error_msg = "ObjectEntityDetection can only accept the value 'object_entity_types'"
    with pytest.raises(TypeError) as excinfo:
        ObjectEntityDetection.fromdict(
            {
                "object_entity_types": [
                    ObjectEntityTypeSelector(type="ENABLE").to_dict()
                ],
                "random": "value",
            }
        )
    assert error_msg in str(excinfo.value)


def test_object_entity_detection_object_entity_types_validator():
    error_msg = "ObjectEntityDetection.object_entity_types can only contain ObjectEntityTypeSelector objects"
    with pytest.raises(ValueError) as excinfo:
        ObjectEntityDetection(
            object_entity_types=["junk"],
        )
    assert error_msg in str(excinfo.value)


def test_object_entity_detection_to_dict():
    object_entity_detection_obj = ObjectEntityDetection(
        object_entity_types=[ObjectEntityTypeSelector(type="ENABLE")],
    ).to_dict()
    assert type(object_entity_detection_obj["object_entity_types"][0]) is dict


# Processed Text Tests
def test_processed_text_default_initializer():
    processed_text = ProcessedText()
    assert processed_text.type == "MARKER"
    assert processed_text.pattern == "[UNIQUE_NUMBERED_ENTITY_TYPE]"
    assert processed_text.coreference_resolution == "heuristics"


def test_processed_text_mask_initializer():
    processed_text = ProcessedText(type="MASK", mask_character="*")
    assert processed_text.type == "MASK"
    assert processed_text.mask_character == "*"


def test_processed_text_coreference_initializer():
    processed_text = ProcessedText(
        type="MARKER", coreference_resolution="model_prediction"
    )
    assert processed_text.type == "MARKER"
    assert processed_text.coreference_resolution == "model_prediction"


def test_processed_text_initialize_fromdict():
    processed_text = ProcessedText.fromdict(
        {
            "type": "MARKER",
            "pattern": "[UNIQUE_NUMBERED_ENTITY_TYPE]",
            "marker_language": "fr",
            "coreference_resolution": "combined",
        }
    )
    assert processed_text.type == "MARKER"
    assert processed_text.pattern == "[UNIQUE_NUMBERED_ENTITY_TYPE]"
    assert processed_text.coreference_resolution == "combined"


def test_processed_text_invalid_initialize_fromdict():
    error_msg = "ProcessedText can only accept the values 'type' and 'pattern'"
    with pytest.raises(TypeError) as excinfo:
        ProcessedText.fromdict(
            {
                "type": "MARKER",
                "pattern": "[UNIQUE_NUMBERED_ENTITY_TYPE]",
                "marker_language": "en",
                "coreference_resolution": "heuristics",
                "junk": "value",
            }
        )
    assert error_msg in str(excinfo.value)


def test_processed_text_mask_setters():
    processed_text = ProcessedText()
    processed_text.type = "MASK"
    processed_text.pattern = "*ALL_ENTITY_TYPES*"
    processed_text.marker_language = "de"
    assert processed_text.type == "MASK"
    assert processed_text.pattern == "*ALL_ENTITY_TYPES*"
    assert processed_text.marker_language == "de"


def test_processed_text_coreference_setters():
    processed_text = ProcessedText()
    processed_text.type = "MARKER"
    processed_text.pattern = "[UNIQUE_NUMBERED_ENTITY_TYPE]"
    processed_text.marker_language = "fr"
    processed_text.coreference_resolution = "model_prediction"
    assert processed_text.type == "MARKER"
    assert processed_text.pattern == "[UNIQUE_NUMBERED_ENTITY_TYPE]"
    assert processed_text.marker_language == "fr"
    assert processed_text.coreference_resolution == "model_prediction"


def test_processed_text_type_validator():
    error_msg = (
        "junk is not valid. ProcessedText.type can only be one of the following: "
    )
    with pytest.raises(ValueError) as excinfo:
        ProcessedText.fromdict(
            {"type": "junk", "pattern": "[UNIQUE_NUMBERED_ENTITY_TYPE]"}
        )
    assert error_msg in str(excinfo.value)


def test_processed_text_pattern_validator():
    error_msg = (
        "junk is not valid. ProcessedText.pattern can only be one of the following: "
    )
    with pytest.raises(ValueError) as excinfo:
        ProcessedText.fromdict({"type": "MARKER", "pattern": "junk"})
    assert error_msg in str(excinfo.value)


def test_processed_text_marker_language_validator():
    error_msg = "junk is not valid. ProcessedText.marker_language can only be one of the following: "
    with pytest.raises(ValueError) as excinfo:
        ProcessedText.fromdict({"type": "MARKER", "marker_language": "junk"})
    assert error_msg in str(excinfo.value)


def test_processed_text_coreference_validator():
    error_msg = "junk is not valid. ProcessedText.coreference_resolution can only be one of the following: "
    with pytest.raises(ValueError) as excinfo:
        ProcessedText.fromdict({"type": "MARKER", "coreference_resolution": "junk"})
    assert error_msg in str(excinfo.value)


def test_processed_text_mask_to_dict():
    processed_text = ProcessedText(type="MASK", mask_character="*").to_dict()
    assert processed_text["type"] == "MASK"
    assert processed_text["mask_character"] == "*"


def test_processed_text_marker_to_dict():
    processed_text = ProcessedText(
        type="MARKER", coreference_resolution="combined"
    ).to_dict()
    assert processed_text["type"] == "MARKER"
    assert processed_text["coreference_resolution"] == "combined"


# PDF Options Tests
def test_pdf_options_default_initializer():
    pdf_options = PDFOptions()
    assert pdf_options.density == 200
    assert pdf_options.max_resolution == 3000
    assert pdf_options.enable_pdf_text_layer is True


def test_pdf_options_initializer():
    pdf_options = PDFOptions(
        density=300, max_resolution=500, enable_pdf_text_layer=False
    )
    assert pdf_options.density == 300
    assert pdf_options.max_resolution == 500
    assert pdf_options.enable_pdf_text_layer is False


def test_pdf_options_initialize_fromdict():
    pdf_options = PDFOptions.fromdict(
        {"density": 300, "max_resolution": 500, "enable_pdf_text_layer": True}
    )
    assert pdf_options.density == 300
    assert pdf_options.max_resolution == 500
    assert pdf_options.enable_pdf_text_layer is True


def test_pdf_options_invalid_initialize_fromdict():
    error_msg = "PDFOptions can only accept 'density', 'max_resolution' and 'enable_pdf_text_layer'"
    with pytest.raises(TypeError) as excinfo:
        PDFOptions.fromdict({"density": 300, "max_resolution": 500, "junk": "value"})
    assert error_msg in str(excinfo.value)


def test_pdf_options_setters():
    pdf_options = PDFOptions(density=300)
    pdf_options.density = 10
    assert pdf_options.density == 10
    pdf_options.max_resolution = 10
    assert pdf_options.max_resolution == 10
    pdf_options.enable_pdf_text_layer = False
    assert pdf_options.enable_pdf_text_layer is False


def test_pdf_options_density_validator():
    error_msg = "PDFOptions.density must be of type int and >0"
    pdf_options = PDFOptions()
    with pytest.raises(ValueError) as excinfo:
        pdf_options.density = "junk"
    assert error_msg in str(excinfo.value)


def test_pdf_options_max_resolution_validator():
    error_msg = "PDFOptions.max_resolution must be of type int and >0"
    pdf_options = PDFOptions()
    with pytest.raises(ValueError) as excinfo:
        pdf_options.max_resolution = "junk"
    assert error_msg in str(excinfo.value)


def test_pdf_options_enable_pdf_text_layer_validator():
    error_msg = "PDFOptions.enable_pdf_text_layer must be of type bool"
    pdf_options = PDFOptions()
    with pytest.raises(ValueError) as excinfo:
        pdf_options.enable_pdf_text_layer = "junk"
    assert error_msg in str(excinfo.value)


def test_pdf_options_to_dict():
    pdf_options = PDFOptions().to_dict()
    assert pdf_options["density"] == 200
    assert pdf_options["max_resolution"] == 3000
    assert pdf_options["enable_pdf_text_layer"] is True


# Audio Options Tests
def test_audio_options_default_initializer():
    audio_options = AudioOptions()
    assert audio_options.bleep_end_padding == 0.5
    assert audio_options.bleep_start_padding == 0.5
    assert audio_options.bleep_frequency == None
    assert audio_options.bleep_gain == None


def test_audio_options_initializer():
    audio_options = AudioOptions(
        bleep_start_padding=200.0,
        bleep_end_padding=300.0,
        bleep_gain=-2,
        bleep_frequency=250,
    )
    assert audio_options.bleep_start_padding == 200.0
    assert audio_options.bleep_end_padding == 300.0
    assert audio_options.bleep_gain == -2
    assert audio_options.bleep_frequency == 250


def test_audio_options_initializer_without_bleep_gain_and_bleep_frequency():
    audio_options = AudioOptions(bleep_start_padding=200.0, bleep_end_padding=300.0)
    assert audio_options.bleep_start_padding == 200.0
    assert audio_options.bleep_end_padding == 300.0
    assert audio_options.bleep_gain == None
    assert audio_options.bleep_frequency == None


def test_audio_options_initialize_fromdict():
    audio_options = AudioOptions.fromdict(
        {
            "bleep_start_padding": 0.3,
            "bleep_end_padding": 0.7,
            "bleep_gain": -2,
            "bleep_frequency": 250,
        }
    )
    assert audio_options.bleep_start_padding == 0.3
    assert audio_options.bleep_end_padding == 0.7
    assert audio_options.bleep_gain == -2
    assert audio_options.bleep_frequency == 250


def test_audio_options_invalid_initialize_fromdict():
    error_msg = "ProcessedText can only accept the values 'bleep_start_padding', 'bleep_end_padding', 'bleep_frequency', and 'bleep_gain'"
    with pytest.raises(TypeError) as excinfo:
        AudioOptions.fromdict(
            {
                "bleep_start_padding": 0.2,
                "bleep_end_padding": 0.1,
                "bleep_frequency": 10,
                "bleep_gain": 0,
                "junk": "value",
            }
        )
    assert error_msg in str(excinfo.value)


def test_audio_options_setters():
    audio_options = AudioOptions()
    audio_options.bleep_end_padding = 1.0
    audio_options.bleep_start_padding = 2.0
    audio_options.bleep_frequency = 100
    audio_options.bleep_gain = -50

    assert audio_options.bleep_end_padding == 1.0
    assert audio_options.bleep_start_padding == 2.0
    assert audio_options.bleep_frequency == 100
    assert audio_options.bleep_gain == -50


def test_audio_options_bleep_start_padding_validator():
    error_msg = "AudioOptions.bleep_start_padding must be of type float"
    with pytest.raises(ValueError) as excinfo:
        AudioOptions().bleep_start_padding = "junk"
    assert error_msg in str(excinfo.value)


def test_audio_options_bleep_end_padding_validator():
    error_msg = "AudioOptions.bleep_end_padding must be of type float"
    with pytest.raises(ValueError) as excinfo:
        AudioOptions().bleep_end_padding = "junk"
    assert error_msg in str(excinfo.value)


def test_audio_options_bleep_gain_validator():
    error_msg = "AudioOptions.bleep_gain must be of type int"
    with pytest.raises(ValueError) as excinfo:
        AudioOptions().bleep_gain = "junk"
    assert error_msg in str(excinfo.value)


def test_audio_options_bleep_frequency_validator():
    error_msg = "AudioOptions.bleep_frequency must be of type int"
    with pytest.raises(ValueError) as excinfo:
        AudioOptions().bleep_frequency = "junk"
    assert error_msg in str(excinfo.value)


def test_audio_options_to_dict():
    audio_options = AudioOptions().to_dict()
    assert audio_options["bleep_end_padding"] == 0.5
    assert audio_options["bleep_start_padding"] == 0.5

    with pytest.raises(KeyError):
        assert audio_options["bleep_gain"] == -3
    with pytest.raises(KeyError):
        assert audio_options["bleep_frequency"] == 600


# Image Options Tests
def test_image_options_default_initializer():
    image_options = ImageOptions()
    assert image_options.masking_method == "blur"
    assert image_options.palette == False


def test_image_options_initializer():
    image_options = ImageOptions(masking_method="blackbox", palette=True)
    assert image_options.masking_method == "blackbox"
    assert image_options.palette == True


def test_image_options_initializer_without_palette():
    image_options = ImageOptions(masking_method="blur")
    assert image_options.masking_method == "blur"
    assert image_options.palette == False


def test_image_options_initialize_fromdict():
    image_options = ImageOptions.fromdict({"masking_method": "blur", "palette": True})
    assert image_options.masking_method == "blur"
    assert image_options.palette == True


def test_image_options_invalid_initialize_fromdict():
    error_msg = "ImageOptions can only accept the values 'masking_method' and 'palette'"
    with pytest.raises(TypeError) as excinfo:
        ImageOptions.fromdict(
            {
                "masking_method": "blur",
                "palette": True,
                "junk": "value",
            }
        )
    assert error_msg in str(excinfo.value)


def test_image_options_setters():
    image_options = ImageOptions()
    image_options.masking_method = "blur"
    image_options.palette = True

    assert image_options.masking_method == "blur"
    assert image_options.palette == True


def test_image_options_masking_method_validator():
    error_msg = (
        "ImageOptions.masking_method must be one of ['blur', 'blackbox'], but got junk"
    )
    with pytest.raises(ValueError) as excinfo:
        ImageOptions().masking_method = "junk"
    assert error_msg in str(excinfo.value)


def test_image_options_palette_validator():
    error_msg = "ImageOptions.palette must be of type bool, but got <class 'str'>"
    with pytest.raises(ValueError) as excinfo:
        ImageOptions().palette = "junk"
    assert error_msg in str(excinfo.value)


# OCR Options Tests
def test_ocr_options_default_initializer():
    ocr_options = OCROptions()
    assert ocr_options.ocr_system == "paddleocr"


def test_ocr_options_initializer():
    ocr_options = OCROptions(ocr_system="azure_doc_intelligence")
    assert ocr_options.ocr_system == "azure_doc_intelligence"


def test_ocr_options_initialize_fromdict():
    ocr_options = OCROptions.fromdict({"ocr_system": "azure_doc_intelligence"})
    assert ocr_options.ocr_system == "azure_doc_intelligence"


def test_ocr_options_invalid_initialize_fromdict():
    error_msg = "OCROptions can only accept 'ocr_system'"
    with pytest.raises(TypeError) as excinfo:
        OCROptions.fromdict({"ocr_system": "azure_doc_intelligence", "junk": "value"})
    assert error_msg in str(excinfo.value)


def test_ocr_options_setters():
    ocr_options = OCROptions(ocr_system="hybrid")
    assert ocr_options.ocr_system == "hybrid"


def test_ocr_options_ocr_system_validator():
    error_msg = "OCROptions.ocr_system must be one of azure_computer_vision,azure_doc_intelligence,hybrid,paddleocr, but got junk"
    ocr_options = OCROptions()
    with pytest.raises(ValueError) as excinfo:
        ocr_options.ocr_system = "junk"
    assert error_msg in str(excinfo.value)


def test_ocr_options_to_dict():
    ocr_options = OCROptions().to_dict()
    assert ocr_options["ocr_system"] == "paddleocr"


# Timestamp Tests
def test_timestamp_initializer():
    timestamp = Timestamp(start=2.0, end=3.0)
    assert timestamp.start == 2.0
    assert timestamp.end == 3.0


def test_timestamp_initialize_fromdict():
    timestamp = Timestamp.fromdict({"start": 2.0, "end": 3.0})
    assert timestamp.start == 2.0
    assert timestamp.end == 3.0


def test_timestamp_invalid_initialize_fromdict():
    error_msg = "Timestamp can only accept the values 'start' and 'end'"
    with pytest.raises(TypeError) as excinfo:
        Timestamp.fromdict({"start": 2.0, "end": 3.0, "junk": "value"})
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
        Timestamp.fromdict({"start": "test", "end": 3.0})
    assert error_msg in str(excinfo.value)


def test_timestamp_end_validator():
    error_msg = "Timestamp.end must be of type float"
    with pytest.raises(ValueError) as excinfo:
        Timestamp.fromdict({"start": 2.0, "end": "test"})
    assert error_msg in str(excinfo.value)


def test_timestamp_to_dict():
    timestamp = Timestamp(start=2.0, end=3.0).to_dict()
    assert timestamp["start"] == 2.0
    assert timestamp["end"] == 3.0


# Process Text Request Tests
def test_process_text_request_default_initializer():
    process_text_request = ProcessTextRequest(text=["hey"])
    assert process_text_request.text == ["hey"]
    assert process_text_request.link_batch is None
    assert process_text_request.entity_detection is None
    assert process_text_request.processed_text is None


def test_process_text_request_initializer():
    text = ["hey!"]
    link_batch = True
    entity_type = EntityTypeSelector(type="ENABLE", value=["NAME"])
    filter = FilterSelector(type="ALLOW", pattern="hey")
    entity_detection = EntityDetection(
        accuracy="standard",
        entity_types=[entity_type],
        filter=[filter],
        return_entity=False,
    )
    processed_text = ProcessedText(type="MARKER", pattern="BEST_ENTITY_TYPE")

    process_text_request = ProcessTextRequest(
        text=text,
        link_batch=link_batch,
        entity_detection=entity_detection,
        processed_text=processed_text,
    )

    assert process_text_request.text == text
    assert process_text_request.link_batch == link_batch
    assert process_text_request.entity_detection.accuracy == entity_detection.accuracy
    assert (
        process_text_request.entity_detection.entity_types[0].type == entity_type.type
    )
    assert (
        process_text_request.entity_detection.entity_types[0].value == entity_type.value
    )
    assert process_text_request.entity_detection.filter[0].type == filter.type
    assert process_text_request.entity_detection.filter[0].pattern == filter.pattern
    assert process_text_request.processed_text.type == processed_text.type
    assert process_text_request.processed_text.pattern == processed_text.pattern


def test_process_text_request_initialize_fromdict():
    request_obj = {
        "text": ["hey!"],
        "link_batch": False,
        "entity_detection": {
            "accuracy": "standard",
            "entity_types": [{"type": "DISABLE", "value": ["LOCATION"]}],
            "filter": [{"type": "BLOCK", "pattern": "Roger", "entity_type": "TEST"}],
            "return_entity": False,
        },
        "processed_text": {"type": "MARKER", "pattern": "ALL_ENTITY_TYPES"},
    }
    process_text_request = ProcessTextRequest.fromdict(request_obj)
    assert process_text_request.text == request_obj["text"]
    assert process_text_request.link_batch == request_obj["link_batch"]
    assert (
        process_text_request.entity_detection.accuracy
        == request_obj["entity_detection"]["accuracy"]
    )
    assert (
        process_text_request.entity_detection.entity_types[0].type
        == request_obj["entity_detection"]["entity_types"][0]["type"]
    )
    assert (
        process_text_request.entity_detection.entity_types[0].value
        == request_obj["entity_detection"]["entity_types"][0]["value"]
    )
    assert (
        process_text_request.entity_detection.filter[0].type
        == request_obj["entity_detection"]["filter"][0]["type"]
    )
    assert (
        process_text_request.entity_detection.filter[0].pattern
        == request_obj["entity_detection"]["filter"][0]["pattern"]
    )
    assert (
        process_text_request.processed_text.type
        == request_obj["processed_text"]["type"]
    )
    assert (
        process_text_request.processed_text.pattern
        == request_obj["processed_text"]["pattern"]
    )


def test_process_text_request_invalid_initialize_fromdict():
    error_msg = "ProcessTextRequest can only accept the values 'text', 'link_batch', 'entity_detection' and 'process_text'"
    request_obj = {
        "text": ["hey!"],
        "link_batch": False,
        "entity_detection": {
            "accuracy": "standard",
            "entity_types": [{"type": "DISABLE", "value": ["LOCATION"]}],
            "filter": [{"type": "BLOCK", "pattern": "Roger"}],
            "return_entity": False,
        },
        "processed_text": {"type": "MARKER", "pattern": "ALL_ENTITY_TYPES"},
        "junk": "value",
    }
    with pytest.raises(TypeError) as excinfo:
        ProcessTextRequest.fromdict(request_obj)
    assert error_msg in str(excinfo.value)


def test_process_text_request_to_dict():
    text = ["hey!"]
    link_batch = True
    entity_type = EntityTypeSelector(type="ENABLE", value=["NAME"])
    filter = FilterSelector(type="ALLOW", pattern="hey")
    entity_detection = EntityDetection(
        accuracy="standard",
        entity_types=[entity_type],
        filter=[filter],
        return_entity=False,
    )
    processed_text = ProcessedText(type="MARKER", pattern="BEST_ENTITY_TYPE")

    process_text_request = ProcessTextRequest(
        text=text,
        link_batch=link_batch,
        entity_detection=entity_detection,
        processed_text=processed_text,
    ).to_dict()
    print(process_text_request)
    assert process_text_request["text"] == text
    assert process_text_request["link_batch"] == link_batch
    assert (
        process_text_request["entity_detection"]["accuracy"]
        == entity_detection.accuracy
    )
    assert (
        process_text_request["entity_detection"]["entity_types"][0]["type"]
        == entity_type.type
    )
    assert (
        process_text_request["entity_detection"]["entity_types"][0]["value"]
        == entity_type.value
    )
    assert process_text_request["entity_detection"]["filter"][0]["type"] == filter.type
    assert (
        process_text_request["entity_detection"]["filter"][0]["pattern"]
        == filter.pattern
    )
    assert process_text_request["processed_text"]["type"] == processed_text.type
    assert process_text_request["processed_text"]["pattern"] == processed_text.pattern


# NER Text Request Tests
def test_ner_text_request_default_initializer():
    ner_text_request = NerTextRequest(text=["hey"])
    assert ner_text_request.text == ["hey"]
    assert ner_text_request.link_batch is None
    assert ner_text_request.entity_detection is None


def test_ner_text_request_initializer():
    text = ["hey!"]
    link_batch = True
    entity_type = EntityTypeSelector(type="ENABLE", value=["NAME"])
    filter = FilterSelector(type="ALLOW", pattern="hey")
    entity_detection = EntityDetection(
        accuracy="standard",
        entity_types=[entity_type],
        filter=[filter],
        return_entity=False,
    )

    ner_text_request = NerTextRequest(
        text=text,
        link_batch=link_batch,
        entity_detection=entity_detection,
    )

    assert ner_text_request.text == text
    assert ner_text_request.link_batch == link_batch
    assert ner_text_request.entity_detection.accuracy == entity_detection.accuracy
    assert ner_text_request.entity_detection.entity_types[0].type == entity_type.type
    assert ner_text_request.entity_detection.entity_types[0].value == entity_type.value
    assert ner_text_request.entity_detection.filter[0].type == filter.type
    assert ner_text_request.entity_detection.filter[0].pattern == filter.pattern


def test_ner_text_request_initialize_fromdict():
    request_obj = {
        "text": ["hey!"],
        "link_batch": False,
        "entity_detection": {
            "accuracy": "standard",
            "entity_types": [{"type": "DISABLE", "value": ["LOCATION"]}],
            "filter": [{"type": "BLOCK", "pattern": "Roger", "entity_type": "TEST"}],
            "return_entity": False,
        },
    }
    ner_text_request = NerTextRequest.fromdict(request_obj)
    assert ner_text_request.text == request_obj["text"]
    assert ner_text_request.link_batch == request_obj["link_batch"]
    assert (
        ner_text_request.entity_detection.accuracy
        == request_obj["entity_detection"]["accuracy"]
    )
    assert (
        ner_text_request.entity_detection.entity_types[0].type
        == request_obj["entity_detection"]["entity_types"][0]["type"]
    )
    assert (
        ner_text_request.entity_detection.entity_types[0].value
        == request_obj["entity_detection"]["entity_types"][0]["value"]
    )
    assert (
        ner_text_request.entity_detection.filter[0].type
        == request_obj["entity_detection"]["filter"][0]["type"]
    )
    assert (
        ner_text_request.entity_detection.filter[0].pattern
        == request_obj["entity_detection"]["filter"][0]["pattern"]
    )


def test_ner_text_request_invalid_initialize_fromdict():
    error_msg = "NerTextRequest can only accept the values 'text', 'link_batch' and 'entity_detection'"
    request_obj = {
        "text": ["hey!"],
        "link_batch": False,
        "entity_detection": {
            "accuracy": "standard",
            "entity_types": [{"type": "DISABLE", "value": ["LOCATION"]}],
            "filter": [{"type": "BLOCK", "pattern": "Roger"}],
            "return_entity": False,
        },
        "junk": "value",
    }
    with pytest.raises(TypeError) as excinfo:
        NerTextRequest.fromdict(request_obj)
    assert error_msg in str(excinfo.value)


def test_ner_text_request_to_dict():
    text = ["hey!"]
    link_batch = True
    entity_type = EntityTypeSelector(type="ENABLE", value=["NAME"])
    filter = FilterSelector(type="ALLOW", pattern="hey")
    entity_detection = EntityDetection(
        accuracy="standard",
        entity_types=[entity_type],
        filter=[filter],
        return_entity=False,
    )

    ner_text_request = NerTextRequest(
        text=text,
        link_batch=link_batch,
        entity_detection=entity_detection,
    ).to_dict()
    print(ner_text_request)
    assert ner_text_request["text"] == text
    assert ner_text_request["link_batch"] == link_batch
    assert ner_text_request["entity_detection"]["accuracy"] == entity_detection.accuracy
    assert (
        ner_text_request["entity_detection"]["entity_types"][0]["type"]
        == entity_type.type
    )
    assert (
        ner_text_request["entity_detection"]["entity_types"][0]["value"]
        == entity_type.value
    )
    assert ner_text_request["entity_detection"]["filter"][0]["type"] == filter.type
    assert (
        ner_text_request["entity_detection"]["filter"][0]["pattern"] == filter.pattern
    )


# Analyze Text Request Tests
def test_analyze_text_request_default_initializer():
    analyze_text_request = AnalyzeTextRequest(text=["hey"], locale="en-US")
    assert analyze_text_request.text == ["hey"]
    assert analyze_text_request.locale == "en-US"
    assert analyze_text_request.link_batch is None
    assert analyze_text_request.entity_detection is None


def test_analyze_text_request_initializer():
    text = ["hey!"]
    locale = "en-US"
    link_batch = True
    entity_type = EntityTypeSelector(type="ENABLE", value=["NAME"])
    filter = FilterSelector(type="ALLOW", pattern="hey")
    entity_detection = EntityDetection(
        accuracy="standard",
        entity_types=[entity_type],
        filter=[filter],
        return_entity=False,
    )

    analyze_text_request = AnalyzeTextRequest(
        text=text,
        locale=locale,
        link_batch=link_batch,
        entity_detection=entity_detection,
    )

    assert analyze_text_request.text == text
    assert analyze_text_request.locale == locale
    assert analyze_text_request.link_batch == link_batch
    assert analyze_text_request.entity_detection.accuracy == entity_detection.accuracy
    assert (
        analyze_text_request.entity_detection.entity_types[0].type == entity_type.type
    )
    assert (
        analyze_text_request.entity_detection.entity_types[0].value == entity_type.value
    )
    assert analyze_text_request.entity_detection.filter[0].type == filter.type
    assert analyze_text_request.entity_detection.filter[0].pattern == filter.pattern


def test_analyze_text_request_initialize_fromdict():
    request_obj = {
        "text": ["hey!"],
        "locale": "en-US",
        "link_batch": False,
        "entity_detection": {
            "accuracy": "standard",
            "entity_types": [{"type": "DISABLE", "value": ["LOCATION"]}],
            "filter": [{"type": "BLOCK", "pattern": "Roger", "entity_type": "TEST"}],
            "return_entity": False,
        },
    }
    analyze_text_request = AnalyzeTextRequest.fromdict(request_obj)
    assert analyze_text_request.text == request_obj["text"]
    assert analyze_text_request.locale == request_obj["locale"]
    assert analyze_text_request.link_batch == request_obj["link_batch"]
    assert (
        analyze_text_request.entity_detection.accuracy
        == request_obj["entity_detection"]["accuracy"]
    )
    assert (
        analyze_text_request.entity_detection.entity_types[0].type
        == request_obj["entity_detection"]["entity_types"][0]["type"]
    )
    assert (
        analyze_text_request.entity_detection.entity_types[0].value
        == request_obj["entity_detection"]["entity_types"][0]["value"]
    )
    assert (
        analyze_text_request.entity_detection.filter[0].type
        == request_obj["entity_detection"]["filter"][0]["type"]
    )
    assert (
        analyze_text_request.entity_detection.filter[0].pattern
        == request_obj["entity_detection"]["filter"][0]["pattern"]
    )


def test_analyze_text_request_invalid_initialize_fromdict():
    error_msg = "AnalyzeTextRequest can only accept the values 'text', 'locale', 'link_batch' and 'entity_detection'"
    request_obj = {
        "text": ["hey!"],
        "link_batch": False,
        "entity_detection": {
            "accuracy": "standard",
            "entity_types": [{"type": "DISABLE", "value": ["LOCATION"]}],
            "filter": [{"type": "BLOCK", "pattern": "Roger"}],
            "return_entity": False,
        },
        "junk": "value",
    }
    with pytest.raises(TypeError) as excinfo:
        AnalyzeTextRequest.fromdict(request_obj)
    assert error_msg in str(excinfo.value)


def test_analyze_text_request_to_dict():
    text = ["hey!"]
    locale = "en"
    link_batch = True
    entity_type = EntityTypeSelector(type="ENABLE", value=["NAME"])
    filter = FilterSelector(type="ALLOW", pattern="hey")
    entity_detection = EntityDetection(
        accuracy="standard",
        entity_types=[entity_type],
        filter=[filter],
        return_entity=False,
    )

    analyze_text_request = AnalyzeTextRequest(
        text=text,
        locale=locale,
        link_batch=link_batch,
        entity_detection=entity_detection,
    ).to_dict()
    print(analyze_text_request)
    assert analyze_text_request["text"] == text
    assert analyze_text_request["locale"] == locale
    assert analyze_text_request["link_batch"] == link_batch
    assert (
        analyze_text_request["entity_detection"]["accuracy"]
        == entity_detection.accuracy
    )
    assert (
        analyze_text_request["entity_detection"]["entity_types"][0]["type"]
        == entity_type.type
    )
    assert (
        analyze_text_request["entity_detection"]["entity_types"][0]["value"]
        == entity_type.value
    )
    assert analyze_text_request["entity_detection"]["filter"][0]["type"] == filter.type
    assert (
        analyze_text_request["entity_detection"]["filter"][0]["pattern"]
        == filter.pattern
    )


# Process File URI Request Tests
def test_process_file_uri_request_default_initializer():
    process_file_uri_obj = ProcessFileUriRequest(uri="this/location/right/here.png")
    assert process_file_uri_obj.uri == "this/location/right/here.png"
    assert process_file_uri_obj.entity_detection is None
    assert process_file_uri_obj.object_entity_detection is None
    assert process_file_uri_obj.pdf_options is None
    assert process_file_uri_obj.audio_options is None


def test_process_file_uri_request_initializer():
    entity_type = EntityTypeSelector(type="ENABLE", value=["NAME"])
    filter = FilterSelector(type="ALLOW", pattern="hey")
    entity_detection = EntityDetection(
        accuracy="standard",
        entity_types=[entity_type],
        filter=[filter],
        return_entity=False,
    )
    pdf_options = PDFOptions(density=100)
    audio_options = AudioOptions(
        bleep_start_padding=1.0,
        bleep_end_padding=2.0,
        bleep_frequency=200,
        bleep_gain=-2,
    )
    object_entity_type = ObjectEntityTypeSelector(type="ENABLE", value=["LOGO"])
    object_entity_detection = ObjectEntityDetection(
        object_entity_types=[object_entity_type],
    )
    process_file_uri_obj = ProcessFileUriRequest(
        uri="this/location/right/here.png",
        entity_detection=entity_detection,
        object_entity_detection=object_entity_detection,
        pdf_options=pdf_options,
        audio_options=audio_options,
    )
    assert process_file_uri_obj.uri == "this/location/right/here.png"
    assert process_file_uri_obj.entity_detection.accuracy == "standard"
    assert (
        process_file_uri_obj.object_entity_detection.object_entity_types[0].type
        == "ENABLE"
    )
    assert process_file_uri_obj.pdf_options.density == 100
    assert process_file_uri_obj.audio_options.bleep_end_padding == 2.0
    assert process_file_uri_obj.audio_options.bleep_frequency == 200
    assert process_file_uri_obj.audio_options.bleep_gain == -2


def test_process_file_uri_request_initialize_fromdict():
    entity_type = EntityTypeSelector(type="ENABLE", value=["NAME"])
    filter = FilterSelector(type="ALLOW", pattern="hey")
    entity_detection = EntityDetection(
        accuracy="standard",
        entity_types=[entity_type],
        filter=[filter],
        return_entity=False,
    )
    pdf_options = PDFOptions(density=100)
    audio_options = AudioOptions(
        bleep_start_padding=1.0,
        bleep_end_padding=2.0,
        bleep_frequency=200,
        bleep_gain=-2,
    )
    object_entity_type = ObjectEntityTypeSelector(type="ENABLE", value=["LOGO"])
    object_entity_detection = ObjectEntityDetection(
        object_entity_types=[object_entity_type],
    )
    ocr_options = OCROptions(ocr_system="azure_computer_vision")
    process_file_uri_obj = ProcessFileUriRequest.fromdict(
        {
            "uri": "this/location/right/here.png",
            "entity_detection": entity_detection.to_dict(),
            "object_entity_detection": object_entity_detection.to_dict(),
            "pdf_options": pdf_options.to_dict(),
            "audio_options": audio_options.to_dict(),
            "ocr_options": ocr_options.to_dict(),
        }
    )
    assert process_file_uri_obj.uri == "this/location/right/here.png"
    assert process_file_uri_obj.entity_detection.accuracy == "standard"
    assert (
        process_file_uri_obj.object_entity_detection.object_entity_types[0].type
        == "ENABLE"
    )
    assert process_file_uri_obj.pdf_options.density == 100
    assert process_file_uri_obj.audio_options.bleep_end_padding == 2.0
    assert process_file_uri_obj.audio_options.bleep_frequency == 200
    assert process_file_uri_obj.audio_options.bleep_gain == -2
    assert process_file_uri_obj.ocr_options.ocr_system == "azure_computer_vision"


def test_process_file_uri_request_invalid_initialize_fromdict():
    error_msg = "ProcessFileUriRequest can only accept the values 'uri', 'entity_detection', 'object_entity_detection', 'pdf_options', 'audio_options', 'image_options' and 'ocr_options'"
    entity_type = EntityTypeSelector(type="ENABLE", value=["NAME"])
    filter = FilterSelector(type="ALLOW", pattern="hey")
    entity_detection = EntityDetection(
        accuracy="standard",
        entity_types=[entity_type],
        filter=[filter],
        return_entity=False,
    )
    pdf_options = PDFOptions(density=100)
    audio_options = AudioOptions(
        bleep_start_padding=1.0,
        bleep_end_padding=2.0,
        bleep_frequency=200,
        bleep_gain=-2,
    )
    object_entity_type = ObjectEntityTypeSelector(type="ENABLE", value=["LOGO"])
    object_entity_detection = ObjectEntityDetection(
        object_entity_types=[object_entity_type],
    )
    ocr_options = OCROptions(ocr_system="azure_computer_vision")
    with pytest.raises(TypeError) as excinfo:
        ProcessFileUriRequest.fromdict(
            {
                "uri": "this/location/right/here.png",
                "entity_detection": entity_detection.to_dict(),
                "object_entity_detection": object_entity_detection.to_dict(),
                "pdf_options": pdf_options.to_dict(),
                "audio_options": audio_options.to_dict(),
                "ocr_options": ocr_options.to_dict(),
                "junk": "value",
            }
        )
    assert error_msg in str(excinfo.value)


def test_process_file_uri_request_to_dict():
    entity_type = EntityTypeSelector(type="ENABLE", value=["NAME"])
    filter = FilterSelector(type="ALLOW", pattern="hey")
    entity_detection = EntityDetection(
        accuracy="standard",
        entity_types=[entity_type],
        filter=[filter],
        return_entity=False,
    )
    pdf_options = PDFOptions(density=100)
    audio_options = AudioOptions(
        bleep_start_padding=1.0,
        bleep_end_padding=2.0,
        bleep_frequency=200,
        bleep_gain=-2,
    )
    object_entity_type = ObjectEntityTypeSelector(type="ENABLE", value=["LOGO"])
    object_entity_detection = ObjectEntityDetection(
        object_entity_types=[object_entity_type],
    )
    process_file_uri_obj = ProcessFileUriRequest(
        uri="this/location/right/here.png",
        entity_detection=entity_detection,
        object_entity_detection=object_entity_detection,
        pdf_options=pdf_options,
        audio_options=audio_options,
    ).to_dict()
    assert process_file_uri_obj["uri"] == "this/location/right/here.png"
    assert process_file_uri_obj["entity_detection"]["accuracy"] == "standard"
    assert (
        process_file_uri_obj["object_entity_detection"]["object_entity_types"][0][
            "type"
        ]
        == "ENABLE"
    )
    assert process_file_uri_obj["pdf_options"]["density"] == 100
    assert process_file_uri_obj["audio_options"]["bleep_end_padding"] == 2.0
    assert process_file_uri_obj["audio_options"]["bleep_frequency"] == 200
    assert process_file_uri_obj["audio_options"]["bleep_gain"] == -2


# Process File Base64 Request Tests
def test_process_file_base64_request_default_initializer():
    process_file_base64_request_obj = ProcessFileBase64Request(
        file="sfsfxe234jkjsdlkfnDATA!!!!!!"
    )
    assert process_file_base64_request_obj.file == "sfsfxe234jkjsdlkfnDATA!!!!!!"
    assert process_file_base64_request_obj.entity_detection is None
    assert process_file_base64_request_obj.object_entity_detection is None
    assert process_file_base64_request_obj.pdf_options is None
    assert process_file_base64_request_obj.audio_options is None


def test_process_file_base64_request_initializer():
    entity_type = EntityTypeSelector(type="ENABLE", value=["NAME"])
    filter = FilterSelector(type="ALLOW", pattern="hey")
    entity_detection = EntityDetection(
        accuracy="standard",
        entity_types=[entity_type],
        filter=[filter],
        return_entity=False,
    )
    pdf_options = PDFOptions(density=100)
    audio_options = AudioOptions(
        bleep_start_padding=1.0,
        bleep_end_padding=2.0,
        bleep_frequency=200,
        bleep_gain=-2,
    )
    object_entity_type = ObjectEntityTypeSelector(type="ENABLE", value=["LOGO"])
    object_entity_detection = ObjectEntityDetection(
        object_entity_types=[object_entity_type],
    )
    process_file_base64_request_obj = ProcessFileBase64Request(
        file="sfsfxe234jkjsdlkfnDATA",
        entity_detection=entity_detection,
        object_entity_detection=object_entity_detection,
        pdf_options=pdf_options,
        audio_options=audio_options,
    )
    assert process_file_base64_request_obj.file == "sfsfxe234jkjsdlkfnDATA"
    assert process_file_base64_request_obj.entity_detection.accuracy == "standard"
    assert (
        process_file_base64_request_obj.object_entity_detection.object_entity_types[
            0
        ].type
        == "ENABLE"
    )
    assert process_file_base64_request_obj.pdf_options.density == 100
    assert process_file_base64_request_obj.audio_options.bleep_end_padding == 2.0
    assert process_file_base64_request_obj.audio_options.bleep_frequency == 200
    assert process_file_base64_request_obj.audio_options.bleep_gain == -2


def test_process_file_base64_request_initialize_fromdict():
    file = File(data="sfsfxe234jkjsdlkfnDATA", content_type="application/pdf")
    entity_type = EntityTypeSelector(type="ENABLE", value=["NAME"])
    filter = FilterSelector(type="ALLOW", pattern="hey")
    entity_detection = EntityDetection(
        accuracy="standard",
        entity_types=[entity_type],
        filter=[filter],
        return_entity=False,
    )
    pdf_options = PDFOptions(density=100)
    audio_options = AudioOptions(
        bleep_start_padding=1.0,
        bleep_end_padding=2.0,
        bleep_frequency=200,
        bleep_gain=-2,
    )
    object_entity_type = ObjectEntityTypeSelector(type="ENABLE", value=["LOGO"])
    object_entity_detection = ObjectEntityDetection(
        object_entity_types=[object_entity_type],
    )
    process_file_base64_request_obj = ProcessFileBase64Request.fromdict(
        {
            "file": file.to_dict(),
            "entity_detection": entity_detection.to_dict(),
            "object_entity_detection": object_entity_detection.to_dict(),
            "pdf_options": pdf_options.to_dict(),
            "audio_options": audio_options.to_dict(),
        }
    )
    assert process_file_base64_request_obj.file.data == "sfsfxe234jkjsdlkfnDATA"
    assert process_file_base64_request_obj.entity_detection.accuracy == "standard"
    assert (
        process_file_base64_request_obj.object_entity_detection.object_entity_types[
            0
        ].type
        == "ENABLE"
    )
    assert process_file_base64_request_obj.pdf_options.density == 100
    assert process_file_base64_request_obj.audio_options.bleep_end_padding == 2.0
    assert process_file_base64_request_obj.audio_options.bleep_frequency == 200
    assert process_file_base64_request_obj.audio_options.bleep_gain == -2


def test_process_file_base64_request_invalid_initialize_fromdict():
    error_msg = "ProcessFileBase64Request can only accept the values 'file', 'entity_detection', 'object_entity_detection', 'pdf_options', 'audio_options', 'image_options' and 'ocr_options'"
    file = File(data="sfsfxe234jkjsdlkfnDATA", content_type="application/pdf")
    entity_type = EntityTypeSelector(type="ENABLE", value=["NAME"])
    filter = FilterSelector(type="ALLOW", pattern="hey")
    entity_detection = EntityDetection(
        accuracy="standard",
        entity_types=[entity_type],
        filter=[filter],
        return_entity=False,
    )
    pdf_options = PDFOptions(density=100)
    audio_options = AudioOptions(
        bleep_start_padding=1.0,
        bleep_end_padding=2.0,
        bleep_frequency=200,
        bleep_gain=-2,
    )
    object_entity_type = ObjectEntityTypeSelector(type="ENABLE", value=["LOGO"])
    object_entity_detection = ObjectEntityDetection(
        object_entity_types=[object_entity_type],
    )
    ocr_options = OCROptions(ocr_system="azure_computer_vision")
    with pytest.raises(TypeError) as excinfo:
        ProcessFileBase64Request.fromdict(
            {
                "file": file.to_dict(),
                "entity_detection": entity_detection.to_dict(),
                "object_entity_detection": object_entity_detection.to_dict(),
                "pdf_options": pdf_options.to_dict(),
                "audio_options": audio_options.to_dict(),
                "ocr_options": ocr_options.to_dict(),
                "junk": "value",
            }
        )
    assert error_msg in str(excinfo.value)


def test_process_file_base64_request_to_dict():
    entity_type = EntityTypeSelector(type="ENABLE", value=["NAME"])
    filter = FilterSelector(type="ALLOW", pattern="hey")
    entity_detection = EntityDetection(
        accuracy="standard",
        entity_types=[entity_type],
        filter=[filter],
        return_entity=False,
    )
    pdf_options = PDFOptions(density=100)
    audio_options = AudioOptions(
        bleep_start_padding=1.0,
        bleep_end_padding=2.0,
        bleep_frequency=200,
        bleep_gain=-2,
    )
    object_entity_type = ObjectEntityTypeSelector(type="DISABLE", value=["LOGO"])
    object_entity_detection = ObjectEntityDetection(
        object_entity_types=[object_entity_type],
    )
    process_file_base64_request_obj = ProcessFileBase64Request(
        file="sfsfxe234jkjsdlkfnDATA",
        entity_detection=entity_detection,
        object_entity_detection=object_entity_detection,
        pdf_options=pdf_options,
        audio_options=audio_options,
    ).to_dict()
    assert process_file_base64_request_obj["file"] == "sfsfxe234jkjsdlkfnDATA"
    assert process_file_base64_request_obj["entity_detection"]["accuracy"] == "standard"
    assert (
        process_file_base64_request_obj["object_entity_detection"][
            "object_entity_types"
        ][0]["type"]
        == "DISABLE"
    )
    assert process_file_base64_request_obj["pdf_options"]["density"] == 100
    assert process_file_base64_request_obj["audio_options"]["bleep_end_padding"] == 2.0
    assert process_file_base64_request_obj["audio_options"]["bleep_frequency"] == 200
    assert process_file_base64_request_obj["audio_options"]["bleep_gain"] == -2


# Bleep Request Tests
def test_bleep_request_initializer():
    file = File(data="test", content_type="image/jpg")
    timestamps = [Timestamp(start=0.0, end=1.0)]
    bleep_request = BleepRequest(file=file, timestamps=timestamps)
    assert bleep_request.file.data == "test"
    assert bleep_request.timestamps[0].start == 0


def test_bleep_request_initialize_fromdict():
    file = File(data="test", content_type="image/jpg")
    timestamps = [Timestamp(start=0.0, end=1.0)]
    bleep_request = BleepRequest.fromdict(
        {"file": file.to_dict(), "timestamps": [row.to_dict() for row in timestamps]}
    )
    assert bleep_request.file.data == "test"
    assert bleep_request.timestamps[0].start == 0


def test_bleep_request_invalid_initialize_fromdict():
    error_msg = "BleepRequest can only accept the values 'file', 'timestamps', 'bleep_frequency', and 'bleep_gain'"
    file = File(data="test", content_type="image/jpg")
    timestamps = [Timestamp(start=0.0, end=1.0)]
    with pytest.raises(TypeError) as excinfo:
        BleepRequest.fromdict(
            {
                "file": file.to_dict(),
                "timestamps": [row.to_dict() for row in timestamps],
                "bleep_gain": 2,
                "bleep_frequency": 400,
                "junk": "value",
            }
        )
    assert error_msg in str(excinfo.value)


def test_bleep_request_to_dict():
    file = File(data="test", content_type="image/jpg")
    timestamps = [Timestamp(start=0.0, end=1.0)]
    bleep_request = BleepRequest(file=file, timestamps=timestamps).to_dict()
    assert bleep_request["file"]["data"] == "test"
    assert bleep_request["timestamps"][0]["start"] == 0


# Reidentify Text Request Tests
def test_reidentify_text_request_initializer():
    processed_text = ["this is a test"]
    entities = [Entity(processed_text="NAME", text="Hola")]
    model = "gpt-700.2-ultra-turbo"
    reid = ReidentifyTextRequest(
        processed_text=processed_text,
        entities=entities,
        model=model,
        reidentify_sensitive_fields=True,
    )
    assert reid.processed_text == ["this is a test"]
    assert reid.entities[0].text == "Hola"
    assert reid.model == "gpt-700.2-ultra-turbo"
    assert reid.reidentify_sensitive_fields == True


def test_reidentify_text_request_initialize_fromdict():
    processed_text = ["this is a test"]
    entities = [Entity(processed_text="NAME", text="Hola")]
    model = "gpt-700.2-ultra-turbo"
    reid = ReidentifyTextRequest.fromdict(
        {
            "processed_text": processed_text,
            "entities": [row.to_dict() for row in entities],
            "model": model,
            "reidentify_sensitive_fields": False,
        }
    )
    assert reid.processed_text == ["this is a test"]
    assert reid.entities[0].text == "Hola"
    assert reid.model == "gpt-700.2-ultra-turbo"
    assert reid.reidentify_sensitive_fields == False


def test_reidentify_text_request_invalid_initialize_fromdict():
    error_msg = "ReidentifyTextRequest can only accept the values 'processed_text', 'entities', 'model' and 'reidentify_sensitive_fields'"
    processed_text = ["this is a test"]
    entities = [Entity(processed_text="NAME", text="Hola")]
    model = "gpt-700.2-ultra-turbo"
    with pytest.raises(TypeError) as excinfo:
        ReidentifyTextRequest.fromdict(
            {
                "processed_text": processed_text,
                "entities": [row.to_dict() for row in entities],
                "model": model,
                "junk": "value",
            }
        )
        assert error_msg in str(excinfo.value)


def test_reidentify_text_request_to_dict():
    processed_text = ["this is a test"]
    entities = [Entity(processed_text="NAME", text="Hola")]
    model = "gpt-700.2-ultra-turbo"
    reidentify_sensitive_fields = False
    reid = ReidentifyTextRequest(
        processed_text=processed_text,
        entities=entities,
        model=model,
        reidentify_sensitive_fields=reidentify_sensitive_fields,
    ).to_dict()
    assert reid["processed_text"][0] == "this is a test"
    assert reid["entities"][0]["text"] == "Hola"
    assert reid["model"] == "gpt-700.2-ultra-turbo"
    assert reid["reidentify_sensitive_fields"] == reidentify_sensitive_fields


def test_synthetic_text():
    processed_text = ProcessedText(
        type="SYNTHETIC",
        synthetic_entity_accuracy="standard",
        preserve_relationships=True,
    )
    assert processed_text.type == "SYNTHETIC"
    assert hasattr(processed_text, "pattern") == False


def test_change_type():
    processed_text = ProcessedText(
        type="MARKER", pattern="UNIQUE_NUMBERED_ENTITY_TYPE"
    )  # Marker
    processed_text.type = "MASK"
    assert processed_text.type == "MASK"
    assert hasattr(processed_text, "pattern") == False
    assert processed_text.mask_character == "#"


def test_mask_invalid_mask_character_initialize():
    error_msg = "mask_character must have only one character."
    with pytest.raises(ValueError) as excinfo:
        processed_text = ProcessedText(type="MASK", mask_character="invalid")
    assert error_msg in str(excinfo.value)


def test_mask_invalid_mask_character():
    error_msg = "mask_character must have only one character."
    processed_text = ProcessedText()
    processed_text.type = "MASK"
    assert processed_text.type == "MASK"
    with pytest.raises(ValueError) as excinfo:
        processed_text.mask_character = "invalid"
    assert error_msg in str(excinfo.value)


def test_synthetic_invalid_accuracy_initialize():
    error_msg = "Synthetic Entity Accuracy can only accept values"
    with pytest.raises(ValueError) as excinfo:
        processed_text = ProcessedText(
            type="SYNTHETIC",
            synthetic_entity_accuracy="invalid",
            preserve_relationships=True,
        )
    assert error_msg in str(excinfo.value)


def test_synthetic_invalid_accuracy():
    error_msg = "Synthetic Entity Accuracy can only accept values"
    processed_text = ProcessedText(
        type="SYNTHETIC",
        preserve_relationships=True,
    )
    with pytest.raises(ValueError) as excinfo:
        processed_text.synthetic_entity_accuracy = "invalid"
    assert error_msg in str(excinfo.value)
