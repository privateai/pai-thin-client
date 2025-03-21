import inspect
from typing import List, Optional, Union


class BaseRequestObject:
    def to_dict(self):
        dict_obj = dict()
        for key, value in self.__dict__.items():
            if value in [None, [], {}]:
                continue
            name = key if key[0] != "_" else key[1:]
            if self._issubclass(value):
                dict_obj[name] = value.to_dict()
            elif type(value) is list:
                dict_obj[name] = [
                    row.to_dict() if self._issubclass(row) else row for row in value
                ]
            elif not key.startswith("__") and not callable(key):
                dict_obj[name] = value
        return dict_obj

    def _issubclass(self, obj):
        return inspect.isclass(type(obj)) and issubclass(type(obj), BaseRequestObject)

    def __call__(self):
        return self.to_dict()

    @classmethod
    def _fromdict(cls, values: dict):
        return cls(**values)


class AudioOptions(BaseRequestObject):
    default_bleep_start_padding: float = 0.5
    default_bleep_end_padding: float = 0.5
    default_bleep_frequency: Optional[int] = None
    default_bleep_gain: Optional[int] = None

    def __init__(
        self,
        bleep_start_padding: float = default_bleep_start_padding,
        bleep_end_padding: float = default_bleep_end_padding,
        bleep_frequency: Optional[int] = default_bleep_frequency,
        bleep_gain: Optional[int] = default_bleep_gain,
    ):
        if self._bleep_start_padding_validator(bleep_start_padding):
            self._bleep_start_padding = bleep_start_padding
        if self._bleep_end_padding_validator(bleep_end_padding):
            self._bleep_end_padding = bleep_end_padding
        if self._bleep_frequency_validator(bleep_frequency):
            self._bleep_frequency = bleep_frequency
        if self._bleep_gain_validator(bleep_gain):
            self._bleep_gain = bleep_gain

    @property
    def bleep_start_padding(self):
        return self._bleep_start_padding

    @property
    def bleep_end_padding(self):
        return self._bleep_end_padding

    @property
    def bleep_frequency(self):
        return self._bleep_frequency

    @property
    def bleep_gain(self):
        return self._bleep_gain

    @bleep_start_padding.setter
    def bleep_start_padding(self, var):
        if self._bleep_start_padding_validator(var):
            self._bleep_start_padding = var

    @bleep_end_padding.setter
    def bleep_end_padding(self, var):
        if self._bleep_end_padding_validator(var):
            self._bleep_end_padding = var

    @bleep_frequency.setter
    def bleep_frequency(self, var):
        if self._bleep_frequency_validator(var):
            self._bleep_frequency = var

    @bleep_gain.setter
    def bleep_gain(self, var):
        if self._bleep_gain_validator(var):
            self._bleep_gain = var

    def _bleep_start_padding_validator(self, var):
        if type(var) is not float:
            raise ValueError(
                f"AudioOptions.bleep_start_padding must be of type float, but got {type(var)}"
            )
        if var < 0:
            raise ValueError("AudioOptions.bleep_start_padding must be positive")
        return True

    def _bleep_end_padding_validator(self, var):
        if type(var) is not float:
            raise ValueError(
                f"AudioOptions.bleep_end_padding must be of type float, but got {type(var)}"
            )
        if var < 0:
            raise ValueError("AudioOptions.bleep_end_padding must be positive")
        return True

    def _bleep_frequency_validator(self, var):
        if type(var) is not int and var is not None:
            raise ValueError(
                f"AudioOptions.bleep_frequency must be of type int or None, but got {type(var)}"
            )
        return True

    def _bleep_gain_validator(self, var):
        if type(var) is not int and var is not None:
            raise ValueError(
                f"AudioOptions.bleep_gain must be of type int or None, but got {type(var)}"
            )
        return True

    @classmethod
    def fromdict(cls, values: dict):
        try:
            return cls._fromdict(values)
        except TypeError:
            raise TypeError(
                "ProcessedText can only accept the values 'bleep_start_padding', 'bleep_end_padding', 'bleep_frequency', and 'bleep_gain'"
            )


