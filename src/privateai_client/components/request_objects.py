import inspect
from typing import List


class BaseRequestObject:

    def to_dict(self):
        dict_obj = dict()
        for key, value in self.__dict__.items():
            name = key if key[0] != "_" else key[1:]
            if self._issubclass(value):
                dict_obj[name] = value.to_dict()
            elif type(value) is list:
                dict_obj[name] = [row.to_dict() if self._issubclass(row) else row for row in value]
            elif not key.startswith('__') and not callable(key):
                dict_obj[name] = value
        return dict_obj

    def _issubclass(self, obj):
        return inspect.isclass(type(obj)) and issubclass(type(obj), BaseRequestObject)

    def __call__(self):
        return self.to_dict()

    @classmethod
    def _fromdict(cls,
                 values: dict):
        return cls(**values)

class AudioOptions(BaseRequestObject):
    default_bleep_start_padding = 0
    default_bleep_end_padding = 0

    def __init__(self, 
                 bleep_start_padding: int = default_bleep_start_padding,
                 bleep_end_padding: int = default_bleep_end_padding
    ):
        if self._bleep_start_padding_validator(bleep_start_padding):
            self._bleep_start_padding = bleep_start_padding
        if self._bleep_end_padding_validator(bleep_end_padding):
            self._bleep_end_padding = bleep_end_padding
    
    @property
    def bleep_start_padding(self):
        return self._bleep_start_padding
    
    @property
    def bleep_end_padding(self):
        return self._bleep_end_padding
    
    @bleep_start_padding.setter
    def bleep_start_padding(self, var):
        if self._bleep_start_padding_validator(var):
            self._bleep_start_padding = var
    
    @bleep_end_padding.setter
    def bleep_end_padding(self, var):
        if self._bleep_end_padding_validator(var):
            self._bleep_end_padding = var

    def _bleep_start_padding_validator(self, var):
        if type(var) is not int:
            raise ValueError("AudioOptions.bleep_start_padding must be of type int")
        return True
        
    def _bleep_end_padding_validator(self, var):
        if type(var) is not int:
            raise ValueError("AudioOptions.bleep_end_padding must be of type int")
        return True


    @classmethod
    def fromdict(cls, values: dict):
        try:
            return cls._fromdict(values)
        except TypeError:
            raise TypeError("ProcessedText can only accept the values 'bleep_start_padding' and 'bleep_end_padding'")

class EntityTypeSelector(BaseRequestObject):
    valid_types = ["DISABLE", "ENABLE"]

    def __init__(self,
                 type: str,
                 value: List[str] = []
    ):
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
        if  var not in self.valid_types:
            raise ValueError(f"'{var}' is not valid. EntityTypeSelector.type can only be one of the following: {', '.join(self.valid_types)}")
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
            raise TypeError("EntityTypeSelector can only accept the values 'type' and 'value'")

class File(BaseRequestObject):
    valid_content_types = ["application/pdf", "application/json", "application/xml", "image/jpg", "image/tiff", "audio/wav", "audio/mp3"]

    def __init__(self,
                 data: str,
                 content_type: str                 
    ):
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
            raise ValueError(f"{var} is not valid. File.content_type can only be one of the following: {', '.join(self.valid_content_types)}")
        return True
    
    @classmethod
    def fromdict(cls, values: dict):
        try:
            return cls._fromdict(values)
        except TypeError:
            raise TypeError("File can only accept the values 'data' and 'content_type'")
    
class FilterSelector(BaseRequestObject):
    valid_types = ["ALLOW", "BLOCK"]

    def __init__(self,
                 type: str,
                 pattern: str             
    ):
        if self._type_validator(type):
            self._type = type
        if self._pattern_validator(pattern):
            self._pattern = pattern
    
    @property
    def type(self):
        return self._type
    
    @property
    def pattern(self):
        return self._pattern
    
    @type.setter
    def type(self, var):
        if self._type_validator(var):
            self._type = var

    @pattern.setter
    def pattern(self, var):
        if self._pattern_validator(var):
            self._pattern = var
        
    def _type_validator(self, var):
        if  var not in self.valid_types:
            raise ValueError(f"{var} is not valid. FilterSelector.type can only be one of the following: {', '.join(self.valid_types)}")
        return True
    
    def _pattern_validator(self, var):
        if type(var) is not str:
            raise TypeError("FilterSelector.pattern must be of type string")
        return True
    
    @classmethod
    def fromdict(cls, values: dict):
        try:
            return cls._fromdict(values)
        except TypeError:
            raise TypeError("FilterSelector can only accept the values 'type' and 'pattern'")