class ImageOptions(BaseRequestObject):
    default_masking_method: str = "blur"
    default_palette: bool = False
    VALID_MASK_MODES = ["blur", "blackbox"]

    def __init__(
        self,
        masking_method: str = default_masking_method,
        palette: Optional[bool] = default_palette,
    ):
        if self._masking_method_validator(masking_method):
            self._masking_method = masking_method
        if self._palette_validator(palette):
            self._palette = palette

    @property
    def masking_method(self):
        return self._masking_method

    @property
    def palette(self):
        return self._palette

    @masking_method.setter
    def masking_method(self, var):
        if self._masking_method_validator(var):
            self._masking_method = var

    @palette.setter
    def palette(self, var):
        if self._palette_validator(var):
            self._palette = var

    def _masking_method_validator(self, var):
        if var not in self.VALID_MASK_MODES:
            raise ValueError(
                f"ImageOptions.masking_method must be one of {self.VALID_MASK_MODES}, but got {var}"
            )
        return True

    def _palette_validator(self, var):
        if not isinstance(var, bool):
            raise ValueError(
                f"ImageOptions.palette must be of type bool, but got {type(var)}"
            )
        return True

    @classmethod
    def fromdict(cls, values: dict):
        try:
            return cls._fromdict(values)
        except TypeError:
            raise TypeError(
                "ImageOptions can only accept the values 'masking_method' and 'palette'"
            )


class Entity(BaseRequestObject):
    def __init__(self, processed_text: str, text: str):
        if self._processed_text_validator(processed_text):
            self._processed_text = processed_text
        if self._text_validator(text):
            self._text = text

    @property
    def processed_text(self):
        return self._processed_text

    @property
    def text(self):
        return self._text

    @processed_text.setter
    def processed_text(self, var):
        if self._processed_text_validator(var):
            self._processed_text = var

    @text.setter
    def text(self, var):
        if self._text_validator(var):
            self._text = var

    def _processed_text_validator(self, var):
        if type(var) is not str:
            raise TypeError(
                f"{var} is not valid. Entity.processed_text must be of type string"
            )
        return True

    def _text_validator(self, var):
        if type(var) is not str:
            raise TypeError(f"{var} is not valid. Entity.text must be of type string")
        return True

    @classmethod
    def fromdict(cls, values: dict):
        try:
            return cls._fromdict(values)
        except TypeError:
            raise TypeError(
                "Entity can only accept the values 'processed_text' and 'text'"
            )


class EntityTypeSelector(BaseRequestObject):
    valid_types = ["DISABLE", "ENABLE"]

    def __init__(self, type: str, value: List[str] = []):
        if self._type_validator(type):
            self._type = type
        if self._value_validator(value):
            self.value = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, var):
        if self._type_validator(var):
            self._type = var

    def _type_validator(self, var):
        if var not in self.valid_types:
            raise ValueError(
                f"'{var}' is not valid. EntityTypeSelector.type can only be one of the following: {', '.join(self.valid_types)}"
            )
        return True

    def _value_validator(self, var):
        if type(var) is not list:
            raise TypeError("EntityTypeSelector.value must be of type list")
        return True

    @classmethod
    def fromdict(cls, values: dict):
        try:
            return cls._fromdict(values)
        except TypeError:
            raise TypeError(
                "EntityTypeSelector can only accept the values 'type' and 'value'"
            )


class File(BaseRequestObject):
    valid_content_types = [
        "application/json",
        "application/msword",
        "application/vnd.ms-powerpoint",
        "application/pdf",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "application/xml",
        "message/rfc822",
        "text/csv",
        "text/plain",
        "image/jpeg",
        "image/jpg",
        "image/tif",
        "image/tiff",
        "image/png",
        "image/bmp",
        "application/dicom",
        "audio/mp4",
        "audio/m4a",
        "audio/mp4a-latm",
        "audio/mp3",
        "audio/mpeg",
        "audio/wav",
        "audio/x-wav",
    ]

    def __init__(self, data: str, content_type: str):
        if self._data_validator(data):
            self._data = data
        if self._content_type_validator(content_type):
            self._content_type = content_type

    @property
    def data(self):
        return self._data

    @property
    def content_type(self):
        return self._content_type

    @data.setter
    def data(self, var):
        if self._data_validator(var):
            self._data = var

    @content_type.setter
    def content_type(self, var):
        if self._content_type_validator(var):
            self._content_type = var

    def _data_validator(self, var):
        if type(var) is not str:
            raise TypeError("data must be string-type")
        return True

    def _content_type_validator(self, var):
        if var not in self.valid_content_types:
            raise ValueError(
                f"{var} is not valid. File.content_type can only be one of the following: {', '.join(self.valid_content_types)}"
            )
        return True

    @classmethod
    def fromdict(cls, values: dict):
        try:
            return cls._fromdict(values)
        except TypeError:
            raise TypeError("File can only accept the values 'data' and 'content_type'")


class FilterSelector(BaseRequestObject):
    valid_types = ["ALLOW", "BLOCK", "ALLOW_TEXT"]
    default_threshold = 1

    def __init__(
        self,
        type: str,
        pattern: str,
        entity_type: str = None,
        threshold: Union[int, float] = default_threshold,
    ):
        if self._type_validator(type):
            self._type = type
        if self._pattern_validator(pattern):
            self._pattern = pattern
        if self.type == "BLOCK":
            if self._entity_type_validator(entity_type):
                self._entity_type = entity_type
            if self._threshold_validator(threshold):
                self._threshold = threshold

    @property
    def type(self):
        return self._type

    @property
    def pattern(self):
        return self._pattern

    @property
    def entity_type(self):
        if self.type != "BLOCK":
            raise AttributeError(
                f"FilterSelector of type {self.type} does not contain entity_type"
            )
        return self._entity_type

    @property
    def threshold(self):
        if self.type != "BLOCK":
            raise AttributeError(
                f"FilterSelector of type {self.type} does not contain threshold"
            )
        return self._threshold

    @type.setter
    def type(self, var):
        if self._type_validator(var):
            self._type = var

    @pattern.setter
    def pattern(self, var):
        if self._pattern_validator(var):
            self._pattern = var

    @entity_type.setter
    def entity_type(self, var):
        if self._entity_type_validator(var):
            self._entity_type = var

    @threshold.setter
    def threshold(self, var):
        if self._threshold_validator(var):
            self._threshold = var

    def _type_validator(self, var):
        if var not in self.valid_types:
            raise ValueError(
                f"{var} is not valid. FilterSelector.type can only be one of the following: {', '.join(self.valid_types)}"
            )
        return True

    def _pattern_validator(self, var):
        if type(var) is not str:
            raise TypeError("FilterSelector.pattern must be of type string")
        return True

    def _entity_type_validator(self, var):
        if type(var) is not str:
            raise TypeError("FilterSelector.entity_type must be of type string")
        return True

    def _threshold_validator(self, var):
        if var < 0:
            raise TypeError("FilterSelector.threshold must be greater than 0")
        return True

    @classmethod
    def fromdict(cls, values: dict):
        try:
            return cls._fromdict(values)
        except TypeError:
            raise TypeError(
                "FilterSelector can only accept the values 'type' and 'pattern'"
            )


class PDFOptions(BaseRequestObject):
    default_density = 200
    default_max_resolution = 3000
    default_enable_pdf_text_layer: bool = True

    def __init__(
        self,
        density: int = default_density,
        max_resolution: int = default_max_resolution,
        enable_pdf_text_layer: bool = default_enable_pdf_text_layer,
    ):
        self._density = density
        self._max_resolution = max_resolution
        self._enable_pdf_text_layer = enable_pdf_text_layer

    @property
    def density(self):
        return self._density

    @property
    def max_resolution(self):
        return self._max_resolution

    @property
    def enable_pdf_text_layer(self):
        return self._enable_pdf_text_layer

    @density.setter
    def density(self, var):
        if self._density_validator(var):
            self._density = var

    @max_resolution.setter
    def max_resolution(self, var):
        if self._max_resolution_validator(var):
            self._max_resolution = var

    @enable_pdf_text_layer.setter
    def enable_pdf_text_layer(self, var):
        if self._enable_pdf_text_layer_validator(var):
            self._enable_pdf_text_layer = var

    def _density_validator(self, var):
        if type(var) is not int:
            raise ValueError("PDFOptions.density must be of type int and >0")
        return True

    def _max_resolution_validator(self, var):
        if type(var) is not int:
            raise ValueError("PDFOptions.max_resolution must be of type int and >0")
        return True

    def _enable_pdf_text_layer_validator(self, var):
        if type(var) is not bool:
            raise ValueError("PDFOptions.enable_pdf_text_layer must be of type bool")
        return True

    @classmethod
    def fromdict(cls, values: dict):
        try:
            return cls._fromdict(values)
        except TypeError:
            raise TypeError(
                "PDFOptions can only accept 'density', 'max_resolution' and 'enable_pdf_text_layer'"
            )