class PDFOptions(BaseRequestObject): 
    default_density = 150

    def __init__(self,
                 density: int = default_density             
    ):
        self._density = density

    @property
    def density(self):
        return self._density
    
    @density.setter
    def density(self, var):
        if self._density_validator(var):
            self._density = var

    def _density_validator(self, var):
        if type(var) is not int:
            raise ValueError("PDFOptions.density must be of type int")
        return True

    @classmethod
    def fromdict(cls, values: dict):
        try:
            return cls._fromdict(values)
        except TypeError:
            raise TypeError("PDFOptions can only accept 'density'")

class ProcessedText(BaseRequestObject):
    default_type = "MARKER"
    default_pattern = "[UNIQUE_NUMBERED_ENTITY_TYPE]"
    valid_types = ["MARKER", "MASK", "SYNTHETIC"]
    valid_patterns = ["BEST_ENTITY_TYPE", "ALL_ENTITY_TYPES", "UNIQUE_NUMBERED_ENTITY_TYPE"]
    
    def __init__(self,
                 type: str = default_type,
                 pattern: str = default_pattern             
    ):
        if self._type_validator(type):
            self._type = type
        if self._pattern_validator(pattern):
            self._pattern = pattern
    @property
    def type(self):
        return self._type
    
    @property
    def pattern(self):
        return self._pattern
    
    @type.setter
    def type(self, var):
        if self._type_validator(var):
            self._type = var
    
    @pattern.setter
    def pattern(self, var):
        if self._pattern_validator(var):
            self._pattern = var

    def _type_validator(self, var):

        if var not in self.valid_types:
            raise ValueError(f"{var} is not valid. ProcessedText.type can only be one of the following: {', '.join(self.valid_types)}")
        return True

    def _pattern_validator(self, var):
        if var not in self.valid_patterns and var[1:-1] not in self.valid_patterns:
            raise ValueError(f"{var} is not valid. ProcessedText.pattern can only be one of the following: {', '.join(self.valid_patterns)}")
        return True

    @classmethod
    def fromdict(cls, values: dict):
        try:
            return cls._fromdict(values)
        except TypeError:
            raise TypeError("ProcessedText can only accept the values 'type' and 'pattern'")

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
    default_accuracy = "high"
    default_return_entity = True
    valid_accuracies = ["standard", "standard_high", "standard_high_multilinguals", "high", "high_multilingual"]

    def __init__(self,
                 accuracy: str = default_accuracy,
                 entity_types: List[EntityTypeSelector] = [],
                 filter: List[FilterSelector] = [],
                 return_entity: bool = default_return_entity
    ):
        if self._accuracy_validator(accuracy):
            self._accuracy = accuracy
        if self._entity_types_validator(entity_types):
            self.entity_types = entity_types
        if self._filter_validator(filter):
            self.filter = filter
        if self._return_entity_validator(return_entity):
            self._return_entity = return_entity

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
            raise ValueError(f"{var} is not valid. EntityDetection.accuracy can only be one of the following: {', '.join(self.valid_accuracies)}")
        return True
    
    def _entity_types_validator(self, var):
        if type(var) is not list:
            raise TypeError(f"{var} is not valid. EntityDetection.entity_types can only be a list")
        elif var and not all(isinstance(row, EntityTypeSelector) for row in var):
            raise ValueError("EntityDetection.entity_types can only contain EntityTypeSelector objects")
        return True

    def _filter_validator(self, var):
        if type(var) is not list:
            raise ValueError(f"{var} is not valid. EntityDetection.filter can only be a list")
        elif var and not all(isinstance(x, FilterSelector) for x in var):
            raise ValueError("EntityDetection.filter can only contain FilterSelector objects")
        return True

    def _return_entity_validator(self, var):
        if type(var) is not bool:
            raise ValueError("EntityDetection.return_entity must be of type bool")
        return True

    @classmethod
    def fromdict(cls, values: dict):
        try:
            initializer_dict = {}
            for key, value in values.items():
                if key == "entity_types":
                    initializer_dict[key] = [EntityTypeSelector.fromdict(row) for row in value]
                elif key == "filter":
                    initializer_dict[key] = [FilterSelector.fromdict(row) for row in value]
                else:
                    initializer_dict[key] = value
            return cls._fromdict(initializer_dict)
        except TypeError:
            raise TypeError("EntityDetection can only accept the values 'accuracy', 'entity_types', 'filter' and 'return_entity'")