class OCROptions(BaseRequestObject):
    default_ocr_system = "paddleocr"
    VALID_OCR_SYSTEM = [
        "azure_computer_vision",
        "azure_doc_intelligence",
        "hybrid",
        "paddleocr",
    ]

    def __init__(self, ocr_system: str = default_ocr_system):
        self._ocr_system = ocr_system

    @property
    def ocr_system(self):
        return self._ocr_system

    @ocr_system.setter
    def ocr_system(self, var):
        if self._ocr_system_validator(var):
            self._ocr_system = var

    def _ocr_system_validator(self, var):
        if var not in self.VALID_OCR_SYSTEM:
            raise ValueError(
                f"OCROptions.ocr_system must be one of {','.join(self.VALID_OCR_SYSTEM)}, but got {var}"
            )
        return True

    @classmethod
    def fromdict(cls, values: dict):
        try:
            return cls._fromdict(values)
        except TypeError:
            raise TypeError("OCROptions can only accept 'ocr_system'")


class ObjectEntityTypeSelector(BaseRequestObject):
    valid_types = ["DISABLE", "ENABLE"]
    valid_values = {"FACE", "LICENSE_PLATE", "LOGO", "SIGNATURE"}

    def __init__(self, type: str, value: List[str] = []):
        if self._type_validator(type):
            self._type = type
        if self._value_validator(value):
            self.value = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, var):
        if self._type_validator(var):
            self._type = var

    def _type_validator(self, var):
        if var not in self.valid_types:
            raise ValueError(
                f"'{var}' is not valid. ObjectEntityTypeSelector.type can only be one of the following: {', '.join(self.valid_types)}"
            )
        return True

    def _value_validator(self, var):
        if type(var) is not list:
            raise TypeError("ObjectEntityTypeSelector.value must be of type list")
        elif var and not all(value in self.valid_values for value in var):
            raise ValueError(
                f"'{var}' is not valid. ObjectEntityTypeSelector.value can only be one of the following: {', '.join(self.valid_values)}"
            )
        return True

    @classmethod
    def fromdict(cls, values: dict):
        try:
            return cls._fromdict(values)
        except TypeError:
            raise TypeError(
                "ObjectEntityTypeSelector can only accept the values 'type' and 'value'"
            )


class ProcessedMarkerText(BaseRequestObject):
    attributes = ["_pattern"]
    default_pattern = "[UNIQUE_NUMBERED_ENTITY_TYPE]"
    valid_patterns = [
        "BEST_ENTITY_TYPE",
        "ALL_ENTITY_TYPES",
        "UNIQUE_NUMBERED_ENTITY_TYPE",
        "UNIQUE_HASHED_ENTITY_TYPE",
    ]
    default_marker_language = "en"
    valid_marker_languages = ["auto", "en", "fr", "de", "ja", "ko", "nl", "ru", "uk"]
    default_coreference_resolution = "heuristics"
    valid_coreference_resolutions = ["heuristics", "model_prediction", "combined"]

    def __init__(
        self,
        pattern: str = default_pattern,
        marker_language: str = default_marker_language,
        coreference_resolution: str = default_coreference_resolution,
    ):
        for attribute in (
            ProcessedMaskText.attributes + ProcessedSyntheticText.attributes
        ):
            delattr(self, attribute) if hasattr(self, attribute) else False
        self._type = "MARKER"
        if self._pattern_validator(pattern):
            self._pattern = pattern
        if self._marker_language_validator(marker_language):
            self._marker_language = marker_language
        if self._coreference_resolution_validator(coreference_resolution):
            self._coreference_resolution = coreference_resolution

    @property
    def pattern(self):
        return self._pattern

    @property
    def marker_language(self):
        return self._marker_language

    @property
    def coreference_resolution(self):
        return self._coreference_resolution

    @pattern.setter
    def pattern(self, var):
        if self._pattern_validator(var):
            self._pattern = var

    @marker_language.setter
    def marker_language(self, var):
        if self._marker_language_validator(var):
            self._marker_language = var

    @coreference_resolution.setter
    def coreference_resolution(self, var):
        if self._coreference_resolution_validator(var):
            self._coreference_resolution = var

    def _pattern_validator(self, var):
        if var not in self.valid_patterns and var[1:-1] not in self.valid_patterns:
            raise ValueError(
                f"{var} is not valid. ProcessedText.pattern can only be one of the following: {', '.join(self.valid_patterns)}"
            )
        return True

    def _marker_language_validator(self, var):
        if var not in self.valid_marker_languages:
            raise ValueError(
                f"{var} is not valid. ProcessedText.marker_language can only be one of the following: {', '.join(self.valid_marker_languages)}"
            )
        return True

    def _coreference_resolution_validator(self, var):
        if var not in self.valid_coreference_resolutions:
            raise ValueError(
                f"{var} is not valid. ProcessedText.coreference_resolution can only be one of the following: {', '.join(self.valid_coreference_resolutions)}"
            )
        return True


class ProcessedMaskText(BaseRequestObject):
    attributes = ["_mask_character"]

    def __init__(self, mask_character: str = "#"):
        for attribute in (
            ProcessedMarkerText.attributes + ProcessedSyntheticText.attributes
        ):
            delattr(self, attribute) if hasattr(self, attribute) else False
        if self._mask_character_validator(mask_character):
            self._mask_character = mask_character
        self._type = "MASK"

    @property
    def mask_character(self):
        return self._mask_character

    @mask_character.setter
    def mask_character(self, var):
        if self._mask_character_validator(var):
            self._mask_character = var

    def _mask_character_validator(self, var):
        if len(var) != 1:
            raise ValueError(
                f"mask_character must have only one character. {var} has {len(var)} characters."
            )
        return True


class ProcessedSyntheticText(BaseRequestObject):
    attributes = ["_synthetic_entity_accuracy", "_preserve_relationships"]
    valid_synthetic_accuracy_values = ["standard", "standard_multilingual"]

    def __init__(
        self,
        synthetic_entity_accuracy: str = "standard",
        preserve_relationships: bool = True,
    ):
        for attribute in ProcessedMarkerText.attributes + ProcessedMaskText.attributes:
            delattr(self, attribute) if hasattr(self, attribute) else False
        self._type = "SYNTHETIC"
        if self._synthetic_entity_accuracy_validator(synthetic_entity_accuracy):
            self._synthetic_entity_accuracy = synthetic_entity_accuracy
        self._preserve_relationships = preserve_relationships
        self._preserve_relationships = True

    @property
    def synthetic_entity_accuracy(self):
        return self._synthetic_entity_accuracy

    @synthetic_entity_accuracy.setter
    def synthetic_entity_accuracy(self, var):
        if self._synthetic_entity_accuracy_validator(var):
            self._synthetic_entity_accuracy = var

    @property
    def preserve_relationships(self):
        return self._preserve_relationships

    @preserve_relationships.setter
    def preserve_relationships(self, var):
        self._preserve_relationships = var

    def _synthetic_entity_accuracy_validator(self, var):
        if var not in self.valid_synthetic_accuracy_values:
            raise ValueError(
                f"{var} is not valid. Synthetic Entity Accuracy can only accept values {', '.join(self.valid_synthetic_accuracy_values)}"
            )


class ProcessedText(ProcessedMarkerText, ProcessedMaskText, ProcessedSyntheticText):
    default_type = "MARKER"
    valid_types = ["MARKER", "MASK", "SYNTHETIC"]

    def __init__(self, type: str = default_type, **kwargs):
        if type == "MARKER":
            ProcessedMarkerText.__init__(self, **kwargs)
        elif type == "MASK":
            ProcessedMaskText.__init__(self, **kwargs)
        elif type == "SYNTHETIC":
            ProcessedSyntheticText.__init__(self, **kwargs)
        else:
            raise ValueError(
                f"{type} is not valid. ProcessedText.type can only be one of the following: {', '.join(self.valid_types)}"
            )

    @classmethod
    def fromdict(cls, values: dict):
        try:
            return cls._fromdict(values)
        except TypeError:
            raise TypeError(
                "ProcessedText can only accept the values 'type' and 'pattern'"
            )

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, var):
        if var in self.valid_types and var != self._type:
            self.__init__(var)


class Timestamp(BaseRequestObject):
    def __init__(self, start, end):
        if self._start_validator(start):
            self._start = start
        if self._end_validator(end):
            self._end = end

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @start.setter
    def start(self, var):
        if self._start_validator(var):
            self._start = var

    @end.setter
    def end(self, var):
        if self._end_validator(var):
            self._end = var

    def _start_validator(self, var):
        if type(var) is not float:
            raise ValueError("Timestamp.start must be of type float")
        return True

    def _end_validator(self, var):
        if type(var) is not float:
            raise ValueError("Timestamp.end must be of type float")
        return True

    @classmethod
    def fromdict(cls, values: dict):
        try:
            return cls._fromdict(values)
        except TypeError:
            raise TypeError("Timestamp can only accept the values 'start' and 'end'")