class ProcessTextRequest(BaseRequestObject):
    default_link_batch = False

    def __init__(self, 
                 text: List[str], 
                 link_batch: bool = default_link_batch,
                 entity_detection: EntityDetection = EntityDetection(),
                 processed_text: ProcessedText = ProcessedText()
    ):
        self.text = text
        self.link_batch = link_batch
        self.entity_detection = entity_detection
        self.processed_text = processed_text

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
            raise TypeError("ProcessTextRequest can only accept the values 'text', 'link_batch', 'entity_detection' and 'process_text'")
    
class ProcessFileUriRequest(BaseRequestObject):

    def __init__(self,
                 uri: str,
                 entity_detection: EntityDetection = EntityDetection(),
                 pdf_options: PDFOptions = PDFOptions(),
                 audio_options: AudioOptions = AudioOptions()                  
    ):
        self.uri = uri
        self.entity_detection = entity_detection
        self.pdf_options = pdf_options
        self.audio_options = audio_options

    @classmethod
    def fromdict(cls, values: dict):
        try:
            initializer_dict = {}
            for key, value in values.items():
                if key == "entity_detection":
                    initializer_dict[key] = EntityDetection.fromdict(value)
                elif key == "pdf_options":
                    initializer_dict[key] = PDFOptions.fromdict(value)
                elif key == "audio_options":
                    initializer_dict[key] = AudioOptions.fromdict(value)
                else:
                    initializer_dict[key] = value
            return cls._fromdict(initializer_dict)
        except TypeError:
            raise TypeError("ProcessFileUriRequest can only accept the values 'uri', 'entity_detection', 'pdf_options and 'audio_options'")

class ProcessFileBase64Request(BaseRequestObject):

    def __init__(self,
                 file: File,
                 entity_detection: EntityDetection = EntityDetection(),
                 pdf_options: PDFOptions = PDFOptions(),
                 audio_options: AudioOptions = AudioOptions()                  
    ):
        self.file = file
        self.entity_detection = entity_detection
        self.pdf_options = pdf_options
        self.audio_options = audio_options

    @classmethod
    def fromdict(cls, values: dict):
        try:
            initializer_dict = {}
            for key, value in values.items():
                if key == "file":
                    initializer_dict[key] = File.fromdict(value)
                elif key == "entity_detection":
                    initializer_dict[key] = EntityDetection.fromdict(value)
                elif key == "pdf_options":
                    initializer_dict[key] = PDFOptions.fromdict(value)
                elif key == "audio_options":
                    initializer_dict[key] = AudioOptions.fromdict(value)
                else:
                    initializer_dict[key] = value
            return cls._fromdict(initializer_dict)
        except TypeError:
            raise TypeError("ProcessFileBase64Request can only accept the values 'file', 'entity_detection', 'pdf_options and 'audio_options'")

class BleepRequest(BaseRequestObject):

    def __init__(self,
                 file: File,
                 timestamps: List,             
    ):
        self.file = file
        self.timestamps = timestamps

    @classmethod
    def fromdict(cls, values: dict):
        try:
            initializer_dict = {}
            for key, value in values.items():
                if key == "file":
                    initializer_dict[key] = File.fromdict(value)
                elif key == "timestamps":
                    initializer_dict[key] = [Timestamp.fromdict(entry) for entry in value]
                else:
                    initializer_dict[key] = value
            return cls._fromdict(initializer_dict)
        except TypeError:
            raise TypeError("BleepRequest can only accept the values 'file'and 'timestamps'")