class EntityDetection(BaseRequestObject):
    default_accuracy = "high_automatic"
    default_return_entity = True
    valid_accuracies = [
        "standard",
        "standard_high",
        "standard_high_multilingual",
        "high",
        "high_multilingual",
        "standard_high_automatic",
        "high_automatic",
    ]
    default_enable_non_max_suppression = False

    def __init__(
        self,
        accuracy: str = default_accuracy,
        entity_types: List[EntityTypeSelector] = [],
        filter: List[FilterSelector] = [],
        return_entity: bool = default_return_entity,
        enable_non_max_suppression: bool = default_enable_non_max_suppression,
    ):
        if self._accuracy_validator(accuracy):
            self._accuracy = accuracy
        if self._entity_types_validator(entity_types):
            self.entity_types = entity_types
        if self._filter_validator(filter):
            self.filter = filter
        if self._return_entity_validator(return_entity):
            self._return_entity = return_entity
        if self._enable_non_max_suppression_validator(enable_non_max_suppression):
            self._enable_non_max_suppression = enable_non_max_suppression

    @property
    def accuracy(self):
        return self._accuracy

    @property
    def return_entity(self):
        return self._return_entity

    @accuracy.setter
    def accuracy(self, var):
        if self._accuracy_validator(var):
            self._accuracy = var

    @return_entity.setter
    def return_entity(self, var):
        if self._return_entity_validator(var):
            self._return_entity = var

    def _accuracy_validator(self, var):
        if var not in self.valid_accuracies:
            raise ValueError(
                f"{var} is not valid. EntityDetection.accuracy can only be one of the following: {', '.join(self.valid_accuracies)}"
            )
        return True

    def _entity_types_validator(self, var):
        if type(var) is not list:
            raise TypeError(
                f"{var} is not valid. EntityDetection.entity_types can only be a list"
            )
        elif var and not all(isinstance(row, EntityTypeSelector) for row in var):
            raise ValueError(
                "EntityDetection.entity_types can only contain EntityTypeSelector objects"
            )
        return True

    def _filter_validator(self, var):
        if type(var) is not list:
            raise ValueError(
                f"{var} is not valid. EntityDetection.filter can only be a list"
            )
        elif var and not all(isinstance(x, FilterSelector) for x in var):
            raise ValueError(
                "EntityDetection.filter can only contain FilterSelector objects"
            )
        return True

    def _return_entity_validator(self, var):
        if type(var) is not bool:
            raise ValueError("EntityDetection.return_entity must be of type bool")
        return True

    def _enable_non_max_suppression_validator(self, var):
        if type(var) is not bool:
            raise ValueError(
                "EntityDetection.enable_non_max_suppression must be of type bool"
            )
        return True

    @classmethod
    def fromdict(cls, values: dict):
        try:
            initializer_dict = {}
            for key, value in values.items():
                if key == "entity_types":
                    initializer_dict[key] = [
                        EntityTypeSelector.fromdict(row) for row in value
                    ]
                elif key == "filter":
                    initializer_dict[key] = [
                        FilterSelector.fromdict(row) for row in value
                    ]
                else:
                    initializer_dict[key] = value
            return cls._fromdict(initializer_dict)
        except TypeError:
            raise TypeError(
                "EntityDetection can only accept the values 'accuracy', 'entity_types', 'filter' and 'return_entity'"
            )


class ObjectEntityDetection(BaseRequestObject):
    def __init__(self, object_entity_types: List[ObjectEntityTypeSelector] = []):
        if self._object_entity_types_validator(object_entity_types):
            self.object_entity_types = object_entity_types

    def _object_entity_types_validator(self, var):
        if type(var) is not list:
            raise TypeError(
                f"{var} is not valid. ObjectEntityDetection.object_entity_types can only be a list"
            )
        elif var and not all(isinstance(row, ObjectEntityTypeSelector) for row in var):
            raise ValueError(
                "ObjectEntityDetection.object_entity_types can only contain ObjectEntityTypeSelector objects"
            )
        return True

    @classmethod
    def fromdict(cls, values: dict):
        try:
            initializer_dict = {}
            for key, value in values.items():
                if key == "object_entity_types":
                    initializer_dict[key] = [
                        ObjectEntityTypeSelector.fromdict(row) for row in value
                    ]
                else:
                    initializer_dict[key] = value
            return cls._fromdict(initializer_dict)
        except TypeError:
            raise TypeError(
                "ObjectEntityDetection can only accept the value 'object_entity_types'"
            )


class ProcessTextRequest(BaseRequestObject):
    def __init__(
        self,
        text: List[str],
        link_batch: Optional[bool] = None,
        entity_detection: Optional[EntityDetection] = None,
        processed_text: Optional[ProcessedText] = None,
        project_id: Optional[str] = None,
    ):
        self.text = text
        self.link_batch = link_batch
        self.entity_detection = entity_detection
        self.processed_text = processed_text
        self.project_id = project_id

    @classmethod
    def fromdict(cls, values: dict):
        try:
            initializer_dict = {}
            for key, value in values.items():
                if key == "entity_detection":
                    initializer_dict[key] = EntityDetection.fromdict(value)
                elif key == "processed_text":
                    initializer_dict[key] = ProcessedText.fromdict(value)
                else:
                    initializer_dict[key] = value
            return cls._fromdict(initializer_dict)
        except TypeError:
            raise TypeError(
                "ProcessTextRequest can only accept the values 'text', 'link_batch', 'entity_detection' and 'process_text'"
            )


class NerTextRequest(BaseRequestObject):
    def __init__(
        self,
        text: List[str],
        link_batch: Optional[bool] = None,
        entity_detection: Optional[EntityDetection] = None,
        project_id: Optional[str] = None,
    ):
        self.text = text
        self.link_batch = link_batch
        self.entity_detection = entity_detection
        self.project_id = project_id

    @classmethod
    def fromdict(cls, values: dict):
        try:
            initializer_dict = {}
            for key, value in values.items():
                if key == "entity_detection":
                    initializer_dict[key] = EntityDetection.fromdict(value)
                else:
                    initializer_dict[key] = value
            return cls._fromdict(initializer_dict)
        except TypeError:
            raise TypeError(
                "NerTextRequest can only accept the values 'text', 'link_batch' and 'entity_detection'"
            )


class AnalyzeTextRequest(BaseRequestObject):
    def __init__(
        self,
        text: List[str],
        locale: str,
        link_batch: Optional[bool] = None,
        entity_detection: Optional[EntityDetection] = None,
        project_id: Optional[str] = None,
    ):
        self.text = text
        self.locale = locale
        self.link_batch = link_batch
        self.entity_detection = entity_detection
        self.project_id = project_id

    @classmethod
    def fromdict(cls, values: dict):
        try:
            initializer_dict = {}
            for key, value in values.items():
                if key == "entity_detection":
                    initializer_dict[key] = EntityDetection.fromdict(value)
                else:
                    initializer_dict[key] = value
            return cls._fromdict(initializer_dict)
        except TypeError:
            raise TypeError(
                "AnalyzeTextRequest can only accept the values 'text', 'locale', 'link_batch' and 'entity_detection'"
            )


class ProcessFileUriRequest(BaseRequestObject):
    def __init__(
        self,
        uri: str,
        entity_detection: Optional[EntityDetection] = None,
        object_entity_detection: Optional[ObjectEntityDetection] = None,
        pdf_options: Optional[PDFOptions] = None,
        audio_options: Optional[AudioOptions] = None,
        image_options: Optional[ImageOptions] = None,
        project_id: Optional[str] = None,
        ocr_options: Optional[OCROptions] = None,
    ):
        self.uri = uri
        self.entity_detection = entity_detection
        self.object_entity_detection = object_entity_detection
        self.pdf_options = pdf_options
        self.audio_options = audio_options
        self.image_options = image_options
        self.project_id = project_id
        self.ocr_options = ocr_options

    @classmethod
    def fromdict(cls, values: dict):
        try:
            initializer_dict = {}
            for key, value in values.items():
                if key == "entity_detection":
                    initializer_dict[key] = EntityDetection.fromdict(value)
                elif key == "object_entity_detection":
                    initializer_dict[key] = ObjectEntityDetection.fromdict(value)
                elif key == "pdf_options":
                    initializer_dict[key] = PDFOptions.fromdict(value)
                elif key == "audio_options":
                    initializer_dict[key] = AudioOptions.fromdict(value)
                elif key == "image_options":
                    initializer_dict[key] = ImageOptions.fromdict(value)
                elif key == "ocr_options":
                    initializer_dict[key] = OCROptions.fromdict(value)
                else:
                    initializer_dict[key] = value
            return cls._fromdict(initializer_dict)
        except TypeError:
            raise TypeError(
                "ProcessFileUriRequest can only accept the values 'uri', 'entity_detection', 'object_entity_detection', 'pdf_options', 'audio_options', 'image_options' and 'ocr_options'"
            )


class ProcessFileBase64Request(BaseRequestObject):
    def __init__(
        self,
        file: File,
        entity_detection: Optional[EntityDetection] = None,
        object_entity_detection: Optional[ObjectEntityDetection] = None,
        pdf_options: Optional[PDFOptions] = None,
        audio_options: Optional[AudioOptions] = None,
        image_options: Optional[ImageOptions] = None,
        project_id: Optional[str] = None,
        ocr_options: Optional[OCROptions] = None,
    ):
        self.file = file
        self.entity_detection = entity_detection
        self.object_entity_detection = object_entity_detection
        self.pdf_options = pdf_options
        self.audio_options = audio_options
        self.image_options = image_options
        self.project_id = project_id
        self.ocr_options = ocr_options

    @classmethod
    def fromdict(cls, values: dict):
        try:
            initializer_dict = {}
            for key, value in values.items():
                if key == "file":
                    initializer_dict[key] = File.fromdict(value)
                elif key == "entity_detection":
                    initializer_dict[key] = EntityDetection.fromdict(value)
                elif key == "object_entity_detection":
                    initializer_dict[key] = ObjectEntityDetection.fromdict(value)
                elif key == "pdf_options":
                    initializer_dict[key] = PDFOptions.fromdict(value)
                elif key == "audio_options":
                    initializer_dict[key] = AudioOptions.fromdict(value)
                elif key == "image_options":
                    initializer_dict[key] = ImageOptions.fromdict(value)
                elif key == "ocr_options":
                    initializer_dict[key] = OCROptions.fromdict(value)
                else:
                    initializer_dict[key] = value
            return cls._fromdict(initializer_dict)
        except TypeError:
            raise TypeError(
                "ProcessFileBase64Request can only accept the values 'file', 'entity_detection', 'object_entity_detection', 'pdf_options', 'audio_options', 'image_options' and 'ocr_options'"
            )


class BleepRequest(BaseRequestObject):
    def __init__(
        self,
        file: File,
        timestamps: List,
        bleep_frequency: Optional[int] = None,
        bleep_gain: Optional[int] = None,
    ):
        self.file = file
        self.timestamps = timestamps
        self.bleep_frequency = bleep_frequency
        self.bleep_gain = bleep_gain

    @classmethod
    def fromdict(cls, values: dict):
        try:
            initializer_dict = {}
            for key, value in values.items():
                if key == "file":
                    initializer_dict[key] = File.fromdict(value)
                elif key == "timestamps":
                    initializer_dict[key] = [
                        Timestamp.fromdict(entry) for entry in value
                    ]
                else:
                    initializer_dict[key] = value
            return cls._fromdict(initializer_dict)
        except TypeError:
            raise TypeError(
                "BleepRequest can only accept the values 'file', 'timestamps', 'bleep_frequency', and 'bleep_gain'"
            )


class ReidentifyTextRequest(BaseRequestObject):
    def __init__(
        self,
        processed_text: List[str] = [],
        entities: List[Entity] = [],
        model: str = "",
        reidentify_sensitive_fields: bool = True,
    ):
        self.reidentify_sensitive_fields = reidentify_sensitive_fields
        self.processed_text = processed_text
        self.entities = entities
        self.model = model

    @classmethod
    def fromdict(cls, values: dict):
        try:
            initializer_dict = {}
            for key, value in values.items():
                if key == "entities":
                    initializer_dict[key] = [
                        Entity.fromdict(entity) for entity in values[key]
                    ]
                else:
                    initializer_dict[key] = value
            return cls._fromdict(initializer_dict)
        except TypeError:
            raise TypeError(
                "ReidentifyTextRequest can only accept the values 'processed_text', 'entities', 'model' and 'reidentify_sensitive_fields'"
            )
